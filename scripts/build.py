"""Build the three static pages with Python's standard library. Run from any folder."""
from pathlib import Path
from html import escape
import json

root = Path(__file__).resolve().parents[1]
(root / 'site/assets').mkdir(parents=True, exist_ok=True)
base = 'https://prithiraj.github.io/bar-n-music-lounge/'
fb = 'https://www.facebook.com/outnaboutbar/'
maps = 'https://www.google.com/maps/dir/?api=1&destination=28.0204627,-81.6333917'
source = 'https://usarestaurants.info/explore/united-states/florida/polk-county/dundee/out-n-about-bar-and-music-lounge-863-439-1537.htm'
# Inherited, externally hosted archive photographs. Attribution is NOT a rights grant.
# The old New Grove Lounge sign is deliberately excluded. Do not imply current owners,
# current drink availability, or a recent shoot. Replace only with cleared originals.
hashes = ['626914c393cd48afea4e633be7ee655a', 'a6e6a1d12ce86f3843a34515d819a086', '5f69c28a3f7f4950221f33117f396576', 'b00117ed0120d1425c1b2dca96bab26f']
photos = [dict(src=f'https://cdn.usarestaurants.info/assets/uploads/{h}_-united-states-florida-polk-county-dundee-out-n-about-bar-and-music-lounge-863-439-1537htm.jpg', alt=a, caption=c, width=w, height=he) for h, a, c, w, he in zip(hashes, ['Patrons seated around the bar beneath exposed wooden rafters.', 'Two people holding microphones during a karaoke session.', 'An orange and red drink with ice on the bar.', 'An orange drink with a lime wedge on the bar.'], ['Around the bar', 'Taking the mic', 'Something colorful', 'A little citrus'], [1024, 720, 720, 720], [768, 540, 960, 960])]
arrow = '<span aria-hidden="true">↗</span>'
spark = '<span class="spark" aria-hidden="true">✳</span>'


def photo(i, cls='', eager=False):
    p = photos[i]
    return f'''<figure class="photo {cls}"><a class="photo-link" href="{p['src']}" data-photo="{i}" aria-label="Enlarge photo: {p['caption']}"><img src="{p['src']}" alt="{p['alt']}" width="{p['width']}" height="{p['height']}" {'fetchpriority="high"' if eager else 'loading="lazy"'} decoding="async"><span class="photo-zoom" aria-hidden="true">↗</span></a><figcaption>{p['caption']} <span>Photo archive</span></figcaption></figure>'''


def header(page):
    pre = './' if page == 'home' else '../'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="{pre}" aria-label="Out-n-About Bar and Music Lounge home"><span class="brand-mark" aria-hidden="true">o<span>n</span>a</span><span><strong>OUT-N-ABOUT</strong><small>BAR & MUSIC LOUNGE</small></span></a>
<nav class="desktop-nav" aria-label="Primary"><a href="{pre}events/" {'aria-current="page"' if page == 'events' else ''}>What’s on</a><a href="{pre}#vibe">The vibe</a><a href="{pre}#food">Food & drinks</a><a class="button button-dark button-small" href="{pre}visit/" {'aria-current="page"' if page == 'visit' else ''}>Find us {arrow}</a></nav>
<details class="mobile-nav"><summary>Menu <span aria-hidden="true">+</span></summary><nav aria-label="Mobile primary"><a href="{pre}events/" {'aria-current="page"' if page == 'events' else ''}>What’s on</a><a href="{pre}#vibe">The vibe</a><a href="{pre}#food">Food & drinks</a><a href="{pre}visit/" {'aria-current="page"' if page == 'visit' else ''}>Find us ↗</a></nav></details>
</div></header>'''


def footer(page):
    pre = './' if page == 'home' else '../'
    return f'''<footer class="site-footer"><div class="shell"><div class="footer-top"><a class="footer-wordmark" href="{pre}">OUT-N-ABOUT</a><p>BAR & MUSIC LOUNGE<br>DUNDEE, FLORIDA</p></div><div class="footer-bottom"><span>Good music. Great nights.</span><nav aria-label="Footer"><a href="{pre}events/">What’s on</a><a href="{pre}visit/">Find us</a><a href="{fb}" rel="noopener">Facebook ↗</a></nav><a href="{source}" class="credit" rel="noopener">Photo source ↗</a></div><p class="footer-note">Photos are from the venue’s public listing archive and may show earlier appearances. Hours, events and specials can change; check with the venue before traveling.</p></div></footer>'''


def visitcta(page):
    pre = './' if page == 'home' else '../'
    return f'''<section class="visit-band" aria-labelledby="find-heading"><div class="shell visit-band-grid"><div><p class="eyebrow">MAKE YOUR WAY TO DUNDEE</p><h2 id="find-heading">Less scrolling.<br>More going out.</h2></div><div class="visit-band-info"><address>28390 US-27<br>Dundee, FL 33838</address><div class="actions"><a class="button button-dark" href="{maps}">Get directions {arrow}</a><a class="text-link" href="{pre}visit/">Hours & details →</a></div></div>{spark}</div></section>'''


def doc(page, title, desc, body):
    pre = 'assets/' if page == 'home' else '../assets/'
    canonical = base + ('' if page == 'home' else page + '/')
    schema = ''
    if page == 'home':
        schema = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'BarOrPub', '@id': base + '#venue', 'name': 'Out-n-About Bar and Music Lounge', 'url': base, 'address': {'@type': 'PostalAddress', 'streetAddress': '28390 US-27', 'addressLocality': 'Dundee', 'addressRegion': 'FL', 'postalCode': '33838', 'addressCountry': 'US'}, 'geo': {'@type': 'GeoCoordinates', 'latitude': 28.0204627, 'longitude': -81.6333917}}) + '</script>'
    return f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#F8F3E9"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{photos[0]['src']}"><meta property="og:image:alt" content="{photos[0]['alt']}"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{pre}styles.css?v=live-room-2">{schema}<script src="{pre}site.js?v=live-room-2" defer></script></head><body data-page="{page}">{header(page)}<main id="main">{body}</main>{footer(page)}<script id="photo-data" type="application/json">{json.dumps(photos)}</script></body></html>'''


