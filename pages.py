"""Page definitions for macaotube.org: URLs, titles, search descriptions and the
short written guides shown on each topic page.

Titles use "Macau" (the spelling most English speakers search for); body text
uses "Macao" (the official English spelling). Keep guide text factual and
check any new claim against an official source before adding it.
"""

SITE = 'https://macaotube.org'
NAME = 'MacaoTube'
TAGLINE = 'Discover and Visit Macao'

# Topic name (as produced by rerank.py) -> page
TOPICS = {
    'Travel & sights': {
        'slug': 'travel',
        'title': 'Macau Travel Videos: Things to Do, Sights and City Guides',
        'description': 'The most-watched Macau travel guides, walking tours and vlogs: what to see, where to go and how Macao feels, updated daily.',
        'intro': ("Macao packs a lot into about 33 square kilometres: a Portuguese-era old town on the peninsula, "
                  "the village lanes of Taipa and Coloane, and the resort towers of Cotai in between. These are the travel guides, "
                  "walking tours and first-impression vlogs people watch most, from the bungy jump off Macau Tower to a slow afternoon in Coloane."),
    },
    'Festivals & events': {
        'slug': 'festivals',
        'title': 'Macau Festivals and Events: Light Up Macao, Fireworks, Chinese New Year',
        'description': "Videos of Macao's festivals and big events: Chinese New Year, the International Fireworks Display Contest, the Food Festival, Light Up Macao and more.",
        'intro': ("Macao's year is full of celebrations. Chinese New Year opens it, temple festivals such as A-Ma's birthday and the "
                  "Feast of the Drunken Dragon follow in spring, the International Fireworks Display Contest lights up the harbour in early autumn, "
                  "and the Grand Prix, Food Festival and Light Up Macao close it out. Watch them here before you plan a trip around one."),
    },
    'Food': {
        'slug': 'food',
        'title': 'Macau Food Videos: Egg Tarts, Macanese Cuisine and Street Food',
        'description': 'Where and what to eat in Macao: Portuguese egg tarts, pork chop buns, Macanese cooking, street food and fine dining, in the videos people watch most.',
        'intro': ("Macao was named a UNESCO Creative City of Gastronomy in 2017, and its food is unlike anywhere else. Macanese cooking blends "
                  "Portuguese, Chinese, African and Southeast Asian flavours in dishes like minchi and African chicken. Add Portuguese egg tarts, "
                  "pork chop buns, almond cookies and serradura, plus street snacks and award-winning restaurants in the resorts."),
    },
    'Heritage & history': {
        'slug': 'heritage',
        'title': "Macau History and Heritage Videos: Ruins of St Paul's, Senado Square, A-Ma Temple",
        'description': "Videos on Macao's history and UNESCO-listed heritage: the Ruins of St Paul's, Senado Square, A-Ma Temple, Guia Fortress and the Portuguese era.",
        'intro': ("Portuguese traders settled in Macao in the 1550s, and the city stayed under Portuguese administration until it returned to China "
                  "in 1999. The Historic Centre of Macao, a UNESCO World Heritage Site since 2005, links more than 20 monuments and squares, "
                  "from the A-Ma Temple and Senado Square to the Ruins of St Paul's and the Guia Fortress and lighthouse."),
    },
    'Arts & music': {
        'slug': 'arts',
        'title': 'Macau Arts and Music: Arts Festival, Music Festival, Exhibitions and Opera',
        'description': "Macao's cultural life on video: the Macao Arts Festival, the International Music Festival, exhibitions, Cantonese opera and performances.",
        'intro': ("Macao's cultural calendar includes the Macao Arts Festival in spring and the Macao International Music Festival in autumn, "
                  "along with Cantonese opera, museum exhibitions and street performances. Many of these videos come from the city's own "
                  "cultural channels, so some are in Chinese or Portuguese."),
    },
    'Traditions & local life': {
        'slug': 'local-life',
        'title': 'Local Life in Macau: Taipa Village, Coloane, Temples and Traditions',
        'description': "Everyday Macao beyond the casinos: Taipa Village, Coloane, temples, markets, the Macanese community and local traditions.",
        'intro': ("Beyond the casinos, Macao is a small, close-knit city of temples, street markets, tea houses and old neighbourhoods. "
                  "Look here for Taipa Village and Coloane, the Macanese community and its Patuá language, and the everyday life that locals know best."),
    },
    'Casinos & shows': {
        'slug': 'casinos-shows',
        'title': 'Macau Casinos, Resorts and Shows: Cotai Strip and The House of Dancing Water',
        'description': "Inside Macao's casinos and integrated resorts on the Cotai Strip, plus the shows, from The House of Dancing Water to resort spectacles.",
        'intro': ("Macao is one of the biggest gaming centres in the world, and the integrated resorts of the Cotai Strip have made it an "
                  "entertainment capital too. These videos cover the resorts, the casino floors and shows such as The House of Dancing Water "
                  "at City of Dreams. You must be 21 or older to enter a casino in Macao."),
    },
    'Hotels': {
        'slug': 'hotels',
        'title': 'Macau Hotel Videos: Room Tours and Reviews',
        'description': 'Macau hotel room tours and reviews, from the big Cotai resorts to smaller hotels on the peninsula.',
        'intro': ("From the giant resorts of Cotai to smaller hotels on the peninsula, Macao has places to stay at every budget. "
                  "These room tours and reviews help you choose where to base yourself."),
    },
    'Grand Prix': {
        'slug': 'grand-prix',
        'title': 'Macau Grand Prix Videos: Guia Circuit Onboard Laps, Races and Crashes',
        'description': 'Macau Grand Prix videos: onboard laps of the Guia Circuit, classic races and crashes, the GT World Cup and the Motorcycle Grand Prix.',
        'intro': ("The Macau Grand Prix was first held in 1954 and is now raced each November on the Guia Circuit, a street track whose tight "
                  "corners and close walls make it one of motorsport's most famous. Watch onboard laps, classic moments and the Motorcycle Grand Prix, "
                  "which has been part of the weekend since 1967."),
    },
    'Getting there': {
        'slug': 'getting-there',
        'title': 'How to Get to Macau: Ferry and Bus from Hong Kong, the Bridge and Borders',
        'description': 'Step-by-step videos on getting to Macao: the ferry from Hong Kong, the bus over the Hong Kong-Zhuhai-Macao Bridge, the airport and the borders.',
        'intro': ("Most visitors arrive from Hong Kong, either by ferry, which takes about an hour, or by bus across the Hong Kong-Zhuhai-Macao Bridge, "
                  "which opened in 2018. Macao International Airport and the land borders with Zhuhai complete the picture. "
                  "These videos show each route step by step."),
    },
    'Living there': {
        'slug': 'living',
        'title': 'Living in Macau: Expat Life, Jobs and Cost of Living',
        'description': 'What it is like to live in Macao: expat and resident videos on jobs, housing, the cost of living and settling in.',
        'intro': ("What is daily life like for people who move to Macao? These videos from expats and residents cover jobs, housing, "
                  "the cost of living and what it takes to settle in."),
    },
}

