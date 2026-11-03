"""Pull every upload from Macau's official tourism and culture channels -> official.json

Uses playlistItems (1 unit / 50 videos) instead of search, so the whole
back catalogue costs ~150 quota units.
"""
import json, os, re, sys, urllib.parse, urllib.request
from fetch import call, batched, iso_seconds

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNELS = {
    'UC0gaccizp0Mm85hxiqE56pw': 'Macao Government Tourism Office',
    'UCCunZAif3rudh3umgTbeVKQ': 'Macao Government Tourism Office - USA',
    'UCdz25Xumze9M7bG9cpgNQvg': '澳門文化局 IC Macao',
    'UC27c-K4kt8Zt5RzWZc7d7JA': 'DSCD 文化體育局',
}
CJK = re.compile(r'[一-鿿]')
PT = re.compile(r'\b(de|da|do|em|para|com|e|o|a)\b.*\b(cultura|turismo|festival|museu|macau)\b', re.I)


def language(sn):
    tag = (sn.get('defaultAudioLanguage') or sn.get('defaultLanguage') or '').lower()
    if tag.startswith('zh') or tag.startswith('yue'):
        return 'Chinese'
    if tag.startswith('pt'):
        return 'Portuguese'
    if tag.startswith('en'):
        return 'English'
    t = sn['title']
    if CJK.search(t):
        # bilingual titles like "澳門美食 Macao Food" count as both
        return 'Bilingual' if re.search(r'[A-Za-z]{4,}', t) else 'Chinese'
    return 'Portuguese' if PT.search(t) else 'English'


def main():
    ch = call('channels', 1, part='contentDetails,statistics', id=','.join(CHANNELS))
    uploads, avg = {}, {}
    for c in ch['items']:
        uploads[c['id']] = c['contentDetails']['relatedPlaylists']['uploads']
        st = c['statistics']
        avg[c['id']] = int(st.get('viewCount', 0)) / max(int(st.get('videoCount', 1)), 1)

    ids = []
    for cid, pl in uploads.items():
        token, n = None, 0
        while True:
            p = dict(part='contentDetails', playlistId=pl, maxResults=50)
            if token:
                p['pageToken'] = token
            d = call('playlistItems', 1, **p)
            ids += [(it['contentDetails']['videoId'], cid) for it in d.get('items', [])]
            n += len(d.get('items', []))
            token = d.get('nextPageToken')
            if not token:
                break
        print(f'  {CHANNELS[cid]}: {n} uploads', file=sys.stderr)

    owner = dict(ids)
    out = []
    for chunk in batched(owner):
        d = call('videos', 1, part='snippet,statistics,contentDetails', id=','.join(chunk))
        for v in d.get('items', []):
            sn, st = v['snippet'], v.get('statistics', {})
            views = int(st.get('viewCount', 0))
            cid = owner[v['id']]
            out.append({
                'id': v['id'], 'title': sn['title'], 'channel': CHANNELS[cid], 'channelId': cid,
                'published': sn['publishedAt'][:10], 'seconds': iso_seconds(v['contentDetails'].get('duration')),
                'views': views, 'likes': int(st.get('likeCount', 0)), 'comments': int(st.get('commentCount', 0)),
                'breakout': round(views / avg[cid], 1) if avg[cid] else 1.0,
                'engagement': round((int(st.get('likeCount', 0)) + 2 * int(st.get('commentCount', 0))) / views * 100, 2) if views else 0,
                'subs': None, 'lang': language(sn), 'official': True,
                'desc': sn.get('description', '')[:300],
            })
    json.dump(out, open(os.path.join(HERE, 'data', 'official.json'), 'w'), ensure_ascii=False, indent=1)
    from fetch import UNITS
    print(f'{len(out)} official videos saved', file=sys.stderr)


if __name__ == '__main__':
    main()