# Preserve previously published event information, with provenance and unknown times
# visible. Confirm with the operator before describing this as a live/official feed.
events = [
    dict(date='2026-09-11', day='FRI', month='SEP', num='11', title='TwiZted', kind='LIVE ROCK', time='8:00 PM EDT', description='Rock favorites from the ’70s through today.', link='https://www.bandsintown.com/e/108855322-twizted-at-out-n-about-bar-and-music-lounge', source='Bandsintown', id='twizted', colour='gold'),
    dict(date='2026-09-12', day='SAT', month='SEP', num='12', title='Ridge Country', kind='LIVE MUSIC', time='Time to be confirmed', description='A live-music date on the Dundee calendar.', link=fb, source='HappeningNext', id='ridge-country', colour='cream'),
    dict(date='2026-09-26', day='SAT', month='SEP', num='26', title='The Highway 41', kind='LIVE MUSIC', time='Time to be confirmed', description='Another reason to make a night of it.', link=fb, source='HappeningNext', id='highway-41', colour='coral'),
    dict(date='2026-10-16', day='FRI', month='OCT', num='16', title='RocTober', kind='LIVE MUSIC', time='Time to be confirmed', description='', link=fb, source='HappeningNext', id='roctober', colour='cream'),
    dict(date='2026-11-13', day='FRI', month='NOV', num='13', title='TwiZted', kind='LIVE ROCK', time='Time to be confirmed', description='', link=fb, source='HappeningNext', id='twizted-nov', colour='gold'),
    dict(date='2026-11-14', day='SAT', month='NOV', num='14', title='Come Together 4 Rock N Roll', kind='LIVE MUSIC', time='Time to be confirmed', description='', link=fb, source='HappeningNext', id='come-together', colour='coral'),
    dict(date='2026-12-05', day='SAT', month='DEC', num='05', title='The Highway 41', kind='LIVE MUSIC', time='8:00 PM–12:00 AM', description='', link='https://thehighway41band.com/', source='Performer schedule', id='highway-41-dec', colour='cream'),
]


def ticket(e):
    return f'''<article class="gig-ticket ticket-{e['colour']}" data-event-date="{e['date']}"><div class="ticket-top"><p class="eyebrow">{e['kind']}</p><time datetime="{e['date']}">{e['day']} / {e['month']} {e['num']}</time></div><h3>{e['title']}</h3><p class="ticket-time">{e['time']}</p><div class="ticket-bottom"><span>Out-n-About · Dundee</span><a href="events/#{e['id']}" aria-label="Event details for {e['title']} on {e['date']}">↗</a></div></article>'''


def listing(e):
    return f'''<article class="event-row" id="{e['id']}" data-event-date="{e['date']}"><time class="event-date" datetime="{e['date']}"><span>{e['month']}</span><strong>{e['num']}</strong><small>{e['day']}</small></time><div class="event-info"><p class="eyebrow">{e['kind']}</p><h3>{e['title']}</h3><p>{e['time']}</p>{f'<p class="muted">{e["description"]}</p>' if e['description'] else ''}</div><div class="event-actions"><a class="button button-outline" href="{e['link']}" rel="noopener">{'Event listing' if e['source'] == 'Bandsintown' else 'Check latest'} {arrow}</a><small>{e['source']}</small></div></article>'''