# Section pages: path -> fixed filters and copy
SECTIONS = {
    'home': {
        'path': '/', 'base': {},
        'title': 'MacaoTube: Macao (Macau) on YouTube, Sorted by Topic',
        'h1': 'Macao on YouTube, sorted by topic',
        'description': 'Discover and visit Macao through its most-watched YouTube videos: travel guides, food, festivals, heritage and the Grand Prix, from official channels and independent creators. Updated daily.',
        'intro': 'The most-watched videos about Macao: travel guides, food, festivals, heritage and the Grand Prix, from official channels and independent creators. Updated every day.',
    },
    'videos': {
        'path': '/videos/', 'base': {'format': 'long'},
        'title': 'Macau Videos: Travel Guides, Documentaries and Vlogs',
        'h1': 'Videos', 'description': 'Long-form YouTube videos about Macao: travel guides, documentaries, walking tours and vlogs, ranked and updated daily.',
        'intro': 'Travel guides, documentaries, walking tours and vlogs longer than three minutes.',
    },
    'shorts': {
        'path': '/shorts/', 'base': {'format': 'short'},
        'title': 'Macau Shorts: Quick Videos of Macao',
        'h1': 'Shorts', 'description': 'The most-watched YouTube Shorts about Macao: quick looks at food, sights, shows and festivals.',
        'intro': 'Quick looks at Macao in three minutes or less.',
    },
    'official': {
        'path': '/official/', 'base': {'src': 'official'},
        'title': 'Official Macao Tourism and Culture Videos',
        'h1': 'Official channels', 'description': "Videos from Macao's official tourism and culture channels: festivals, events, heritage and promotional films.",
        'intro': "Festivals, events, heritage and promotional films from Macao's official tourism and culture channels.",
    },
    'creators': {
        'path': '/creators/', 'base': {'src': 'creators'},
        'title': 'Macau Travel Vlogs by Independent Creators',
        'h1': 'Independent creators', 'description': 'English-language Macau travel vlogs, food tours and guides from independent YouTube creators.',
        'intro': 'English-language travel vlogs, food tours and guides from YouTube creators outside government.',
    },
}


