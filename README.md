# Out-n-About — Live & Local

Static, photo-led website for Out-n-About Bar and Music Lounge in Dundee, Florida.

Live: https://prithiraj.github.io/bar-n-music-lounge/

## Build and preview

Requires Python 3.12 or later, with no build dependencies:

```sh
python scripts/build.py
python -m http.server 8000 --directory site
```

The build generates Home, Events and Visit in `site/`. Page templates, shared navigation, the dated event list, hours and photo metadata live in **scripts/build.py**. Change content there, not in the generated HTML. Design tokens and responsive layouts: **site/assets/styles.css**. Progressive enhancement: **site/assets/site.js**.

Pushes to main build and deploy the `site/` directory through GitHub Pages. The visual-review workflow exercises the browser on the design branch and pull requests; its artifacts include desktop/mobile screenshots and an explicit test report.

## What changed in the vibrancy redesign

- Cream, coral and gold replace the uniformly dimmed visual treatment.
- Loaded Barlow Condensed and DM Sans replace unavailable-font assumptions.
- Photo collages preserve native image proportions and natural brightness.
- The old New Grove Lounge sign is no longer used as a food/venue image.
- Event-poster cards lead to actual dated listings, not a pretend ticket checkout.
- A keyboard-operable photo dialog, mobile navigation, clipboard fallback and New York date expiry are progressively enhanced. Core content works without JavaScript.
- Removed the always-running WebGL overlay. There is no automatic audio, motion loop, social embed or tracking script. CSS hover feedback respects reduced motion.

## Evidence and maintenance boundary

The inherited public event listings and hours remain dated **September 6, 2026**. This update is not an owner confirmation of operational facts. Unknown event times are visibly unconfirmed. The conflicting phone number is still omitted. No menu prices, cover-charge policy, dress-code policy or fabricated reviews were added.

Photos are inherited external references to a public venue listing. The listing attributes the selected photos to the venue, but **that does not establish permission to republish, current ownership or the capture date**. One karaoke photograph visibly dates from 2018. The website calls them archive photos, and drinks shown are not presented as a current menu. Do not treat this as a rights clearance. Owner-supplied, rights-cleared originals remain the required long-term replacement. No new stock or generated documentary imagery was introduced.

Google Fonts and the existing external image host receive browser requests; no analytics or advertising pixels are added. Fonts use `display=swap`; imagery has error states. Review third-party hosting/privacy requirements before commercial handover.

Accessibility is a WCAG 2.2 AA target, not a certification. Browser checks and axe scans do not replace manual assistive-technology review.