home = f'''
<section class="hero" aria-labelledby="hero-heading"><div class="shell hero-grid"><div class="hero-copy"><p class="eyebrow location-label"><span class="status-dot" aria-hidden="true"></span> DUNDEE, FLORIDA · LIVE & LOCAL</p><h1 id="hero-heading">Good music.<br><em>Great nights.</em></h1><p class="hero-lead">Your hometown spot for live bands, karaoke, food & cold drinks. Right here on US-27.</p><div class="actions"><a class="button button-coral" href="events/">See what’s on {arrow}</a><a class="text-link" href="visit/">Plan your visit →</a></div><p class="hero-footnote">OUT-N-ABOUT BAR & MUSIC LOUNGE</p></div><div class="hero-visual"><div class="photo-halo" aria-hidden="true"></div>{photo(0, 'hero-main', True)}{photo(1, 'hero-inset')}<span class="round-stamp" aria-hidden="true">YOUR<br><strong>LOCAL</strong><br>GOOD TIME</span></div></div></section>
<div class="identity-strip" aria-label="Live bands, karaoke, food and drinks in Dundee"><div class="shell"><span>LIVE BANDS</span>{spark}<span>KARAOKE</span>{spark}<span>FOOD & DRINKS</span>{spark}<span>DUNDEE, FL</span></div></div>
<section class="section gig-section" aria-labelledby="gig-heading"><div class="shell"><div class="section-heading"><div><p class="eyebrow">TURN A DATE INTO A NIGHT OUT</p><h2 id="gig-heading">On the <em>calendar.</em></h2></div><a class="text-link" href="events/">All upcoming dates →</a></div><div class="ticket-grid">{''.join(ticket(e) for e in events[:3])}</div><p class="event-empty" data-event-empty hidden>No upcoming dates are listed here yet. <a href="{fb}">Check the venue’s latest updates ↗</a></p><p class="section-note">Public listings checked September 6, 2026. Dates and times can change. <a href="events/#calendar-note">About the calendar →</a></p></div></section>
<section class="section vibe-section" id="vibe" aria-labelledby="vibe-heading"><div class="shell vibe-grid"><div class="vibe-copy"><p class="eyebrow">SMALL ROOM. BIG REASON TO GO OUT.</p><h2 id="vibe-heading">A mic.<br>A moment.<br><em>Your kind of night.</em></h2><p>Some nights you’re here for the band. Some nights you’re the one holding the mic. That’s the fun of a hometown music spot.</p><a class="text-link" href="{photos[1]['src']}" data-photo="1">Take a look around {arrow}</a></div><div class="vibe-photo-wrap">{photo(1, 'vibe-photo')}<p class="photo-note">A moment from the venue photo archive.</p><span class="vertical-label" aria-hidden="true">KARAOKE / COMMUNITY / GOOD COMPANY</span></div></div></section>
<section class="section food-section" id="food" aria-labelledby="food-heading"><div class="shell food-grid"><div class="drinks-collage">{photo(2, 'drink-main')}{photo(3, 'drink-inset')}<span class="food-sticker" aria-hidden="true">MAKE IT<br><strong>A NIGHT.</strong></span></div><div class="food-copy"><p class="eyebrow">GOOD COMPANY. SOMETHING COLD.</p><h2 id="food-heading">A bite.<br>A drink.<br><em>An encore.</em></h2><p>Make room for food & drinks alongside the music. Check the latest venue updates for the current menu and specials.</p><a class="button button-dark" href="{fb}" rel="noopener">Latest food & drink updates {arrow}</a><p class="food-note">Archive drinks pictured; current selection may differ.</p></div></div></section>
{visitcta('home')}'''

