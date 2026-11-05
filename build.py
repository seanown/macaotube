"""Build macaotube.org into site/: one real, crawlable page per section and topic.

Every list page carries its first 48 videos as plain HTML (so search engines and
link previews see real content), plus a small script that loads /videos.json for
filters, search and "Show more".

Output
  site/index.html, site/videos/, site/shorts/, site/official/, site/creators/,
  site/topics/ (directory) and site/topics/<slug>/, site/about/, site/later/,
  site/404.html, site/videos.json, site/sitemap.xml, site/robots.txt, site/urls.txt
  plus everything in static/ (icons, preview image, logo, IndexNow key).
"""
import datetime as dt, html, json, os, shutil
from pages import SITE, NAME, TOPICS, SECTIONS, EVENTS, PACKAGES, PARTNER_EMAIL, SPONSORS, topic_path

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
# Google Analytics 4 Measurement ID (public, safe to commit). Empty = no analytics.
GA_ID = 'G-LDG73TDR2R'
# Baidu Tongji site code: the 32 characters after 'hm.js?'. Empty = no Baidu Tongji.
BAIDU_ID = 'b844c9f0bbbb22e5a149c38476c4cdf4'
PAGE_SIZE = 48
TODAY = dt.date.today()
BUILT = TODAY.isoformat()

E = lambda s: html.escape(str(s), quote=True)
KEEP = ['id', 'title', 'channel', 'published', 'seconds', 'views', 'tier', 'short', 'topic', 'lang', 'official']
DATA = [{k: r[k] for k in KEEP} for r in json.load(open(os.path.join(HERE, 'data', 'ranked.json')))]
DATA.sort(key=lambda v: (v['tier'], -v['views']))  # English first, then most viewed
assert 'AIza' not in json.dumps(DATA), 'API key must never reach the published site'
TOPIC_ORDER = sorted(TOPICS, key=lambda t: -sum(v['topic'] == t for v in DATA))


# ---------------------------------------------------------------- formatting (mirrors the page script)
def fmt_n(n):
    """1234 -> 1.2K, 56789 -> 57K, 1234567 -> 1.2M, 12345678 -> 12M"""
    for div, suf in ((1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if n >= div:
            x = n / div
            s = f'{x:.1f}' if (suf == 'B' or n < div * 10) else f'{x:.0f}'
            return s.removesuffix('.0') + suf
    return str(n)


def dur(s):
    h, m, x = s // 3600, s % 3600 // 60, s % 60
    return f'{h}:{m:02d}:{x:02d}' if h else f'{m}:{x:02d}'


def ago(d):
    days = (TODAY - dt.date.fromisoformat(d)).days
    if days < 1:
        return 'today'
    n, u = (days, 'day') if days < 30 else (int(days / 30.4), 'month') if days < 365 else (int(days / 365.25), 'year')
    return f"{n} {u}{'' if n == 1 else 's'} ago"


def yt_url(v):
    return f"https://www.youtube.com/{'shorts/' if v['short'] else 'watch?v='}{v['id']}"


ICON_CHECK = '<svg viewBox="0 0 24 24" aria-label="Official channel"><path d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20zm-1.2 13.4l5.6-5.6-1.4-1.4-4.2 4.2-2-2-1.4 1.4z"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20zm0 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16zm1 3v4.6l3.6 2.1-1 1.7L11 12.7V7z"/></svg>'
ICON_FILTER = '<svg viewBox="0 0 24 24"><path d="M3 6h10v2H3zm14 0h4v2h-4zm-2-2h2v6h-2zM3 16h4v2H3zm8 0h10v2H11zm-2-2h2v6H9z"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 1 7 7c0 5-7 13-7 13S5 14 5 9a7 7 0 0 1 7-7zm0 4.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z"/></svg>'


def card(v):
    href = yt_url(v)
    img = f"https://i.ytimg.com/vi/{v['id']}/{'hqdefault' if v['short'] else 'mqdefault'}.jpg"
    bo = ''
    lang = {'Chinese': '<span class="lang">中文</span>', 'Portuguese': '<span class="lang">PT</span>'}.get(v['lang'], '')
    return f"""<article class="card">
      <a class="thumb" href="{href}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
        <img src="{img}" alt="" width="320" height="180" loading="lazy" decoding="async" onerror="this.remove()">
        <span class="dur">{dur(v['seconds'])}</span>
      </a>
      <button class="later" data-id="{v['id']}" aria-pressed="false" aria-label="Save to Watch later">{ICON_CLOCK}</button>
      <div class="info">
        <h3 class="title"><a href="{href}" target="_blank" rel="noopener" title="{E(v['title'])}">{E(v['title'])}</a></h3>
        <div class="ch">{ICON_CHECK if v['official'] else ''}<span>{E(v['channel'])}</span>{lang}</div>
        <div class="stats">{fmt_n(v['views'])} views • {ago(v['published'])}{bo}</div>
      </div>
    </article>"""


def select(base):
    return [v for v in DATA
            if (base.get('format') != 'long' or not v['short']) and (base.get('format') != 'short' or v['short'])
            and (base.get('src') != 'official' or v['official']) and (base.get('src') != 'creators' or not v['official'])
            and (not base.get('topic') or v['topic'] == base['topic'])]


def topic_chips(current=None, n=8):
    chosen = TOPIC_ORDER if current else TOPIC_ORDER[:n]
    return ''.join(f'<a class="chip" href="{topic_path(t)}"{" aria-current=\"page\"" if t == current else ""}>{E(t)}</a>'
                   for t in chosen)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'


PUBLISHER = {'@type': 'Organization',
             'name': 'Guangdong-Hong Kong-Macao Greater Bay Area Electronic Commerce Association (GBAECA)',
             'url': 'https://gbaeca.org', 'logo': f'{SITE}/gbaeca-logo.png'}


def item_list(videos, n=20):
    return {'@type': 'ItemList', 'numberOfItems': len(videos), 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'url': yt_url(v), 'name': v['title']} for i, v in enumerate(videos[:n])]}



