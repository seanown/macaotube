"""Inject data/ranked.json into template.html -> site/index.html (a standalone web page)."""
import json, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'data', 'ranked.json')))
keep = ['id', 'title', 'channel', 'published', 'seconds', 'views', 'subs', 'breakout',
        'engagement', 'score', 'short', 'topic', 'lang', 'official']
slim = [{k: r[k] for k in keep} for r in rows]

body = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
body = body.replace('/*DATA*/[]', json.dumps(slim, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
body = body.replace('/*BUILT*/', dt.date.today().isoformat())
assert 'AIza' not in body, 'API key must never reach the published page'

html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Discover and Visit Macao: the best of Macao tourism and culture on YouTube, '
        'from official channels and independent creators. Sponsored by GBAECA.org.">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

os.makedirs(os.path.join(HERE, 'site'), exist_ok=True)
open(os.path.join(HERE, 'site', 'index.html'), 'w', encoding='utf-8').write(html)
print(len(slim), 'videos -> site/index.html')