agenda = f'''
<section class="page-hero events-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">OUT-N-ABOUT / THE GIG GUIDE</p><h1>Find your<br><em>next night out.</em></h1><p class="hero-lead">Live music, familiar favorites, and a date worth putting on the calendar.</p><a class="text-link" href="#september">Jump to the dates ↓</a></div><div class="mini-photo-wrap">{photo(1, 'page-photo', True)}<span class="small-stamp" aria-hidden="true">LIVE<br>& LOCAL</span></div></div></section>
<section class="section schedule-section" aria-labelledby="september"><div class="shell"><div class="schedule-heading"><p class="eyebrow">THE LINEUP</p><h2 id="september">September <em>2026</em></h2></div><div class="event-list">{''.join(listing(e) for e in events[:3])}</div><h2 class="later-heading">Later this <em>fall.</em></h2><div class="event-list">{''.join(listing(e) for e in events[3:])}</div><p class="event-empty" data-event-empty hidden>No upcoming dates are currently listed. <a href="{fb}">Check Facebook for new dates ↗</a></p><aside class="calendar-note" id="calendar-note"><strong>A quick note before you head out.</strong><p>This is a guide to public event listings, checked September 6, 2026—not a live venue-managed feed. Unconfirmed times are marked above. Check the linked listing or the venue’s Facebook for changes, admission details and start times.</p><p>Sources: <a href="https://www.bandsintown.com/e/108855322-twizted-at-out-n-about-bar-and-music-lounge">Bandsintown</a>, <a href="https://happeningnext.com/dundee-fl">HappeningNext</a> and <a href="https://thehighway41band.com/">The Highway 41 Band</a>.</p></aside><noscript><p class="section-note">JavaScript is off. This static calendar was prepared September 6, 2026; check dates before traveling.</p></noscript></div></section>{visitcta('events')}'''

hours = [('Monday', 'Closed'), ('Tuesday', '11 AM–2 AM'), ('Wednesday', '1 PM–2 AM'), ('Thursday', '12 PM–2 AM'), ('Friday', '11 AM–2 AM'), ('Saturday', '11 AM–2 AM'), ('Sunday', '12 PM–12 AM')]
visit = f'''
<section class="page-hero"><div class="shell page-hero-grid"><div><p class="eyebrow">28390 US-27 / DUNDEE, FLORIDA</p><h1>Your night.<br><em>Our corner.</em></h1><p class="hero-lead">Make your way to Out-n-About for live music, karaoke, food & drinks.</p><a class="button button-coral" href="{maps}">Get directions {arrow}</a></div>{photo(0, 'page-photo', True)}</div></section>
<section class="section visit-section"><div class="shell visit-grid"><section aria-labelledby="address-heading"><p class="eyebrow">FIND YOUR WAY IN</p><h2 id="address-heading">Right here<br>on <em>US-27.</em></h2><address class="big-address">Out-n-About Bar and Music Lounge<br>28390 US-27<br>Dundee, FL 33838</address><div class="actions"><a class="button button-dark" href="{maps}">Open Google Maps {arrow}</a><button class="text-button" type="button" data-copy-address hidden>Copy address</button></div><p class="copy-status" role="status" aria-live="polite"></p><p class="muted">Use the exact map pin for turn-by-turn directions.</p></section><section class="hours-panel" aria-labelledby="hours-heading"><div class="hours-head"><h2 id="hours-heading">Plan your visit.</h2><span aria-hidden="true">↗</span></div><p class="eyebrow">CURRENTLY LISTED HOURS</p><dl class="hours-list">{''.join(f'<div><dt>{d}</dt><dd>{t}</dd></div>' for d, t in hours)}</dl><p class="hours-note">Public listings as of September 6, 2026. Kitchen, holiday and event hours may differ. Late closing times run into the following day.</p></section></div></section>
<section class="section before-you-go"><div class="shell before-grid"><div><p class="eyebrow">BEFORE YOU HEAD OUT</p><h2>Make sure<br><em>the night’s on.</em></h2></div><div><p>Check the latest event details, same-day updates and specials on the venue’s Facebook page.</p><p class="muted">For questions about age restrictions, cover charges, parking or accessibility, confirm with the venue before your visit.</p><a class="button button-gold" href="{fb}" rel="noopener">Check the latest {arrow}</a></div></div></section>'''

for page, title, desc, body in [
    ('home', 'Out-n-About | Live Music, Karaoke & Good Nights in Dundee, FL', 'Live bands, karaoke, food and drinks at Out-n-About Bar and Music Lounge in Dundee, Florida. See the calendar and plan your visit.', home),
    ('events', 'Live Music & Events | Out-n-About Dundee, FL', 'Find your next night out at Out-n-About. Browse upcoming public event listings, start times and links to check the latest details.', agenda),
    ('visit', 'Hours & Directions | Out-n-About Dundee, FL', 'Find Out-n-About at 28390 US-27 in Dundee, Florida. Get directions, check listed hours and plan your visit.', visit),
]:
    path = root / 'site' / ('index.html' if page == 'home' else page + '/index.html')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc(page, title, desc, body), encoding='utf-8')
print('Built Home, Events and Visit with shared navigation, photo data and event content.')
