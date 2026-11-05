"""Tell search engines that support IndexNow (Bing, Yandex, Seznam, Naver and
others) that macaotube.org's pages changed. Run after each deploy.

The key is public by design: search engines check that https://macaotube.org/<key>.txt
contains it, which proves the site owner sent the ping. Google does not use
IndexNow; it reads sitemap.xml through Search Console instead.
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = open(os.path.join(HERE, 'indexnow_key.txt')).read().strip()
try:  # the live sitemap after deploy; fall back to the local build
    with urllib.request.urlopen('https://macaotube.org/sitemap.xml', timeout=30) as r:
        urls = re.findall(r'<loc>([^<]+)</loc>', r.read().decode())
except Exception:
    urls = [u for u in open(os.path.join(HERE, 'site', 'urls.txt')).read().split() if u]
body = json.dumps({'host': 'macaotube.org', 'key': KEY,
                   'keyLocation': f'https://macaotube.org/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, method='POST',
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f'IndexNow: {r.status} for {len(urls)} URLs')
except urllib.error.HTTPError as e:
    # 202 = accepted, 422/403 usually mean the key file is not live yet; never fail the deploy over this
    print(f'IndexNow: HTTP {e.code} {e.read()[:200]!r}', file=sys.stderr)
except Exception as e:
    print(f'IndexNow: {e}', file=sys.stderr)
