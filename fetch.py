"""MacaoTube: find English-language YouTube videos about Macao by independent
creators, keep a growing catalogue of them, and score them.

Every run
  1. "newest" searches  - uploads from the last 14 days for the core queries
  2. rotating sweep     - a quarter of all queries, by relevance and by views
                          (every query gets a full sweep every 4 nights)
  3. refresh            - fresh stats for EVERY video in the catalogue, so videos
                          never drop off just because they slipped in a search

Quota (free tier = 10,000 units/day): search.list costs 100; videos.list and
channels.list cost 1 per 50 ids. A nightly run uses ~3,200 units. If the quota
runs out mid-run, whatever was found so far is kept.

Usage
  YT_KEY=... python3 fetch.py                 nightly run
  YT_KEY=... python3 fetch.py --full          sweep every query (≈8,000 units)
  YT_KEY=... python3 fetch.py --topics Food,Festivals   sweep only these topics

Files
  data/creators_seen.json   catalogue: video id -> topics, first_seen
  data/videos.json          scored videos (>= 1,000 views) read by rerank.py
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

KEY = os.environ.get('YT_KEY') or sys.exit('Set YT_KEY to your YouTube Data API key.')
API = 'https://www.googleapis.com/youtube/v3/'
HERE = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(HERE, 'data', 'creators_seen.json')
OUT = os.path.join(HERE, 'data', 'videos.json')
UNITS = 0

# Each query is tagged with the topic it feeds.
QUERIES = {
    'Travel': ['Macau travel guide', 'things to do in Macau', 'Macau vlog', 'Macau day trip from Hong Kong',
               'Macau first time', 'Macao travel', 'Macau itinerary', 'Macau walking tour', 'Macau budget travel'],
    'Food': ['Macau food', 'Macau street food', 'Macanese food', 'Macau egg tart', 'Macanese cooking',
             'Macau food tour', 'Macau Michelin'],
    'Casinos & hotels': ['Macau casino', 'Macau hotel tour', 'Cotai strip', 'House of Dancing Water'],
    'History & culture': ['Macau history', 'Macau Portuguese culture', 'Historic Centre of Macao',
                          'A-Ma Temple Macau', 'Ruins of St Paul Macau', 'Senado Square Macau', 'Macau museum'],
    'Festivals': ['Light Up Macao', 'Macao Food Festival', 'Macau Chinese New Year',
                  'Macao International Fireworks', 'Macao Arts Festival', 'Macau Christmas'],
    'Neighbourhoods': ['Taipa village', 'Coloane Macau', 'Macau Tower', 'Macau old town'],
    'Grand Prix': ['Macau Grand Prix'],
    'Living there': ['living in Macau', 'moving to Macau'],
}
# Searched for brand-new uploads every night.
NEWEST = ['Macau', 'Macao', 'Macau travel', 'Macau food', 'Macau vlog', 'Macau casino',
          'Light Up Macao', 'Macau Grand Prix', 'Taipa', 'Macao festival']
MACAU = re.compile(r'maca[uo]|澳門|澳门|taipa|coloane|cotai', re.I)


class QuotaExhausted(Exception):
    pass


def call(endpoint, cost, **params):
    global UNITS
    params['key'] = KEY
    url = API + endpoint + '?' + urllib.parse.urlencode(params)
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                UNITS += cost
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')
            if e.code == 403 and 'quota' in body.lower():
                raise QuotaExhausted(f'quota used up after ~{UNITS} units')
            if e.code in (400, 403):
                sys.exit(f'YouTube API refused the request ({e.code}): {body[:300]}')
            time.sleep(3 * (i + 1))
    sys.exit('YouTube API kept failing; try again later.')


def batched(ids, n=50):
    ids = list(ids)
    for i in range(0, len(ids), n):
        yield ids[i:i + n]


def iso_seconds(d):
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    if not m:
        return 0
    dd, h, mi, s = (int(x or 0) for x in m.groups())
    return dd * 86400 + h * 3600 + mi * 60 + s


def load_seen():
    if os.path.exists(SEEN):
        return json.load(open(SEEN))
    seen = {}  # first run: bootstrap the catalogue from the existing scored list
    if os.path.exists(OUT):
        for v in json.load(open(OUT)):
            seen[v['id']] = {'topics': v.get('topics', []), 'first_seen': datetime.now(timezone.utc).date().isoformat()}
    return seen


def plan(args):
    """Return (newest_queries, [(topic, query, order), ...]) for this run."""
    pairs = [(t, q) for t, qs in QUERIES.items() for q in qs]
    if '--full' in args:
        chosen = pairs
    elif '--topics' in args:
        want = {t.strip().lower() for t in args[args.index('--topics') + 1].split(',')}
        chosen = [(t, q) for t, q in pairs if t.lower() in want]
    else:
        slot = datetime.now(timezone.utc).timetuple().tm_yday % 4
        chosen = [p for i, p in enumerate(pairs) if i % 4 == slot]
    newest = [] if ('--full' in args or '--topics' in args) else NEWEST
    return newest, [(t, q, o) for t, q in chosen for o in ('relevance', 'viewCount')]


def search(args, seen):
    newest, sweep = plan(args)
    today = datetime.now(timezone.utc).date().isoformat()
    since = (datetime.now(timezone.utc) - timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%SZ')
    found = {}
    jobs = [('New', q, 'date') for q in newest] + sweep
    try:
        for i, (topic, q, order) in enumerate(jobs, 1):
            p = dict(part='id', q=q, type='video', maxResults=50, order=order,
                     relevanceLanguage='en', safeSearch='moderate')
            if order == 'date':
                p['publishedAfter'] = since
            for it in call('search', 100, **p).get('items', []):
                found.setdefault(it['id']['videoId'], set()).add(topic)
            if i % 10 == 0:
                print(f'  {i}/{len(jobs)} searches, {len(found)} videos, ~{UNITS} units', file=sys.stderr)
    except QuotaExhausted as e:
        print(f'  stopped searching: {e}; keeping what was found', file=sys.stderr)
    added = 0
    for vid, topics in found.items():
        if vid in seen:
            seen[vid]['topics'] = sorted(set(seen[vid]['topics']) | (topics - {'New'}))
        else:
            seen[vid] = {'topics': sorted(topics - {'New'}), 'first_seen': today, 'pending': True}
            added += 1
    print(f'  {len(jobs)} searches planned, {len(found)} results, {added} not seen before', file=sys.stderr)


def main():
    args = sys.argv[1:]
    seen = load_seen()
    before = len(seen)
    search(args, seen)

    old = {v['id']: v for v in json.load(open(OUT))} if os.path.exists(OUT) else {}
    videos, refreshed, complete = {}, set(), False
    try:
        for chunk in batched(seen):
            for v in call('videos', 1, part='snippet,statistics,contentDetails', id=','.join(chunk)).get('items', []):
                refreshed.add(v['id'])
                sn, st = v['snippet'], v.get('statistics', {})
                text = sn['title'] + ' ' + sn.get('description', '')[:500] + ' ' + ' '.join(sn.get('tags', []))
                lang = (sn.get('defaultAudioLanguage') or sn.get('defaultLanguage') or '').lower()
                if not MACAU.search(text) or (lang and not lang.startswith('en')):
                    seen[v['id']]['rejected'] = True
                    continue
                seen[v['id']].pop('pending', None)
                videos[v['id']] = {
                    'id': v['id'], 'title': sn['title'], 'channel': sn['channelTitle'],
                    'channelId': sn['channelId'], 'published': sn['publishedAt'][:10],
                    'seconds': iso_seconds(v['contentDetails'].get('duration')),
                    'views': int(st.get('viewCount', 0)), 'likes': int(st.get('likeCount', 0)),
                    'comments': int(st.get('commentCount', 0)), 'topics': seen[v['id']]['topics'],
                    'first_seen': seen[v['id']]['first_seen'],
                }
        complete = True
    except QuotaExhausted as e:
        print(f'  stats refresh cut short: {e}; keeping previous stats for the rest', file=sys.stderr)
        for vid, v in old.items():
            if vid not in refreshed:
                videos[vid] = v
    # drop entries that turned out not to be about Macao, and (only after a complete
    # refresh) ones YouTube no longer returns because they were deleted or made private
    for vid in list(seen):
        if seen[vid].get('rejected') or (complete and vid not in refreshed):
            del seen[vid]

    channels = {}
    try:
        for chunk in batched({v['channelId'] for v in videos.values() if 'channelId' in v}):
            for c in call('channels', 1, part='statistics', id=','.join(chunk)).get('items', []):
                st = c.get('statistics', {})
                n = max(int(st.get('videoCount', 1)), 1)
                channels[c['id']] = {'avg': int(st.get('viewCount', 0)) / n,
                                     'subs': int(st.get('subscriberCount', 0)) if not st.get('hiddenSubscriberCount') else None}
    except QuotaExhausted as e:
        print(f'  channel refresh cut short: {e}', file=sys.stderr)

    now = datetime.now(timezone.utc)
    out = []
    for v in videos.values():
        if v['views'] < 1000:
            continue
        ch = channels.get(v.get('channelId'))
        if ch:
            breakout = v['views'] / ch['avg'] if ch['avg'] else 1.0
            subs = ch['subs']
        else:  # keep the previous figures when the channel could not be refreshed
            breakout, subs = v.get('breakout', 1.0), v.get('subs')
        engagement = (v['likes'] + 2 * v['comments']) / v['views']
        age_days = (now - datetime.fromisoformat(v['published']).replace(tzinfo=timezone.utc)).days
        score = (math.log2(1 + breakout) * 2.0 + min(engagement, 0.15) / 0.15 * 2.0
                 + 0.5 ** (age_days / 540) * 1.5 + math.log10(v['views']) * 0.5)
        v.update(breakout=round(breakout, 1), engagement=round(engagement * 100, 2),
                 subs=subs, score=round(score, 2), short=v['seconds'] <= 180)
        out.append(v)
    out.sort(key=lambda v: -v['score'])

    json.dump(seen, open(SEEN, 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
    print(f'catalogue {before} -> {len(seen)} videos; {len(out)} with 1,000+ views written; ~{UNITS} quota units',
          file=sys.stderr)


if __name__ == '__main__':
    main()