# ---------------------------------------------------------------- events
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def fmt_range(a, b, short=False):
    a, b = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
    m = (lambda d: MONTHS[d.month - 1][:3]) if short else (lambda d: MONTHS[d.month - 1])
    yr = '' if short else f' {b.year}'
    if a == b:
        return f'{a.day} {m(a)}{yr}'
    if (a.year, a.month) == (b.year, b.month):
        return f'{a.day}–{b.day} {m(b)}{yr}'
    return f"{a.day} {m(a)}{'' if short or a.year == b.year else f' {a.year}'} – {b.day} {m(b)}{yr}"


def upcoming():
    out = []
    for e in EVENTS:
        last = dt.date.fromisoformat(e['end']) if 'end' in e else dt.date.fromisoformat(e['sort']) + dt.timedelta(days=31)
        if last >= TODAY:
            first = dt.date.fromisoformat(e.get('start', e.get('sort')))
            out.append(dict(e, _first=first, _last=last, _now='start' in e and first <= TODAY <= last))
    return sorted(out, key=lambda e: e['_first'])


def when(e, short=False):
    return fmt_range(e['start'], e['end'], short) if 'start' in e else e['when']


def coming_up_strip(n=3, days=45):
    soon = [e for e in upcoming() if 'start' in e and (e['_first'] - TODAY).days <= days][:n]
    if not soon:
        return ''
    items = ' · '.join(f'<a href="{E(e["link"])}">{E(e["name"])}</a> <span>{"now on" if e["_now"] else when(e, short=True)}</span>' for e in soon)
    return f'<p class="soon"><b>Coming up</b> {items} · <a href="/whats-on/">What\'s on →</a></p>'



def sponsor_line(path):
    sp = SPONSORS.get(path)
    if not sp:
        return ''
    line = f' · {E(sp["line"])}' if sp.get('line') else ''
    return (f'<p class="sponsor"><span class="tag">Sponsored</span> Presented by '
            f'<a href="{E(sp["url"])}" target="_blank" rel="sponsored noopener">{E(sp["name"])}</a>{line}</p>')

# ---------------------------------------------------------------- page shell
STYLE, BODY = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read().split('<!--BODY-->')
COUNTS = {'N_VIDEOS': fmt_n(sum(not v['short'] for v in DATA)), 'N_SHORTS': fmt_n(sum(v['short'] for v in DATA)),
          'N_OFFICIAL': fmt_n(sum(v['official'] for v in DATA)), 'N_CREATORS': fmt_n(sum(not v['official'] for v in DATA))}
RAIL_TOPICS = ''.join(
    f'<a href="{topic_path(t)}" data-r="topic:{E(t)}" class="topic">{ICON_PIN}{E(t)}'
    f'<span class="n">{fmt_n(sum(v["topic"] == t for v in DATA))}</span></a>'
    for t in TOPIC_ORDER[:7])


