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
        'title': 'MacaoTube: The Best YouTube Videos About Macao (Macau)',
        'h1': 'The best YouTube videos about Macao',
        'description': 'Discover and visit Macao through the best YouTube videos: travel guides, food, festivals, heritage and the Grand Prix, from official channels and independent creators. Updated daily.',
        'intro': 'Travel guides, food, festivals, heritage and the Grand Prix, from official channels and the creators people actually watch. Updated every day.',
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
        'h1': 'Shorts', 'description': 'The best YouTube Shorts about Macao: quick looks at food, sights, shows and festivals.',
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
