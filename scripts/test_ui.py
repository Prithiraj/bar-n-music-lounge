"""Browser checks against the built static site. Test reports are not certification."""
import json
import pathlib
import shutil
from playwright.sync_api import sync_playwright

out = pathlib.Path('review')
out.mkdir(exist_ok=True)
base = 'http://localhost:4173/'
report = {'screens': [], 'accessibility': [], 'functional': [], 'errors': []}

def check(name, ok, details=None):
    report['functional'].append({'name': name, 'passed': bool(ok), 'details': details})
    if not ok:
        report['errors'].append(name)

def load(page, route=''):
    page.goto(base + route, wait_until='networkidle', timeout=60000)
    page.locator('.photo img').evaluate_all('(imgs) => imgs.forEach(i => i.loading = "eager")')
    page.wait_for_function('Array.from(document.querySelectorAll(".photo img")).every(i => i.complete)', timeout=30000)
    page.evaluate('document.fonts.ready')

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(reduced_motion='reduce', viewport={'width':1440,'height':1000})
        page = context.new_page()
        page.on('pageerror', lambda error: report['errors'].append('pageerror: ' + str(error)))
        for route in ['', 'events/', 'visit/']:
            for width, height in [(320,900),(390,844),(768,1024),(1024,768),(1440,1000),(812,375)]:
                page.set_viewport_size({'width':width,'height':height})
                load(page, route)
                screen = {'page':route or 'home', 'width':width, 'height':height,
                          'overflow':page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),
                          'h1':page.locator('h1').count(),
                          'images':page.locator('.photo img').evaluate_all('(imgs) => imgs.map(i=>({src:i.src,ok:i.complete && i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight}))')}
                report['screens'].append(screen)
                check(f'layout {route or "home"} {width}x{height}', not screen['overflow'] and screen['h1']==1)
                check(f'images {route or "home"} {width}', all(i['ok'] for i in screen['images']))
                if width in [390,1440]:
                    page.screenshot(path=str(out/f'{route.strip("/") or "home"}-{width}.png'),full_page=True)
                    page.add_script_tag(path='node_modules/axe-core/axe.min.js')
                    result = page.evaluate('async () => await axe.run(document, {runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
                    violations = [{'id':v['id'],'impact':v['impact'],'description':v['description'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in result['violations']]
                    report['accessibility'].append({'page':route or 'home','width':width,'violations':violations,'incomplete_count':len(result['incomplete'])})
                    check(f'axe {route or "home"} {width}', not violations, violations)
            page.set_viewport_size({'width':390,'height':844})
            load(page, route)
            page.add_style_tag(content='html {font-size:200% !important;}')
            overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
            offenders = page.locator('body *').evaluate_all('(els)=>els.filter(e=>{const r=e.getBoundingClientRect();return r.width>0 && (r.right>innerWidth+1 || r.left < -1) && getComputedStyle(e).position!=="fixed"}).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right,left:e.getBoundingClientRect().left})).slice(0,25)') if overflow else []
            check(f'text enlargement {route or "home"}', not overflow, offenders)
            page.screenshot(path=str(out/f'{route.strip("/") or "home"}-text-200.png'),full_page=True)

        page.set_viewport_size({'width':390,'height':844})
        load(page)
        page.locator('.mobile-nav summary').focus()
        page.keyboard.press('Enter')
        check('mobile menu opens by keyboard', page.locator('.mobile-nav').evaluate('(e)=>e.open'))
        page.keyboard.press('Escape')
        check('mobile Escape restores focus', page.locator('.mobile-nav summary').evaluate('(e)=>document.activeElement===e') and not page.locator('.mobile-nav').evaluate('(e)=>e.open'))
        page.locator('.mobile-nav summary').click()
        page.locator('.mobile-nav nav a[href="./#food"]').click()
        check('mobile anchor closes menu', not page.locator('.mobile-nav').evaluate('(e)=>e.open'))

        page.set_viewport_size({'width':1440,'height':1000})
        load(page)
        launch = page.locator('.hero-main [data-photo]')
        launch.focus()
        page.keyboard.press('Enter')
        check('gallery opens by keyboard', page.locator('dialog').evaluate('(e)=>e.open'))
        page.keyboard.press('ArrowRight')
        check('gallery advances', page.locator('.dialog-count').inner_text()=='2 / 4')
        page.keyboard.press('ArrowLeft')
        check('gallery reverses', page.locator('.dialog-count').inner_text()=='1 / 4')
        page.screenshot(path=str(out/'gallery.png'))
        page.keyboard.press('Escape')
        check('gallery restores trigger focus', launch.evaluate('(e)=>document.activeElement===e'))
        check('reduced-motion feedback disabled', page.locator('.photo img').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s')
        check('no continuous WebGL or audio', page.locator('canvas,audio,video').count()==0)

        seen=set()
        for route in ['', 'events/', 'visit/']:
            load(page,route)
            for href in page.locator('a[href]').evaluate_all('(a)=>a.map(e=>e.href)'):
                if not href.startswith(base): continue
                url=href.split('#')[0]
                if url not in seen:
                    seen.add(url)
                    response=page.request.get(url)
                    check('internal link '+url,response.status==200)
        load(page,'visit/')
        context.grant_permissions(['clipboard-read','clipboard-write'])
        page.locator('[data-copy-address]').click()
        page.wait_for_function('document.querySelector(".copy-status").textContent === "Address copied."')
        check('copy address success',page.locator('.copy-status').inner_text()=='Address copied.')
        page.evaluate('() => { navigator.clipboard.writeText = async () => {throw new Error("test denial")}; }')
        page.locator('[data-copy-address]').click()
        page.wait_for_function('document.querySelector(".copy-status").textContent.includes("Select the address")')
        check('copy address recovery', 'Select the address' in page.locator('.copy-status').inner_text())
        context.close()

        nojs=browser.new_context(java_script_enabled=False)
        np=nojs.new_page()
        for route in ['', 'events/', 'visit/']:
            np.goto(base+route,wait_until='domcontentloaded')
            check('no-JS content '+(route or 'home'),np.locator('h1').count()==1 and np.locator('a[href*="google.com/maps"]').count()>0)
        np.goto(base+'events/',wait_until='domcontentloaded')
        check('no-JS dated calendar visible',np.locator('[data-event-date]').count()==7)
        nojs.close()

        for iso,visible in [('2026-09-12T03:59:00Z',True),('2026-09-12T04:01:00Z',False),('2027-01-01T12:00:00Z',False)]:
            c=browser.new_context()
            c.add_init_script('''{const D=Date; window.Date=class extends D {constructor(...a){super(...(a.length?a:["'''+iso+'''"]));} static now(){return new D("'''+iso+'''").getTime();}};}''')
            q=c.new_page();q.goto(base+'events/',wait_until='networkidle')
            check('New York expiry '+iso,q.locator('#twizted').is_visible()==visible)
            if iso.startswith('2027'):
                check('empty calendar state',q.locator('[data-event-empty]').is_visible())
            c.close()
        failed=browser.new_context()
        failed.route('**/cdn.usarestaurants.info/**',lambda route:route.abort())
        q=failed.new_page();q.goto(base,wait_until='networkidle')
        check('image failure has honest fallback',q.locator('.hero-main .image-fallback').is_visible())
        check('image failure keeps directions available',q.locator('a[href*="google.com/maps"]').count()>0)
        failed.close()
        browser.close()
except Exception as exc:
    report['errors'].append(repr(exc))
finally:
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    shutil.copytree('site',out/'built-site',dirs_exist_ok=True)
    print(json.dumps(report,indent=2))
if report['errors']:
    raise SystemExit('Browser review reported failures: '+str(report['errors']))