def analytics():
    out = ''
    if GA_ID:
        out += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
                "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n")
    if BAIDU_ID:
        assert len(BAIDU_ID) == 32 and BAIDU_ID.isalnum(), 'BAIDU_ID should be the 32-character code after hm.js?'
        out += ('<script>var _hmt=_hmt||[];(function(){var hm=document.createElement("script");'
                f'hm.src="https://hm.baidu.com/hm.js?{BAIDU_ID}";var s=document.getElementsByTagName("script")[0];'
                's.parentNode.insertBefore(hm,s);})();</script>\n')
    return out


def page(path, *, title, description, view_html, rail_key, page_js=None, ld=None, index=True):
    full_title = title if title.startswith(NAME) else f'{title} | {NAME}'
    url = SITE + path
    lds = ''.join(jsonld(x) for x in (ld if isinstance(ld, list) else [ld] if ld else []))
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
{f'<link rel="canonical" href="{url}">' if index else '<meta name="robots" content="noindex, follow">'}
<meta name="theme-color" content="#00785e">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="MacaoTube: Discover and Visit Macao">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(full_title)}">
<meta name="twitter:description" content="{E(description)}">
<meta name="twitter:image" content="{SITE}/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://i.ytimg.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap">
{analytics()}{lds}{STYLE}
</head>
<body>
"""
    body = BODY.replace('%%VIEW%%', view_html).replace('%%RAIL_TOPICS%%', RAIL_TOPICS)
    for k, val in COUNTS.items():
        body = body.replace(f'%%{k}%%', val)
    if rail_key:
        body = body.replace(f'data-r="{E(rail_key)}"', f'data-r="{E(rail_key)}" aria-current="page"', 1)
    js = dict(page_js or {'view': 'static'}, title=full_title, built=BUILT)
    body = body.replace('/*PAGE*/{}', json.dumps(js, ensure_ascii=False).replace('</', '<\\/'))
    target = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
    return url if index else None


def list_view(videos, head_html, chips, shorts=False):
    grid = '\n    '.join(card(v) for v in videos[:PAGE_SIZE])
    return f"""    <div class="head" id="head">{head_html}</div>
    <div class="bar" id="bar"><button class="chip" id="filters" aria-expanded="false" aria-controls="panel">{ICON_FILTER}Filters</button>{chips}</div>
    <div class="panel" id="panel" hidden></div>
    <div class="grid{' shorts' if shorts else ''}" id="grid">
    {grid}
    </div>
    <button class="more" id="more" hidden>Show more</button>"""


# ---------------------------------------------------------------- build
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
shutil.copytree(os.path.join(HERE, 'static'), OUT)
json.dump(DATA, open(os.path.join(OUT, 'videos.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
urls = []

# section pages: home, videos, shorts, official, creators
for key, s in SECTIONS.items():
    vids = select(s['base'])
    count = '' if key == 'home' else f'<span class="count">{len(vids):,} videos</span>'
    head = f'<h1>{E(s["h1"])}</h1><p class="intro">{E(s["intro"])}</p>{count}'
    if key == 'home':
        head += coming_up_strip()
    head += sponsor_line(s['path'])
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': s['title'], 'url': SITE + s['path'],
           'description': s['description'], 'inLanguage': 'en', 'about': {'@type': 'Place', 'name': 'Macao'},
           'isPartOf': {'@type': 'WebSite', 'name': NAME, 'url': SITE + '/'}, 'mainEntity': item_list(vids)}]
    if key == 'home':
        ld.insert(0, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'alternateName': 'Macao Tube',
                      'url': SITE + '/', 'description': s['description'], 'inLanguage': 'en', 'publisher': PUBLISHER,
                      'potentialAction': {'@type': 'SearchAction',
                                          'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + '/?q={search_term_string}'},
                                          'query-input': 'required name=search_term_string'}})
    chips = topic_chips()
    urls.append(page(s['path'], title=s['title'], description=s['description'], rail_key=key, ld=ld,
                     view_html=list_view(vids, head, chips, shorts=key == 'shorts'),
                     page_js={'view': 'list', 'base': s['base'], 'shown': min(PAGE_SIZE, len(vids)), 'chips': chips}))

# topic pages
for t in TOPIC_ORDER:
    m, path = TOPICS[t], topic_path(t)
    vids = select({'topic': t})
    head = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span>'
            '<a href="/topics/">Topics</a></nav>'
            f'<h1>{E(t)}</h1><p class="intro">{E(m["intro"])}</p><span class="count">{len(vids):,} videos</span>')
    head += sponsor_line(path)
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': m['title'], 'url': SITE + path,
           'description': m['description'], 'inLanguage': 'en', 'about': {'@type': 'Place', 'name': 'Macao'},
           'isPartOf': {'@type': 'WebSite', 'name': NAME, 'url': SITE + '/'}, 'mainEntity': item_list(vids)},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
              {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
              {'@type': 'ListItem', 'position': 2, 'name': 'Topics', 'item': SITE + '/topics/'},
              {'@type': 'ListItem', 'position': 3, 'name': t, 'item': SITE + path}]}]
    chips = topic_chips(current=t)
    urls.append(page(path, title=m['title'], description=m['description'], rail_key=f'topic:{t}', ld=ld,
                     view_html=list_view(vids, head, chips),
                     page_js={'view': 'list', 'base': {'topic': t}, 'shown': min(PAGE_SIZE, len(vids)), 'chips': chips}))

# topic directory
mx = max(sum(v['topic'] == t for v in DATA) for t in TOPIC_ORDER)
cards = []
for t in TOPIC_ORDER:
    vs, p = [v for v in DATA if v['topic'] == t], topic_path(t)
    sub = [('In English', sum(v['lang'] == 'English' for v in vs), '?lang=English'),
           ('Past year', sum((TODAY - dt.date.fromisoformat(v['published'])).days < 366 for v in vs), '?date=year'),
           ('Most viewed', len(vs), '?sort=views'), ('Newest first', len(vs), '?sort=new')]
    rows_html = ''.join(f'<a class="row" href="{p}{q}">{lab}<span>{n:,}</span></a>' for lab, n, q in sub if n)
    blurb = TOPICS[t]['intro'].split('. ')[0].rstrip('.') + '.'
    cards.append(f"""<section class="cat">
      <h2><a href="{p}">{E(t)}</a><span>{len(vs):,}</span></h2>
      <div class="bar2"><i style="width:{len(vs) / mx * 100:.0f}%"></i></div>
      <p>{E(blurb)}</p>
      {rows_html}
    </section>""")
directory = (f'    <div class="head"><h1>Explore Macao by topic</h1><p class="intro">{len(TOPIC_ORDER)} topics and {len(DATA):,} videos, '
             'from the Grand Prix and Macanese food to festivals, heritage and life in the city.</p></div>\n'
             f'    <div class="cats">{"".join(cards)}</div>')
urls.append(page('/topics/', title='Macau Video Topics: Food, Festivals, Heritage, Grand Prix and More',
                 description='Browse the most-watched YouTube videos about Macao by topic: travel, food, festivals, heritage, arts, local life, casinos and shows, the Grand Prix and more.',
                 view_html=directory, rail_key='topics',
                 ld={'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Macao video topics', 'url': SITE + '/topics/',
                     'hasPart': [{'@type': 'CollectionPage', 'name': t, 'url': SITE + topic_path(t)} for t in TOPIC_ORDER]}))

# what's on
evs = upcoming()
ev_cards, ev_ld = [], []
for e in evs:
    status = ('<span class="now">On now</span>' if e['_now'] else '<span class="tbc">Provisional dates</span>' if e.get('provisional')
              else '' if 'start' in e else '<span class="tbc">Dates to be confirmed</span>')
    ev_cards.append(f"""<article class="event">
      <div class="when">{E(when(e))}{status}</div>
      <div class="what">
        <h2>{E(e['name'])}</h2>
        <p class="where">{E(e['where'])}</p>
        <p>{E(e['what'])}</p>
        <a class="watch" href="{E(e['link'])}">Watch videos →</a>
      </div>
    </article>""")
    if 'start' in e:
        ev_ld.append({'@context': 'https://schema.org', '@type': 'Event', 'name': e['name'], 'startDate': e['start'], 'endDate': e['end'],
                      'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
                      'description': e['what'],
                      'location': {'@type': 'Place', 'name': e['where'], 'address': {'@type': 'PostalAddress', 'addressLocality': 'Macao', 'addressCountry': 'MO'}}})
whats_on = (f'    <div class="head"><h1>What\'s on in Macao</h1><p class="intro">Festivals, races and celebrations coming up in Macao, '
            'with the videos to watch before you go. Where this season\'s dates have not been announced yet, we show the usual timing. '
            'Always check the organiser\'s official site before you travel.</p></div>\n'
            f'    <div class="events">{"".join(ev_cards)}</div>')
urls.append(page('/whats-on/', title="What's On in Macau: Festivals and Events Calendar",
                 description='Upcoming festivals and events in Macao: the Grand Prix, the Food Festival, Light Up Macao, Chinese New Year, the fireworks contest and more, with videos of each.',
                 view_html=whats_on, rail_key='whats-on',
                 ld=[{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': "What's on in Macao", 'url': SITE + '/whats-on/'}] + ev_ld))

# partner page
pk_cards = ''.join(f"""<section class="pkg">
      <h2>{E(k['name'])}</h2>
      <p class="note">{E(k['note'])}</p>
      <p class="price"><b>{E(k['price'])}</b> <span>{E(k['per'])}</span></p>
      <ul>{''.join(f'<li>{E(g)}</li>' for g in k['gets'])}</ul>
    </section>""" for k in PACKAGES)
partner_html = f"""    <article class="prose wide">
      <header>
        <h1>Partner with MacaoTube</h1>
        <p class="lede">Put your business in front of English-speaking travellers while they plan a trip to Macao. MacaoTube is a new, free guide to the most-watched YouTube videos about Macao, refreshed every day, with {len(DATA):,} videos across {len(TOPIC_ORDER)} topics.</p>
      </header>
      <div class="pkgs">{pk_cards}</div>
      <section>
        <h2>Our promise to viewers</h2>
        <p>Sponsors never change which videos are shown or in what order. Every paid placement is labelled <b>Sponsored</b>, and each page carries at most one sponsor. Trust is what makes MacaoTube worth sponsoring, so we protect it.</p>
      </section>
      <section>
        <h2>Get in touch</h2>
        <p>Email <a href="mailto:{PARTNER_EMAIL}?subject=Partnering%20with%20MacaoTube">{PARTNER_EMAIL}</a> with your business name and the package you are interested in. We reply in English or Chinese, usually within a day. Prices are in Macao patacas; US$1 is about MOP 8.</p>
      </section>
    </article>"""
urls.append(page('/partner/', title='Partner with MacaoTube: Sponsorship for Macao Businesses',
                 description='Sponsor MacaoTube and reach English-speaking travellers planning a trip to Macao: founding partner, season sponsor and business video page packages.',
                 view_html=partner_html, rail_key='partner',
                 ld={'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Partner with MacaoTube', 'url': SITE + '/partner/', 'publisher': PUBLISHER}))

# privacy
privacy_html = """    <article class="prose">
      <header>
        <h1>Privacy</h1>
        <p class="lede">MacaoTube is a free website that lists YouTube videos about Macao. It has no accounts or sign-ups and asks you for no personal information.</p>
      </header>
      <section>
        <h2>YouTube API Services</h2>
        <p>MacaoTube uses YouTube API Services to show video titles, thumbnails, channel names and view counts. We only read public video information; we never access your YouTube or Google account. When you play a video you go to YouTube, where the <a href="https://www.youtube.com/t/terms" target="_blank" rel="noopener">YouTube Terms of Service</a> and the <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a> apply. By using MacaoTube you agree to the YouTube Terms of Service.</p>
      </section>
      <section>
        <h2>What your browser loads from others</h2>
        <p>Video thumbnails load from YouTube's image servers, and the typeface loads from Google Fonts. Like any website, those servers receive your IP address and browser details when your browser fetches them.</p>
      </section>
      <section>
        <h2>Visitor statistics</h2>
        <p>We use Google Analytics and Baidu Tongji to count visits and see which pages are useful. They set cookies and record things like the pages you view, your device type and your approximate location. We use these numbers only in aggregate, to improve the site, and we do not sell them. You can block these cookies in your browser settings without losing any feature of MacaoTube.</p>
      </section>
      <section>
        <h2>Watch later</h2>
        <p>Videos you save to Watch later are stored only in your own browser, on your device. They are never sent to us. Clearing your browser data removes them.</p>
      </section>
      <section>
        <h2>Email</h2>
        <p>If you email us, we use your message and address only to reply and to follow up on what you asked about. Contact: <a href="mailto:hello@macaotube.org">hello@macaotube.org</a>; for sponsorship, <a href="mailto:partners@macaotube.org">partners@macaotube.org</a>.</p>
      </section>
      <p class="fine">Last updated 5 November 2026.</p>
    </article>"""
urls.append(page('/privacy/', title='Privacy', description='How MacaoTube handles data: YouTube API Services, visitor statistics, Watch later and email.',
                 view_html=privacy_html, rail_key='privacy',
                 ld={'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'MacaoTube privacy', 'url': SITE + '/privacy/', 'publisher': PUBLISHER}))

# about
n_ch = len({v['channel'] for v in DATA})
about = f"""    <article class="prose">
      <header>
        <h1>Discover and Visit Macao</h1>
        <p class="lede">MacaoTube gathers the most-watched YouTube videos about Macao in one place, sorted by topic: its festivals, heritage, food, neighbourhoods and nightlife, from the city's official channels and from the travellers and creators people actually watch.</p>
      </header>
      <section>
        <h2>How it works</h2>
        <p>Every night MacaoTube collects the latest uploads from Macao's official tourism and culture channels and searches YouTube for English-language videos about the city. Right now that is {len(DATA):,} videos from {n_ch:,} channels, {sum(v['official'] for v in DATA):,} of them official.</p>
        <p>Pages list English-language videos first, then videos in Chinese and Portuguese, each group ordered by YouTube view count. You can also sort by upload date. View counts, titles and thumbnails come from YouTube and are refreshed every night. Sports, public notices and spam are left out. Shorts are videos of three minutes or less.</p>
      </section>
      <section>
        <h2>Explore</h2>
        <div class="topiclinks">{topic_chips(n=len(TOPIC_ORDER))}</div>
      </section>
      <section>
        <h2>Who's behind it</h2>
        <p>MacaoTube is curated by <a href="https://ownsean.com" target="_blank" rel="noopener">Sean Own</a>, a Macao entrepreneur, investor and curator, and is a GBAECA initiative.</p>
        <div class="org">
          <a href="https://gbaeca.org" target="_blank" rel="noopener"><img src="/gbaeca-logo.png" width="96" height="96" alt="Logo of the Guangdong-Hong Kong-Macao Greater Bay Area Electronic Commerce Association"></a>
          <div><p>The <a href="https://gbaeca.org" target="_blank" rel="noopener">Guangdong-Hong Kong-Macao Greater Bay Area Electronic Commerce Association</a> (GBAECA) is a non-profit founded in Macao in 2019. It helps businesses grow e-commerce and cross-border trade across the Greater Bay Area.</p></div>
        </div>
      </section>
      <section>
        <h2>More from Sean Own</h2>
        <div class="sites">
          <a href="https://ownsean.com" target="_blank" rel="noopener"><b>Sean Own</b><span>Projects, ventures and media, in English.</span><span class="u">ownsean.com</span></a>
          <a href="https://seanown.org" target="_blank" rel="noopener"><b>翁振軒 Sean Own</b><span>Writing on AI, culture and industry from Macao, in Chinese.</span><span class="u">seanown.org</span></a>
          <a href="https://gbaeca.org" target="_blank" rel="noopener"><b>GBAECA</b><span>The Greater Bay Area Electronic Commerce Association, in Chinese.</span><span class="u">gbaeca.org</span></a>
        </div>
      </section>
      <p class="fine">Last refreshed {BUILT}. Videos remain on YouTube and belong to their creators; MacaoTube only links to them.</p>
    </article>"""
urls.append(page('/about/', title='About MacaoTube',
                 description='How MacaoTube finds and sorts YouTube videos about Macao, and who is behind it.',
                 view_html=about, rail_key='about',
                 ld={'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About MacaoTube',
                     'url': SITE + '/about/', 'publisher': PUBLISHER}))

# watch later (personal, not indexed)
page('/later/', title='Watch later', description='Videos you saved on this device.', rail_key='later', index=False,
     view_html=list_view([], '<h1>Watch later</h1><span class="count">Saved in this browser only</span>', ''),
     page_js={'view': 'later', 'base': {}, 'shown': 0, 'chips': ''})

# 404
notfound = """    <article class="prose">
      <header><h1>That page isn't here</h1><p class="lede">The link may be old or mistyped. Try one of these instead, or search above.</p></header>
      <div class="topiclinks"><a class="chip" href="/">Home</a>""" + topic_chips(n=len(TOPIC_ORDER)) + """</div>
    </article>"""
page('/404.html', title='Page not found', description='This page could not be found.', view_html=notfound, rail_key='', index=False)

# sitemap, robots, url list (for IndexNow)
urls = [u for u in urls if u]
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc><lastmod>{BUILT}</lastmod><changefreq>daily</changefreq></url>\n' for u in urls)
    + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /later/\n\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(OUT, 'urls.txt'), 'w').write('\n'.join(urls) + '\n')
print(f'{len(DATA)} videos, {len(urls)} indexable pages -> site/')
