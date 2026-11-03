"""Inject data/ranked.json into template.html -> site/index.html (a standalone web page)."""
import json, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
# Google Analytics 4 Measurement ID (public, safe to commit). Empty = no analytics.
GA_ID = 'G-LDG73TDR2R'
# Baidu Tongji site code: the 32 characters after 'hm.js?'. Empty = no Baidu Tongji.
BAIDU_ID = ''
rows = json.load(open(os.path.join(HERE, 'data', 'ranked.json')))
keep = ['id', 'title', 'channel', 'published', 'seconds', 'views', 'subs', 'breakout',
        'engagement', 'score', 'short', 'topic', 'lang', 'official']
slim = [{k: r[k] for k in keep} for r in rows]

body = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
body = body.replace('/*DATA*/[]', json.dumps(slim, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
body = body.replace('/*BUILT*/', dt.date.today().isoformat())
assert 'AIza' not in body, 'API key must never reach the published page'

ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
      f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
      f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n") if GA_ID else ''

if BAIDU_ID:
    assert len(BAIDU_ID) == 32 and BAIDU_ID.isalnum(), 'BAIDU_ID should be the 32-character code after hm.js?'
    ga += (f'<script>var _hmt=_hmt||[];(function(){{var hm=document.createElement("script");'
           f'hm.src="https://hm.baidu.com/hm.js?{BAIDU_ID}";var s=document.getElementsByTagName("script")[0];'
           f's.parentNode.insertBefore(hm,s);}})();</script>\n')

html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Discover and Visit Macao: the best of Macao tourism and culture on YouTube, '
        'from official channels and independent creators. Curated by Sean Own, a GBAECA initiative.">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + ga +
        '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

os.makedirs(os.path.join(HERE, 'site'), exist_ok=True)
import shutil
for asset in ('gbaeca-logo.png',):
    shutil.copy(os.path.join(HERE, asset), os.path.join(HERE, 'site', asset))
open(os.path.join(HERE, 'site', 'index.html'), 'w', encoding='utf-8').write(html)
print(len(slim), 'videos -> site/index.html')