def topic_path(topic):
    return f"/topics/{TOPICS[topic]['slug']}/"


# What's on: upcoming events. Confirmed dates use start/end; others give the usual
# timing in `when` and a `sort` date for ordering. An event disappears from the
# site once `end` (or `sort` + 31 days for unconfirmed ones) has passed.
# Sources are kept so dates can be re-checked each year.
EVENTS = [
    {'name': 'Macao International Music Festival', 'start': '2026-10-02', 'end': '2026-11-29',
     'where': 'Venues across the city, including the Macao Cultural Centre',
     'what': 'Two months of classical concerts, opera and crossover performances, some of them free.',
     'link': '/topics/arts/', 'organizer': ('Cultural Affairs Bureau of Macao', 'https://www.icm.gov.mo'), 'source': 'https://www.thestandard.com.hk/news/article/345942'},
    {'name': '73rd Macau Grand Prix', 'start': '2026-11-19', 'end': '2026-11-22',
     'where': 'Guia Circuit',
     'what': 'Four days of street racing: the FIA FR, GT and F4 World Cups, the Guia Race and the Motorcycle Grand Prix. Hotels fill up and prices peak, so book early.',
     'link': '/grand-prix/', 'organizer': ('Macau Grand Prix Committee', 'https://www.macau.grandprix.gov.mo'), 'tickets': 'https://www.macau.grandprix.gov.mo', 'source': 'https://macaudailytimes.com.mo/organizers-confirm-program-for-the-73rd-edition.html'},
    {'name': '26th Macau Food Festival', 'start': '2026-11-20', 'end': '2026-12-06',
     'where': 'Sai Van Lake Square, beside Macau Tower',
     'what': 'Around 150 local food and drink vendors. Open 4pm to 11pm Monday to Thursday, and 3pm to midnight Friday to Sunday.',
     'link': '/?q=food+festival', 'free': True, 'source': 'https://thebeat.asia/hong-kong/delish/happenings/26th-macau-food-festival'},
    {'name': 'Light Up Macao', 'when': 'Usually December into January', 'sort': '2026-12-06',
     'where': 'Nam Van and other neighbourhoods',
     'what': 'Free evening light installations and projection shows around the city. Dates for this season are not yet announced.',
     'link': '/?q=light+up+macao', 'source': 'https://macaudailytimes.com.mo/light-festival-returns-with-shorter-run-bigger-displays.html'},
    {'name': 'Macao SAR Establishment Day', 'start': '2026-12-20', 'end': '2026-12-20',
     'where': 'Across the city',
     'what': 'Public holiday marking the return of Macao to China in 1999.',
     'link': '/topics/heritage/', 'source': 'https://www.humanresourcesonline.net/macao-s-2027-public-holidays-and-rest-days-for-public-employees'},
    {'name': 'Chinese New Year (Year of the Goat)', 'start': '2027-02-06', 'end': '2027-02-08',
     'where': 'Senado Square, Sai Van Lake and the Macau Tower waterfront',
     'what': 'Public holidays from 6 to 8 February, with dragon parades, fireworks and drone shows usually spread over the first two weeks. Expect big crowds.',
     'link': '/?q=chinese+new+year', 'organizer': ('Macao Government Tourism Office', 'https://www.macaotourism.gov.mo'), 'free': True, 'source': 'https://www.humanresourcesonline.net/macao-s-2027-public-holidays-and-rest-days-for-public-employees'},
    {'name': 'A-Ma Festival', 'when': 'Usually April or May (23rd day of the third lunar month)', 'sort': '2027-04-28',
     'where': 'A-Ma Temple, Barra',
     'what': "Birthday of the sea goddess A-Ma, with Chinese opera, incense and lion dances at the temple which, by tradition, gave Macao its name.",
     'link': '/?q=a-ma', 'source': 'https://macaulifestyle.com'},
    {'name': "Buddha's Birthday and the Feast of the Drunken Dragon", 'start': '2027-05-13', 'end': '2027-05-13',
     'where': 'Temples, and the Red Market and Inner Harbour area',
     'what': "Fishmongers parade a wooden dragon through the streets and share rice wine: a hallmark of Macao, listed as national intangible cultural heritage.",
     'link': '/topics/local-life/', 'source': 'https://macaulifestyle.com/event/feast-of-the-drunken-dragon'},
    {'name': 'Macao Arts Festival', 'when': 'Usually May to June', 'sort': '2027-05-08',
     'where': 'Theatres and outdoor venues',
     'what': "The city's flagship performing-arts festival: theatre, dance, music and street performances.",
     'link': '/topics/arts/', 'source': 'https://www.icm.gov.mo'},
    {'name': 'Dragon Boat Festival races', 'when': 'Around 9 June 2027', 'sort': '2027-06-09',
     'where': 'Nam Van Lake',
     'what': 'International and local dragon boat races around the Tuen Ng festival.',
     'link': '/topics/festivals/', 'source': 'https://www.humanresourcesonline.net/macao-s-2027-public-holidays-and-rest-days-for-public-employees'},
    {'name': 'Macao International Fireworks Display Contest', 'when': 'Usually five nights, mid-September to early October', 'sort': '2027-09-15',
     'where': 'Macau Tower waterfront',
     'what': 'Fireworks teams from around the world compete over the water; free to watch from the waterfront.',
     'link': '/?q=fireworks', 'source': 'https://www.thestandard.com.hk/news/article/343374'},
    {'name': 'Mid-Autumn Festival', 'start': '2027-09-15', 'end': '2027-09-15',
     'where': 'Senado Square, Lou Lim Ieoc Garden',
     'what': 'Lantern displays and mooncakes; 16 September is a public holiday.',
     'link': '/topics/festivals/', 'source': 'https://www.humanresourcesonline.net/macao-s-2027-public-holidays-and-rest-days-for-public-employees'},
    {'name': 'Lusofonia Festival', 'when': 'Usually late October to early November', 'sort': '2027-10-24',
     'where': 'Taipa Houses and Largo do Carmo',
     'what': "Food, music and dance from the Portuguese-speaking world: the easiest way to see Macao's Portuguese heritage up close.",
     'link': '/topics/local-life/', 'source': 'https://www.gov.mo/en/news/372814'},
    {'name': '74th Macau Grand Prix', 'when': 'Usually mid-to-late November', 'sort': '2027-11-18',
     'where': 'Guia Circuit',
     'what': 'Next year’s edition of the street race.',
     'link': '/topics/grand-prix/', 'source': 'https://51gt3.com'},
]


