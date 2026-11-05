"""Merge creator videos (videos.json) and official channel uploads (official.json),
clean, classify by tourism/culture topic, order English first then by views -> ranked.json. No API calls.
"""
import json, math, os, re
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))

IN_TITLE = re.compile(r'maca[uo]|澳門|澳门|taipa|coloane|cotai', re.I)
SPAM = re.compile(r'toto|togel|live draw|keluaran|result macau|data macau|prediksi|'
                  r'national anthem|remix|karaoke|nonstop|songs\b|lagu|bokep|slot gacor|full movie|'
                  r'full action movie|multi-sub', re.I)
# Official channels also post sports and government admin; keep tourism and culture only.
OFF_TOPIC = re.compile(r'體育|运动|運動|足球|籃球|排球|乒乓|羽毛球|游泳|田徑|馬拉松|marathon|錦標賽|championship|'
                       r'全運|運動會|體操|武術|龍舟賽|sport|football|basketball|volleyball|'
                       r'長跑|长跑|賽道|挑戰賽|武林|體質|健康|exercício|saúde|covid|抗原|康碼|財政局|電子服務|政務|報考|'
                       r'交通安排|交通管制|號碼布|冠軍賽|競技|\b10k\b|'
                       r'記者會|新聞發布|招標|招聘|簡介會|說明會|立法|施政|預算|tender|press conference|recruit', re.I)
CJK = re.compile(r'[\u4e00-\u9fff]')
LATIN_WORD = re.compile(r'[A-Za-z]{4,}')
CULTURE = {'Festivals & events', 'Heritage & history', 'Arts & music', 'Traditions & local life', 'Food'}
GP = re.compile(r'格蘭披治|grand prix', re.I)

TOPICS = [  # first match wins; English and Chinese keywords
    ('Grand Prix', r'grand prix|格蘭披治|\bgp\b|\bf3\b|\bfia\b|motorcycle race|racing|guia circuit|賽車'),
    ('Festivals & events', r'festival|節|fireworks|煙花|light up|光影|lunar new year|新春|春節|中秋|carnival|嘉年華|parade|巡遊|'
                           r'celebrat|慶祝|christmas|聖誕|anniversary|creatorweek|創作者大會|expo|博覽|countdown|倒數'),
    ('Food', r'food|\beat\b|eating|egg tart|蛋撻|pork chop|豬扒|restaurant|michelin|dessert|noodle|\bbuns?\b|cuisine|美食|葡國菜|土生菜|餐|'
             r'gastronom|cafe|snack|serradura|treats|asmr|小食|甜品'),
    ('Heritage & history', r'heritage|世遺|世界遺產|history|歷史|portugu|colonial|ruins|大三巴|st\.? paul|a-ma|媽閣|temple|廟|'
                           r'church|教堂|unesco|古蹟|文物|senado|議事亭|lighthouse|燈塔|fortress|炮台|archaeolog|考古'),
    ('Arts & music', r'music|音樂|concert|音樂會|orchestra|樂團|\bart\b|\barts\b|藝術|exhibit|展覽|museum|博物館|theatre|theater|戲劇|'
                     r'dance|舞|opera|粵劇|粉墨|film|電影|photograph|攝影|design|設計|literature|文學|書|painting|畫'),
    ('Traditions & local life', r'tradition|傳統|craft|工藝|非遺|intangible|patuá|patua|土生|macanese|community|社區|neighbourhood|'
                                r'街坊|old street|老街|market|街市|taipa|氹仔|coloane|路環|local|folk|民俗|神誕'),
    ('Casinos & shows', r'casino|gambl|baccarat|poker|jackpot|dancing water|水舞間|venetian|parisian|londoner|wynn|galaxy|'
                        r'city of dreams|studio city|morpheus|cotai|show\b'),
    ('Hotels', r'hotel|resort|酒店|room tour|suite|staycation'),
    ('Getting there', r'ferry|船|bridge|大橋|hong kong to macau|from hong kong|border|口岸|visa|airport|機場|turbojet|how to get'),
    ('Living there', r'living in|live in|moving to|expat|cost of living|salary|work in|life in|apartment|rent'),
]
TOPIC_RE = [(t, re.compile(p, re.I)) for t, p in TOPICS]


def topic(title):
    for t, rx in TOPIC_RE:
        if rx.search(title):
            return t
    return 'Travel & sights'


def main():
    creators = json.load(open(os.path.join(HERE, 'data', 'videos.json')))
    for v in creators:
        v.setdefault('lang', 'English')
        v.setdefault('official', False)
    official = json.load(open(os.path.join(HERE, 'data', 'official.json')))

    now = datetime.now(timezone.utc)
    seen, out, dropped = set(), [], {'not about Macau': 0, 'spam': 0, 'sports/admin': 0, 'too few views': 0}
    for v in official + creators:  # official first, so its record wins on duplicates
        if v['id'] in seen:
            continue
        seen.add(v['id'])
        t = v['title']
        if v['official']:
            if OFF_TOPIC.search(t + ' ' + v.get('desc', '')[:120]) and not GP.search(t):
                dropped['sports/admin'] += 1
                continue
            if v['views'] < 300:
                dropped['too few views'] += 1
                continue
            # the culture-and-sports bureau is mostly sports and public services
            if v['channel'].startswith('DSCD') and topic(t) not in CULTURE:
                dropped['sports/admin'] += 1
                continue
        else:
            if not IN_TITLE.search(t):
                dropped['not about Macau'] += 1
                continue
            if SPAM.search(t):
                dropped['spam'] += 1
                continue
        # YouTube's API policies require stored data to be refreshed within 30 days.
        fetched = datetime.fromisoformat(v.get('fetched') or now.date().isoformat()).replace(tzinfo=timezone.utc)
        if (now - fetched).days > 30:
            dropped['stale'] = dropped.get('stale', 0) + 1
            continue
        v['topic'] = topic(t)
        v['short'] = v['seconds'] <= 180
        if v['official'] and v['topic'] == 'Travel & sights' and v['channel'].startswith('澳門文化局'):
            v['topic'] = 'Arts & music'
        # Language follows the title text: a channel's default language is often wrong.
        if CJK.search(t) and not LATIN_WORD.search(t):
            v['lang'] = 'Chinese'
        # English-first ordering uses our own language label, not a YouTube-derived metric.
        v['tier'] = 0 if v.get('lang') == 'English' else 1
        for k in ('topics', 'desc', 'channelId', 'likes', 'comments', 'breakout', 'engagement', 'subs', 'score'):
            v.pop(k, None)
        out.append(v)
    out.sort(key=lambda v: (v['tier'], -v['views']))
    json.dump(out, open(os.path.join(HERE, 'data', 'ranked.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{len(out)} kept ({sum(v["official"] for v in out)} official); dropped {dropped}')


if __name__ == '__main__':
    main()
