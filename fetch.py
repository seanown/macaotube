"""MacauTube: find English-language YouTube videos about Macau and rank them
for a Western Gen Z / creator audience.

Signals
  breakout   = views / channel's average views per video  (what over-performed)
  engagement = (likes + 2*comments) / views                 (what people loved)
  freshness  = decays with age, half-life ~18 months        (what's current)

Quota (free tier = 10,000 units/day): search.list costs 100, videos.list and
channels.list cost 1 per call of up to 50 ids. A full run uses ~5,000 units.

Usage: YT_KEY=... python3 fetch.py   -> videos.json
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

KEY = os.environ.get('YT_KEY') or sys.exit('Set YT_KEY to your YouTube Data API key.')
API = 'https://www.googleapis.com/youtube/v3/'
HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = 0

# Each query is tagged with the topic it feeds, so the page can filter by topic.
QUERIES = {
    'Travel': ['Macau travel guide', 'things to do in Macau', 'Macau vlog', 'Macau day trip from Hong Kong',
               'Macau first time', 'Macao travel'],
    'Food': ['Macau food', 'Macau street food', 'Macanese food', 'Macau egg tart'],
    'Casinos & hotels': ['Macau casino', 'Macau hotel tour', 'Cotai strip'],
    'History & culture': ['Macau history', 'Macau Portuguese culture', 'Historic Centre of Macao'],
    'Neighbourhoods': ['Taipa village', 'Coloane Macau'],
    'Grand Prix': ['Macau Grand Prix'],
    'Living there': ['living in Macau', 'moving to Macau'],
}
MACAU = re.compile(r'maca[uo]|澳門|澳门|taipa|coloane|cotai', re.I)


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
                sys.exit(f'Daily quota used up after ~{UNITS} units. Rerun tomorrow.')
            if e.code in (400, 403):
                sys.exit(f'YouTube API refused the request ({e.code}): {body[:300]}')
            time.sleep(3 * (i + 1))
    sys.exit('YouTube API kept failing; try again later.')


def search():
    found = {}  # video id -> set of topics
    for topic, qs in QUERIES.items():
        for q in qs:
            for order in ('relevance', 'viewCount'):
                d = call('search', 100, part='id', q=q, type='video', maxResults=50,
                         order=order, relevanceLanguage='en', safeSearch='moderate')
                for it in d.get('items', []):
                    found.setdefault(it['id']['videoId'], set()).add(topic)
        print(f'  searched {topic}: {len(found)} videos so far, ~{UNITS} units', file=sys.stderr)
    return found


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


def main():
    found = search()
    videos = {}
    for chunk in batched(found):
        d = call('videos', 1, part='snippet,statistics,contentDetails', id=','.join(chunk))
        for v in d.get('items', []):
            sn, st = v['snippet'], v.get('statistics', {})
            text = sn['title'] + ' ' + sn.get('description', '')[:500] + ' ' + ' '.join(sn.get('tags', []))
            if not MACAU.search(text):
                continue  # search returned something not actually about Macau
            lang = (sn.get('defaultAudioLanguage') or sn.get('defaultLanguage') or '').lower()
            if lang and not lang.startswith('en'):
                continue
            videos[v['id']] = {
                'id': v['id'], 'title': sn['title'], 'channel': sn['channelTitle'],
                'channelId': sn['channelId'], 'published': sn['publishedAt'][:10],
                'seconds': iso_seconds(v['contentDetails'].get('duration')),
                'views': int(st.get('viewCount', 0)), 'likes': int(st.get('likeCount', 0)),
                'comments': int(st.get('commentCount', 0)), 'topics': sorted(found[v['id']]),
            }
    print(f'  {len(videos)} videos are about Macau and in English (or untagged)', file=sys.stderr)

    channels = {}
    for chunk in batched({v['channelId'] for v in videos.values()}):
        d = call('channels', 1, part='statistics', id=','.join(chunk))
        for c in d.get('items', []):
            st = c.get('statistics', {})
            n = max(int(st.get('videoCount', 1)), 1)
            channels[c['id']] = {'avg': int(st.get('viewCount', 0)) / n,
                                 'subs': int(st.get('subscriberCount', 0)) if not st.get('hiddenSubscriberCount') else None}

    now = datetime.now(timezone.utc)
    out = []
    for v in videos.values():
        if v['views'] < 1000:
            continue
        ch = channels.get(v['channelId'], {'avg': 0, 'subs': None})
        breakout = v['views'] / ch['avg'] if ch['avg'] else 1.0
        engagement = (v['likes'] + 2 * v['comments']) / v['views']
        age_days = (now - datetime.fromisoformat(v['published']).replace(tzinfo=timezone.utc)).days
        freshness = 0.5 ** (age_days / 540)
        score = (math.log2(1 + breakout) * 2.0
                 + min(engagement, 0.15) / 0.15 * 2.0
                 + freshness * 1.5
                 + math.log10(v['views']) * 0.5)
        v.update(breakout=round(breakout, 1), engagement=round(engagement * 100, 2),
                 subs=ch['subs'], score=round(score, 2), short=v['seconds'] <= 180)
        out.append(v)
    out.sort(key=lambda v: -v['score'])
    json.dump(out, open(os.path.join(HERE, 'data', 'videos.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{len(out)} videos ranked; used ~{UNITS} quota units', file=sys.stderr)


if __name__ == '__main__':
    main()