# Partner programme. Prices in MOP (US$1 ≈ MOP 8). Contact goes live once the inbox is verified.
PARTNER_EMAIL = 'partners@macaotube.org'
PACKAGES = [
    {'name': 'Founding partner', 'price': 'MOP 2,400', 'per': 'for 3 months (≈ US$300)', 'note': 'Only three founding places',
     'gets': ['"Presented by" on one topic page of your choice', 'Your logo and link on the About page',
              'A mention in the MacaoTube email once it launches', 'The founding rate if you renew']},
    {'name': 'Season sponsor', 'price': 'MOP 800', 'per': 'for the 2026 season (≈ US$100)', 'note': 'Grand Prix or Food Festival',
     'gets': ['"Presented by" on the Grand Prix or Food Festival page', 'A line on What\'s on beside the event',
              'Runs until 6 December 2026']},
    {'name': 'Business video page', 'price': 'from MOP 1,500', 'per': 'setup, then MOP 300 a month', 'note': 'For hotels, shops and restaurants',
     'gets': ['A page of the most-watched videos about the streets around your business, updated daily',
              'A QR code for your front desk, menus or windows', 'A link you can put on your own website']},
]

# Live sponsorships: page path -> sponsor. Shown as a labelled "Presented by" line.
# Example: '/topics/food/': {'name': 'Example Café', 'url': 'https://example.com', 'line': 'Macanese food since 1990'}
SPONSORS = {}


