# MHF — My Happy Family · Website

A static marketing site for John Naparlo's umbrella company **MHF (My Happy Family)** —
Development · Operations · Management — built from John's notes in
`MHF Website Ideas.docx`, research on the family's public footprint, and the three
reference sites he admires (mullerec.com, dfmdevelopment.com, ryansdev.com).

## Run it

No build tools or server required — open `site/index.html` in a browser, or:

```bash
cd site && python3 -m http.server 8000
```

## Edit it

All page copy lives in **`build.py`** (one shared header/footer/template so the
branding never drifts). After editing, regenerate with:

```bash
python3 build.py
```

The portfolio map/list data lives in **`site/js/properties.js`** — edit that file
directly (no rebuild needed). Each entry has `name`, `category`
(`residential | operations | retail | land`), `location`, `coords` (`[lat, lng]`,
or `null` to list without a map pin), `blurb`, and optionally `image` (card banner
photo) and `url` (adds a "Visit website →" link on the card).

Properties with live websites use real screenshots as card banners
(`site/assets/screenshots/`): Yalick Farms + Yalick Shoppes (yalickfarms.com),
Virginia Car Wash Co. (virginiacarwashco.com), and Burger King (bk.com).
Re-capture them anytime with `node tools/capture-screenshots.js` (needs
`npm i playwright` somewhere on the path). Swap in real property photos from John
as they become available — same `image` field.

Every pinned property also has a satellite/aerial image (`site/assets/locations/`,
`aerial` field) generated from its exact coordinates — regenerate after moving a
pin with `node tools/capture-aerials.js`. The homepage map section pairs these
with an auto-rotating carousel: each slide highlights its pin on the map with a
gold pulse, clicking a pin or dot jumps the carousel, and rotation pauses on
hover. Pin coordinates for Yalick Farms, Yalick Shoppes, Ewell Station, Virginia
Car Wash Co., Newport Circle and Hanover Corner were geocoded from their street
addresses (OpenStreetMap/Nominatim); aerials visibly match the real properties.

## Structure

| Page | Purpose |
|---|---|
| `index.html` | Hero, three pillars, stats, story teaser, featured properties |
| `about.html` | J. Naparlo's story (from John's notes), John's bio, company timeline |
| `portfolio.html` | Interactive Leaflet map with clickable pins + filterable property list |
| `development.html` / `operations.html` / `management.html` | Division pages with personnel |
| `team.html` | Full team with cartoon avatars (DiceBear, per John's "cartoon look-alikes" idea) |
| `careers.html` | The four open positions from John's notes + restaurant careers + general inquiries |
| `contact.html` | Office mini-map + direct contact rows + form (front-end only; supports `?topic=` preselect — careers/leasing/development CTAs route into it) |

## Brand decisions (proposals — easy to change)

- **Aesthetic:** "heritage print Americana" — warm paper grain, letterpress-style
  offset shadows, ledger double-rules, a scalloped umbrella-canopy edge on every
  hero, a vintage sunburst + rotating "EST. 1980" stamp badge on the homepage, and
  a scrolling ticker of the family's brands above the footer.
- **Slogan:** "Family built. Community grown." Footer motif: "All under one umbrella."
- **Logo:** gold umbrella mark (inline SVG in `build.py`, favicon in `site/assets/`) —
  the umbrella = development, operations and management under one family.
- **Palette:** deep evergreen `#1b3527`, warm paper `#f7f1e2`, harvest gold `#c8973a`.
- **Type:** Fraunces (display, with its SOFT/WONK axes) + Newsreader (editorial body
  serif) + Archivo (labels, nav, buttons), via Google Fonts.

## Needs confirmation from John before launch

- **The Orchards & Madison Crest** — no public record found of locations; both are
  listed without map pins. Get addresses/coords from John.
- **Newport Circle** — pinned to Newport Township, PA (the K.M. Smith school
  redevelopment) based on research, but the name match is unconfirmed.
- **Hanover Corner** — pinned to Hanover Township, PA (near the Durkee Farms
  project); confirm.
- **BK Shoppes, C-Store, WaWa, Jimmy John's pads** — listed without pins; need addresses.
- **`info@mhfamily.com`** is a placeholder email; the domain isn't registered to MHF.
  Social links in the footer are `#` placeholders until the LinkedIn/Instagram/Facebook
  pages exist.
- **Contact form** has no backend — wire to Formspree/Netlify Forms/etc. on deploy.
- Stats on the homepage (45+ years, 30+ built, 22 operating) come from John's notes
  and public press; verify the current restaurant count.
- Team uses cartoon avatars and first names per John's notes; swap seeds or real
  surnames as desired (avatars are DiceBear URLs — change `seed=` to regenerate).
- **Photo licensing notes** (from the web hunt): Ewell Station photos exist on
  Flickr but are all-rights-reserved; Times Leader has photos of Guys & Dolls and
  the K.M. Smith/Newport project (newspaper copyright — ask before using); a CC0
  Burger King exterior exists on Wikimedia Commons if a real storefront is ever
  preferred over the brand hero. Branded placeholders are used wherever rights
  are unclear — regenerate with `node tools/make-placeholders.js`.

## Research sources

Key facts verified via the Times Leader profiles of J. Naparlo (2004, 2023),
yalickfarms.com, corporate registry records (MHF Dining Inc., Yalick CCJ LLC),
virginiacarwashco.com, and GlobeSt (Ewell Station). Notable: Virginia Car Wash Co.
is at 4830 Portsmouth Blvd, **Chesapeake** VA; Yalick Farms/Shoppes are in
**Dallas, PA**; the BK history is 1967 (age 16, Kingston Corners PA) → franchisee
1980 (Williamsburg, with Gene Chismer) → ~30 built → sold 1996 → repurchased 2003 →
today N&R Dining / MHF Dining across VA & NC.