# Grand Prix race-week hub (/grand-prix/). Facts checked 2026-11-05 (ticket prices re-checked 2026-11-12 via moefriends.com and heatalk.com, both citing the organiser) against:
#   https://macaudailytimes.com.mo/organizers-confirm-program-for-the-73rd-edition.html (12 Oct 2026: dates, seven races, ticket channels, on-site booths)
#   https://www.macaupostdaily.com/news/29720 (20 Oct 2026: dates, Guia Circuit, race names, 58th Motorcycle GP)
#   https://en.wikipedia.org/wiki/Guia_Circuit (6.12 km, opened 1954, Melco Hairpin 7 m wide)
#   https://macaudailytimes.com.mo/gp-tickets-go-on-sale-with-a-sharp-price-increase.html (2023 prices: race days MOP 400-1,000, practice MOP 100)
# 2026 per-stand prices were not confirmed by an official source, so the page gives the recent range and sends readers to the official site.
GP_OFFICIAL = 'https://www.macau.grandprix.gov.mo/'
GP_HUB = {
    'path': '/grand-prix/',
    'title': 'Macau Grand Prix 2026: Dates, Races, Tickets and the Best Videos',
    'description': 'The 73rd Macau Grand Prix runs 19-22 November 2026 on the Guia Circuit. Dates, the seven races, tickets, where to watch, and the best onboard laps, races and crashes on YouTube.',
    'intro': ('Every November, the streets of Macao turn into the Guia Circuit, a 6.1 km track with walls inches from the cars '
              'and a hairpin so tight that drivers queue to get round it. Here is what is on this year, how to go, '
              'and the videos to watch before race week.'),
    'facts': [
        ('When', '19-22 November 2026. Thursday and Friday are practice and qualifying; Saturday and Sunday are race days.'),
        ('Where', 'Guia Circuit, a 6.1 km street track around the Macao peninsula, first raced in 1954.'),
        ('Edition', 'The 73rd Macau Grand Prix and the 58th Macau Motorcycle Grand Prix.'),
        ('Races', 'Macau Grand Prix (FIA FR World Cup), Macau GT Cup (FIA GT World Cup), Macau Guia Race (FIA TCR World Tour), '
                  'FIA F4 World Cup, Macau Motorcycle Grand Prix, Greater Bay Area GT Cup (GT4) and Macau Roadsport Challenge.'),
        ('Tickets', 'On sale since 9 October through Macau Ticket, Kwong Sing stores, Trip.com, Ctrip and Damai, plus booths by the stands '
                    'with counters and self-service machines. Practice and qualifying days (19-20 Nov) cost MOP 100 for any stand; race days (21-22 Nov) '
                    'cost MOP 400 at the Reservoir Stand, MOP 750 at the Grandstand and MOP 1,200 for a reserved seat at the Lisboa Bend. Everyone aged 2 or over needs a ticket.'),
    ],
    'faq': [
        ('When is the Macau Grand Prix 2026?',
         'The 73rd Macau Grand Prix runs from 19 to 22 November 2026. Thursday 19 and Friday 20 November are practice and qualifying days; '
         'the races are on Saturday 21 and Sunday 22 November.'),
        ('Where is the Macau Grand Prix held?',
         'On the Guia Circuit, a 6.1 km street circuit on the Macao peninsula that has hosted racing since 1954. Its Melco Hairpin is only '
         'about 7 metres wide, one of the tightest corners in international motorsport.'),
        ('What races are on at the 2026 Macau Grand Prix?',
         'Seven races: the Macau Grand Prix for the FIA FR World Cup, the Macau GT Cup for the FIA GT World Cup, the Macau Guia Race for the '
         'FIA TCR World Tour, the FIA F4 World Cup, the 58th Macau Motorcycle Grand Prix, the Greater Bay Area GT Cup and the Macau Roadsport Challenge.'),
        ('How do I buy Macau Grand Prix tickets?',
         'Through Macau Ticket (macauticket.com), Kong Seng stores in Macao, outlets in Hong Kong and mainland China, the Trip.com, Ctrip and Damai apps, '
         'and the EGL Tours website. During the event there are ticket booths at the circuit with counters and self-service machines.'),
        ('How much are Macau Grand Prix tickets?',
         'For 2026, practice and qualifying days (19 and 20 November) cost MOP 100 a day at any stand. On race days (21 and 22 November) '
         'the Reservoir Stand costs MOP 400, the Grandstand MOP 750 and a reserved seat at the Lisboa Bend MOP 1,200, per person per day. '
         'Macao residents with a student card, aged 65 or over or with a disability card can buy a MOP 150 Reservoir Stand ticket on race days.'),
        ('Can I watch the Macau Grand Prix for free?',
         'From 2023 to 2025 the FIA streamed the FR, F3, F4 and GT World Cup races at Macau live on its YouTube channel, and the full replays '
         'are still online; you will find them in the rows above. Check the FIA channel nearer race week to see whether 2026 is streamed too.'),
    ],
    # Each video joins the first row whose pattern matches its title; rows under 3 videos are hidden.
    'skip': r'disney|assetto|game vs|gran turismo|iracing|f1 2026|karting',
    'rows': [
        ('Onboard laps', r'\bon-?board\b|\bhot lap\b|\blap (?:around|of)\b|\bdrive around\b|driver.s eye|in car camera'),
        ('Crashes and drama', r'\bcrash|pile ?-?up|\bfails\b|\bwtf\b|\binsan|\bcraz|\bhorror\b|\bairborne\b|\bflip\b|wild finish|incredible finish'),
        ('Motorcycle Grand Prix', r'motorcycle|\bbikes?\b|電單車|schwantz|hickman|\bsbk\b|road ?racing|king of the roads|motogp'),
        ('GT World Cup', r'\bgt\b|\bgt[34]\b|gt cup|gt world cup'),
        ('Formula races: FR, F3 and F4', r'\bf[34]\b|formula (?:3|4|regional)|\bfr world cup\b'),
        ('Fan trips, vlogs and the museum', r'vlog|museum|博物館|\bday \d|final day|tsingtao|everything you need|visiting|review|explained|what its like|明星'),
    ],
}

# Official MacaoTube social accounts.
SOCIAL = [
    ('Instagram', 'https://www.instagram.com/macaotube/'),
    ('Threads', 'https://www.threads.com/@macaotube'),
    ('X', 'https://x.com/MacaoTube'),
    ('YouTube', 'https://www.youtube.com/@macaotube_org'),
    ('TikTok', 'https://www.tiktok.com/@macaotube'),
]
