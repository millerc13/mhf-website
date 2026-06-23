#!/usr/bin/env python3
"""Generates the MHF static site into site/ from a shared template.

Run:  python3 build.py
Each page shares one header/footer/brand block so the branding never drifts.
"""

import pathlib

OUT = pathlib.Path(__file__).parent / "site"

# ---------------------------------------------------------------- brand mark
LOGO = """<svg viewBox="0 0 64 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="MHF umbrella mark">
  <path d="M32 4 C17 4 6.5 15 4.5 28.5 C8.5 24 15 24 18.5 28.5 C22 24 28.5 24 32 28.5 C35.5 24 42 24 45.5 28.5 C49 24 55.5 24 59.5 28.5 C57.5 15 47 4 32 4 Z" fill="{gold}"/>
  <rect x="30.6" y="6" width="2.8" height="40" rx="1.4" fill="{green}"/>
  <path d="M33.4 46 c0 7 -10.5 7 -10.5 0" fill="none" stroke="{green}" stroke-width="2.8" stroke-linecap="round"/>
  <circle cx="18" cy="36" r="2.6" fill="{gold}"/>
  <circle cx="32" cy="55" r="0" fill="none"/>
  <circle cx="46" cy="36" r="2.6" fill="{gold}"/>
</svg>"""

LOGO_HEADER = LOGO.format(gold="#c79a3b", green="#1e3a2f")
LOGO_FOOTER = LOGO.format(gold="#c79a3b", green="#faf6ed")

# ---------------------------------------------------------------- chrome
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MHF — My Happy Family">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://mhf-website.vercel.app/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://mhf-website.vercel.app/assets/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500..800&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;1,9..144,300..700,0..100,0..1&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="stylesheet" href="css/styles.css">
{extra_head}
</head>
<body>
"""

NAV = f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html">
      {LOGO_HEADER}
      <span class="brand-text">
        <span class="brand-name">MHF</span><br>
        <span class="brand-sub">My&nbsp;Happy&nbsp;Family</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
    <ul class="nav-links">
      <li><a href="about.html">About</a></li>
      <li><a href="portfolio.html">Portfolio</a></li>
      <li><a href="development.html">Development</a></li>
      <li><a href="operations.html">Operations</a></li>
      <li><a href="management.html">Management</a></li>
      <li><a href="team.html">Team</a></li>
      <li><a href="careers.html">Join Our Team</a></li>
      <li><a class="nav-cta" href="contact.html">Contact</a></li>
    </ul>
  </div>
</header>
"""

TICKER_ITEMS = "".join(
    f"<span>{name}</span>"
    for name in [
        "The Orchards", "Yalick Farms", "Virginia Car Wash Co.", "Madison Crest",
        "22 Burger Kings", "Ewell Station", "Newport Circle", "Hanover Corner",
        "Yalick Shoppes", "Est. 1980",
    ]
)

FOOTER = f"""<div class="brand-ticker" aria-hidden="true">
  <div class="ticker-track">{TICKER_ITEMS}{TICKER_ITEMS}</div>
</div>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        {LOGO_FOOTER}
        <p>A second-generation family company. Development, operations and
        management — all under one umbrella.</p>
        <div class="footer-social">
          <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.22 8.09h4.56V23H.22zM8.34 8.09h4.37v2.04h.06c.61-1.15 2.1-2.36 4.32-2.36 4.62 0 5.47 3.04 5.47 7v8.23h-4.55v-7.3c0-1.74-.03-3.98-2.42-3.98-2.43 0-2.8 1.9-2.8 3.85V23H8.34z"/></svg></a>
          <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zM12 16a4 4 0 1 1 4-4 4 4 0 0 1-4 4zm6.4-11.85a1.44 1.44 0 1 0 1.44 1.44 1.44 1.44 0 0 0-1.44-1.44z"/></svg></a>
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.5h-2.8V24C19.62 23.09 24 18.1 24 12.07z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="portfolio.html">Portfolio</a></li>
          <li><a href="team.html">Team</a></li>
          <li><a href="careers.html">Join Our Team</a></li>
        </ul>
      </div>
      <div>
        <h4>What We Do</h4>
        <ul>
          <li><a href="development.html">Development</a></li>
          <li><a href="operations.html">Operations</a></li>
          <li><a href="management.html">Management</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit Us</h4>
        <ul>
          <li>423 N. Boundary St., Suite 100<br>Williamsburg, VA 23185</li>
          <li>Office: <a href="tel:+17575643175">757.564.3175</a></li>
          <li><a href="mailto:info@mhfamily.com">info@mhfamily.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 MHF — My Happy Family. All rights reserved.</span>
      <span>Development &middot; Operations &middot; Management</span>
    </div>
  </div>
</footer>
<script src="js/main.js"></script>
{{extra_scripts}}
<!-- CLIENT PREVIEW ONLY — color palette previewer. Remove this line + js/theme-switcher.js before launch. -->
<script src="js/theme-switcher.js"></script>
</body>
</html>
"""


def page(filename, title, desc, body, extra_head="", extra_scripts=""):
    html = (
        HEAD.format(title=title, desc=desc, extra_head=extra_head)
        + NAV
        + '<main id="main">'
        + body
        + '</main>'
        + FOOTER.format(extra_scripts=extra_scripts)
    )
    (OUT / filename).write_text(html)
    print(f"  wrote site/{filename}")


# ================================================================ HOME
STAMP_BADGE = """<div class="stamp-badge" aria-hidden="true">
  <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
    <circle class="stamp-disc" cx="80" cy="80" r="78" fill="#122419" stroke="rgba(200,151,58,0.55)" stroke-width="1.5"/>
    <defs><path id="stamp-circ" d="M80,80 m-64,0 a64,64 0 1,1 128,0 a64,64 0 1,1 -128,0"/></defs>
    <g class="stamp-ring">
      <text font-family="Archivo, sans-serif" font-size="12.5" font-weight="600" letter-spacing="3.4" fill="rgba(247,241,226,0.78)">
        <textPath href="#stamp-circ">EST. 1980 &#183; WILLIAMSBURG, VA &#183; MY HAPPY FAMILY &#183;</textPath>
      </text>
    </g>
    <circle cx="80" cy="80" r="47" fill="none" stroke="rgba(247,241,226,0.35)" stroke-width="1.5"/>
    <g transform="translate(48,50)">
      <path d="M32 4 C17 4 6.5 15 4.5 28.5 C8.5 24 15 24 18.5 28.5 C22 24 28.5 24 32 28.5 C35.5 24 42 24 45.5 28.5 C49 24 55.5 24 59.5 28.5 C57.5 15 47 4 32 4 Z" fill="#c8973a"/>
      <rect x="30.6" y="6" width="2.8" height="40" rx="1.4" fill="#f7f1e2"/>
      <path d="M33.4 46 c0 7 -10.5 7 -10.5 0" fill="none" stroke="#f7f1e2" stroke-width="2.8" stroke-linecap="round"/>
    </g>
  </svg>
</div>"""

HOME = f"""
<div class="hero">
  <div class="container">
    <span class="eyebrow">My Happy Family &middot; Williamsburg, Virginia</span>
    <h1>Family built. <em>Community grown.</em></h1>
    <p class="lead">For over four decades, the Naparlo family has built restaurants,
    neighborhoods and businesses the same way we'd build anything for our own family —
    with care, grit and a handshake you can count on. Development, operations and
    management — one family behind all of it.</p>
    <div class="hero-pillars">
      <a href="development.html">Development</a>
      <span class="pillar-sep" aria-hidden="true">&#10022;</span>
      <a href="operations.html">Operations</a>
      <span class="pillar-sep" aria-hidden="true">&#10022;</span>
      <a href="management.html">Management</a>
    </div>
    <div class="hero-actions">
      <a class="btn btn-gold" href="portfolio.html">Explore Our Portfolio</a>
      <a class="btn btn-outline" href="about.html">Our Story</a>
    </div>
    {STAMP_BADGE}
  </div>
</div>

<section>
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">What We Do</span>
      <h2>One family. Three disciplines.</h2>
      <p class="lead">We operate like a mom &amp; pop — because we are one. But the
      reach of our work might surprise you.</p>
    </div>
    <div class="card-grid">
      <div class="card reveal">
        <div class="card-head">
          <div class="card-icon"><svg fill="none" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5M3.75 21V9.35a1.5 1.5 0 01.66-1.24l6.75-4.6a1.5 1.5 0 011.68 0l6.75 4.6a1.5 1.5 0 01.66 1.24V21M9 21v-5.25A1.75 1.75 0 0110.75 14h2.5A1.75 1.75 0 0115 15.75V21"/></svg></div>
          <h3>Development</h3>
        </div>
        <p>From raw land to thriving communities. We acquire, entitle and build —
        residential neighborhoods, retail centers and commercial sites across
        Virginia and Pennsylvania.</p>
        <a class="card-link" href="development.html">See our projects</a>
      </div>
      <div class="card reveal">
        <div class="card-head">
          <div class="card-icon"><svg fill="none" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12a7.5 7.5 0 0015 0m-15 0a7.5 7.5 0 1115 0m-15 0H3m16.5 0H21m-9-7.5V3m0 18v-1.5"/></svg></div>
          <h3>Operations</h3>
        </div>
        <p>Twenty-two Burger King restaurants, a convenience store and the Virginia
        Car Wash Co. — run hands-on, every day, by people who know your name.</p>
        <a class="card-link" href="operations.html">How we operate</a>
      </div>
      <div class="card reveal">
        <div class="card-head">
          <div class="card-icon"><svg fill="none" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.5 20.25a7.5 7.5 0 0115 0v.75h-15v-.75z"/></svg></div>
          <h3>Management</h3>
        </div>
        <p>Commercial and multi-family property management with an owner's eye —
        because we own what we manage. Our tenants are neighbors, not numbers.</p>
        <a class="card-link" href="management.html">What we manage</a>
      </div>
    </div>
  </div>
</section>

<section class="green-band tight">
  <div class="container">
    <div class="stats-row">
      <div class="reveal"><div class="stat-num">45+</div><div class="stat-label">Years in Business</div></div>
      <div class="reveal"><div class="stat-num">30+</div><div class="stat-label">Burger Kings Built</div></div>
      <div class="reveal"><div class="stat-num">22</div><div class="stat-label">Restaurants Operating</div></div>
      <div class="reveal"><div class="stat-num">2</div><div class="stat-label">Generations of Family</div></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Where You'll Find Us</span>
      <h2>One family, <em>two states.</em></h2>
      <p class="lead">From the Historic Triangle of Virginia to the Back Mountain of
      Pennsylvania — every pin is something the family built, runs or manages.</p>
    </div>
    <div class="map-stage reveal">
      <div id="home-map"></div>
      <aside class="loc-carousel" aria-label="Featured locations">
        <div class="loc-slide" id="loc-slide">
          <div class="loc-img"></div>
          <div class="loc-body">
            <h3></h3>
            <div class="loc-meta">
              <span class="prop-tag"></span>
              <span class="loc-loc"></span>
            </div>
            <p></p>
          </div>
        </div>
        <div class="loc-progress" aria-hidden="true"><span id="loc-progress-bar"></span></div>
        <div class="loc-dots" id="loc-dots"></div>
      </aside>
    </div>
    <div class="home-map-foot reveal">
      <p>Every spot tells a story — tap a pin or let the tour run.</p>
      <a class="btn btn-green" href="portfolio.html">Explore the Full Portfolio</a>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Our Story</span>
        <h2>It started with one teenager flipping burgers.</h2>
        <p class="lead">In 1980, after working his way up from an hourly Burger King
        job he took at sixteen, Joseph "Just J." Naparlo became a Burger King
        franchisee. Forty-five years and thirty-plus restaurants later, MHF is still
        what it has always been: a family taking care of its people, its properties
        and its communities.</p>
        <a class="btn btn-green" href="about.html" style="margin-top:26px;">Read the Full Story</a>
      </div>
      <div class="reveal">
        <blockquote class="pull-quote">"Many things are possible through hard work
        and determination — and a little help from the Man upstairs."
        <cite>— J. Naparlo, Founder</cite></blockquote>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">The Family Way</span>
      <h2>How we work</h2>
      <p class="lead">Three habits, two generations, one standard.</p>
    </div>
    <div class="way-grid">
      <div class="way reveal">
        <span class="way-num">01</span>
        <h3>Show up</h3>
        <p>J. started behind a Burger King counter at sixteen. Fifty years on, the
        family still walks its own restaurants, sites and properties — nothing is
        run from a distance.</p>
      </div>
      <div class="way reveal">
        <span class="way-num">02</span>
        <h3>Build to keep</h3>
        <p>We develop what we intend to own and manage. When the builder, landlord
        and operator are the same family, quality isn't a promise — it's
        self-interest.</p>
      </div>
      <div class="way reveal">
        <span class="way-num">03</span>
        <h3>Know your name</h3>
        <p>Tenants, team members and guests deal with people, not departments. It's
        called My Happy Family because we mean it.</p>
      </div>
    </div>
    <div style="text-align:center;margin-top:48px;">
      <a class="btn btn-green" href="portfolio.html">View the Full Portfolio &amp; Map</a>
    </div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <span class="eyebrow">Join Our Team</span>
    <h2>Come grow with a company that knows your name.</h2>
    <p class="lead" style="margin:0 auto;">We're hiring across operations, construction
    and the home office.</p>
    <a class="btn btn-gold" href="careers.html">See Open Positions</a>
  </div>
</section>
"""

# ================================================================ ABOUT
ABOUT = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">About MHF</span>
    <h1>Our story is a <em>family story.</em></h1>
    <p class="lead">MHF stands for My Happy Family — and we mean it. Everything we
    build, operate and manage flows from one simple idea: take care of people the
    way you'd take care of your own.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">The Founder</span>
        <h2>Joseph J. Naparlo</h2>
        <p class="lead">Known to most as <strong>"Just J."</strong>, J. Naparlo is the
        patriarch, visionary and driving force of what has now evolved into MHF.</p>
        <p style="margin-top:18px;color:var(--ink-soft);">His inspiring life story is
        a reminder that many things are possible through hard work and determination.
        Having lost both parents at a young age, J. had no option but to jump into
        work. He started at Burger King as an hourly employee at age sixteen and
        worked his way up over several years until he found a partner, Gene Chismer,
        who backed him in becoming a Burger King franchisee in 1980. Together they
        built over thirty Burger Kings from the ground up.</p>
        <p style="margin-top:14px;color:var(--ink-soft);">Having never gone to
        college, J. learned most of what he knows through trial and error, and he
        relied heavily on key mentors throughout his life. J. often gives credit to
        "the Man upstairs for taking good care of him." He is a relentless family
        man — a proud father of three and grandfather of nine.</p>
      </div>
      <div class="reveal">
        <div class="card" style="border-top-color:var(--green);">
          <div class="profile-head">
            <span class="avatar avatar-sm"><img src="assets/photos/john-avatar.jpg" alt="John Naparlo — cartoon avatar"></span>
            <h3>John Naparlo</h3>
          </div>
          <p style="margin-top:8px;">The second generation of MHF leadership, John
          carries the family standard forward — guiding the company's restaurant
          operations, development projects and property portfolio from the family's
          Williamsburg home office. A Williamsburg native and James Madison
          University alum, John believes — like his father — that the best way to
          grow a business is to show up, do the work and treat every employee,
          tenant and guest like family.</p>
        </div>
        <blockquote class="pull-quote" style="margin-top:34px;">"We operate like a
        mom and pop — we just happen to touch a lot of different things."
        <cite>— John Naparlo</cite></blockquote>
      </div>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">How We Got Here</span>
      <h2>Four decades, one family</h2>
    </div>
    <div class="timeline">
      <div class="timeline-item reveal">
        <div class="timeline-year">1967</div>
        <h3>An hourly job at sixteen</h3>
        <p>After losing both parents at a young age, J. Naparlo goes to work at the
        Wyoming Valley's first Burger King in Kingston Corners, Pennsylvania — and
        starts climbing, from crew to manager to regional director of operations.</p>
      </div>
      <div class="timeline-item reveal">
        <div class="timeline-year">1980</div>
        <h3>Becoming a franchisee</h3>
        <p>Backed by partner Gene Chismer, J. opens his first Burger King in
        Williamsburg, Virginia. Over the years that follow, they build roughly
        thirty restaurants from the ground up.</p>
      </div>
      <div class="timeline-item reveal">
        <div class="timeline-year">1996 &amp; 2003</div>
        <h3>Sold — and bought back</h3>
        <p>J. sells the Williamsburg restaurant group in 1996. When the buyer later
        stumbles, the family buys its restaurants back. Burgers, it turns out, are
        in the blood.</p>
      </div>
      <div class="timeline-item reveal">
        <div class="timeline-year">Growth</div>
        <h3>Beyond the restaurant</h3>
        <p>Restaurant success funds land acquisition, retail development and
        residential communities across Virginia and Pennsylvania — including the
        60-acre Yalick Farms planned community and the Shoppes at Yalick Farms in
        the Back Mountain of Pennsylvania — plus a car wash, a c-store and a
        growing management portfolio.</p>
      </div>
      <div class="timeline-item reveal">
        <div class="timeline-year">Today</div>
        <h3>MHF — My Happy Family</h3>
        <p>Two generations strong, MHF brings development, operations and management
        together under one name: 22 Burger King restaurants across Virginia and
        North Carolina, the Virginia Car Wash Co., and a portfolio of residential,
        retail and commercial properties.</p>
      </div>
    </div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <h2>Meet the people behind the name.</h2>
    <a class="btn btn-gold" href="team.html">Meet the Team</a>
  </div>
</section>
"""

# ================================================================ DEVELOPMENT
DEVELOPMENT = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Development</span>
    <h1>From raw land to <em>thriving communities.</em></h1>
    <p class="lead">MHF acquires, entitles and develops land for residential
    neighborhoods, retail centers and commercial use — projects we're proud to put
    the family name on.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">What We Do</span>
        <h2>Built from the ground up — literally.</h2>
        <p class="lead">We've been building since 1980, when the family put up its
        first Burger King. Thirty-plus restaurants later, that same ground-up
        discipline drives our land acquisition and development work.</p>
        <ul class="check-list">
          <li><strong>Land acquisition</strong> — identifying and securing well-located
          parcels across Virginia and Pennsylvania.</li>
          <li><strong>Entitlement &amp; planning</strong> — zoning, engineering and
          approvals, managed start to finish.</li>
          <li><strong>Residential development</strong> — single-family and
          multi-family communities built for the long haul.</li>
          <li><strong>Commercial &amp; retail construction</strong> — build-to-suit
          and pad sites for national and local tenants.</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="card">
          <span class="eyebrow">Flagship Projects</span>
          <h3 style="margin-top:6px;">Yalick Farms</h3>
          <p>A 60-acre planned community in the Back Mountain of Pennsylvania —
          townhomes, condos, patio homes and apartments, developed together with
          the Shoppes at Yalick Farms retail center.</p>
          <h3 style="margin-top:22px;">The Orchards</h3>
          <p>A signature residential community and a model for how MHF builds:
          thoughtful planning, quality construction, lasting value.</p>
          <h3 style="margin-top:22px;">Madison Crest</h3>
          <p>Residential development carrying the family standard into its next
          neighborhood.</p>
          <a class="card-link" href="portfolio.html">See every project on the map</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="green-band">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Start to Finish</span>
      <h2>One family, every step</h2>
    </div>
    <div class="step-row">
      <div class="step reveal"><div class="step-head"><span class="step-num">1</span><h3>Acquire</h3></div>
        <p>Find the right ground — well-located parcels we'd be proud to hold for decades.</p></div>
      <div class="step reveal"><div class="step-head"><span class="step-num">2</span><h3>Entitle</h3></div>
        <p>Zoning, engineering and approvals, managed in-house from first sketch to final stamp.</p></div>
      <div class="step reveal"><div class="step-head"><span class="step-num">3</span><h3>Build</h3></div>
        <p>Ground-up construction with the discipline of a family that has built 30+ restaurants.</p></div>
      <div class="step reveal"><div class="step-head"><span class="step-num">4</span><h3>Manage</h3></div>
        <p>We keep what we build — and manage it with an owner's eye, because we are the owner.</p></div>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Land Holdings</span>
      <h2>Ground ready for what's next</h2>
      <p class="lead">MHF maintains a portfolio of vacant land positioned for future
      development — including sites at Oilville, and lots in Chesapeake, Armistead
      and New Kent.</p>
    </div>
    <div style="margin-top:10px;">
      <a class="btn btn-green" href="contact.html?topic=development">Talk to Us About a Site</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Development Team</span>
      <h2>Who's behind the work</h2>
    </div>
    <div class="team-grid" style="max-width:780px;">
      <div class="team-card reveal">
        <div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Perry&backgroundColor=f1ead9" alt="Perry Dunford — cartoon avatar"></div>
        <h3>Perry Dunford</h3>
        <div class="team-role">Development</div>
        <div class="team-div">Land, entitlement &amp; construction</div>
      </div>
      <div class="team-card reveal">
        <div class="avatar"><img src="assets/photos/john-avatar.jpg" alt="John Naparlo — cartoon avatar"></div>
        <h3>John Naparlo</h3>
        <div class="team-role">Principal</div>
        <div class="team-div">Strategy &amp; project leadership</div>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================ OPERATIONS
OPERATIONS = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Operations</span>
    <h1>Run every day, <em>the family way.</em></h1>
    <p class="lead">Twenty-two Burger King restaurants, a convenience store and the
    Virginia Car Wash Co. — operated hands-on by people who've spent their careers
    in the business.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="card-grid">
      <div class="card reveal">
        <span class="eyebrow">Restaurants</span>
        <h3>22 Burger King Locations</h3>
        <p>The family has been a Burger King franchisee since 1980 and has built more
        than thirty restaurants from the ground up. Today we operate twenty-two
        locations across Virginia and North Carolina — each one led by a Restaurant
        General Manager empowered to run it like their own.</p>
      </div>
      <div class="card reveal">
        <span class="eyebrow">Car Wash</span>
        <h3>Virginia Car Wash Co.</h3>
        <p>Our express tunnel wash in Chesapeake, Virginia brings MHF's operational
        standard to a whole new lane — fast, friendly and spotless, with free
        vacuums, monthly memberships and a fleet program.</p>
      </div>
      <div class="card reveal">
        <span class="eyebrow">Convenience</span>
        <h3>C-Store</h3>
        <p>Neighborhood convenience, run with the same care as everything else
        with the family's name on it.</p>
      </div>
    </div>
  </div>
</section>

<section class="green-band tight">
  <div class="container">
    <div class="stats-row">
      <div class="reveal"><div class="stat-num">22</div><div class="stat-label">Burger Kings</div></div>
      <div class="reveal"><div class="stat-num">1980</div><div class="stat-label">Franchisee Since</div></div>
      <div class="reveal"><div class="stat-num">100s</div><div class="stat-label">Team Members</div></div>
      <div class="reveal"><div class="stat-num">7</div><div class="stat-label">Days a Week</div></div>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Operations Team</span>
      <h2>The people who keep it running</h2>
      <p class="lead">Operations is the heartbeat of MHF — and these are the folks
      with their hands on it every day, alongside our Burger King Restaurant
      General Managers.</p>
    </div>
    <div class="team-grid">
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jim&backgroundColor=f1ead9" alt="Jim — cartoon avatar"></div><h3>Jim</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=JP&backgroundColor=f1ead9" alt="JP — cartoon avatar"></div><h3>JP</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Becky&backgroundColor=f1ead9" alt="Becky — cartoon avatar"></div><h3>Becky</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Cynthia&backgroundColor=f1ead9" alt="Cynthia — cartoon avatar"></div><h3>Cynthia</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jon&backgroundColor=f1ead9" alt="Jon — cartoon avatar"></div><h3>Jon</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Patti&backgroundColor=f1ead9" alt="Patti — cartoon avatar"></div><h3>Patti</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Ken&backgroundColor=f1ead9" alt="Ken — cartoon avatar"></div><h3>Ken</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Dawn&backgroundColor=f1ead9" alt="Dawn — cartoon avatar"></div><h3>Dawn</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jeff&backgroundColor=f1ead9" alt="Jeff — cartoon avatar"></div><h3>Jeff</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Brian&backgroundColor=f1ead9" alt="Brian — cartoon avatar"></div><h3>Brian</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Lauren&backgroundColor=f1ead9" alt="Lauren — cartoon avatar"></div><h3>Lauren</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=RGM&backgroundColor=f1ead9" alt="RGMs — cartoon avatar"></div><h3>Our BK RGMs</h3><div class="team-role">Restaurant General Managers</div></div>
    </div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <span class="eyebrow">Your Move</span>
    <h2>Ever wanted to run a restaurant like it's yours?</h2>
    <p class="lead" style="margin:0 auto;">Crew, shift leaders, RGMs and a Director
    of Operations — we promote from within, and the founder started at sixteen.</p>
    <a class="btn btn-gold" href="careers.html">See Open Positions</a>
  </div>
</section>
"""

# ================================================================ MANAGEMENT
MANAGEMENT = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Management</span>
    <h1>Managed with <em>an owner's eye.</em></h1>
    <p class="lead">MHF manages commercial and multi-family properties across our
    portfolio — and because we own what we manage, every decision is made like
    it's our own front yard. It is.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">What We Manage</span>
        <h2>Commercial and multi-family, under one roof</h2>
        <ul class="check-list">
          <li><strong>Multi-family communities</strong> — including The Orchards,
          Yalick Farms and Madison Crest.</li>
          <li><strong>Retail centers</strong> — Ewell Station, BK Shoppes and Yalick
          Shoppes, home to tenants like Starbucks, Verizon, Mattress Warehouse,
          WaWa, Jimmy John's and Fresenius.</li>
          <li><strong>Commercial properties</strong> — office and single-tenant
          buildings managed end to end.</li>
          <li><strong>Leasing &amp; tenant relations</strong> — handled directly by
          our family office in Williamsburg. No call centers, ever.</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="card">
          <span class="eyebrow">Flagship Properties</span>
          <h3 style="margin-top:6px;">Ewell Station</h3>
          <p>Retail center anchored by Starbucks, Verizon and Mattress Warehouse.</p>
          <h3 style="margin-top:22px;">The Orchards</h3>
          <p>Multi-family community managed by the same family that built it.</p>
          <h3 style="margin-top:22px;">Yalick Shoppes</h3>
          <p>Neighborhood retail serving the Yalick Farms community.</p>
          <a class="card-link" href="portfolio.html">Browse the full portfolio</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <h2>Looking to lease with us?</h2>
    <p class="lead" style="margin:0 auto;">Retail, commercial or residential — talk
    directly to the people who own the property.</p>
    <a class="btn btn-gold" href="contact.html?topic=leasing">Get in Touch</a>
  </div>
</section>
"""

# ================================================================ TEAM
TEAM = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Our Team</span>
    <h1>The family — and the family <em>we've hired.</em></h1>
    <p class="lead">Some of us are Naparlos. The rest of us might as well be. Meet
    the people who make MHF what it is.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Leadership</span>
      <h2>Two generations at the helm</h2>
    </div>
    <div class="team-grid" style="max-width:560px;">
      <div class="team-card reveal">
        <div class="avatar"><img src="assets/photos/j-avatar.jpg" alt="J. Naparlo — cartoon avatar"></div>
        <h3>J. Naparlo</h3>
        <div class="team-role">Founder &amp; Patriarch</div>
        <div class="team-div">"Just J." — building since 1980</div>
      </div>
      <div class="team-card reveal">
        <div class="avatar"><img src="assets/photos/john-avatar.jpg" alt="John Naparlo — cartoon avatar"></div>
        <h3>John Naparlo</h3>
        <div class="team-role">Principal</div>
        <div class="team-div">Second-generation leadership</div>
      </div>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Development</span>
      <h2>Development</h2>
    </div>
    <div class="team-grid" style="max-width:280px;">
      <div class="team-card reveal">
        <div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Perry&backgroundColor=f1ead9" alt="Perry Dunford — cartoon avatar"></div>
        <h3>Perry Dunford</h3>
        <div class="team-role">Development</div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Operations</span>
      <h2>Operations</h2>
      <p class="lead">Alongside our Burger King Restaurant General Managers, who run
      their stores like their own.</p>
    </div>
    <div class="team-grid">
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jim&backgroundColor=f1ead9" alt="Jim — cartoon avatar"></div><h3>Jim</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=JP&backgroundColor=f1ead9" alt="JP — cartoon avatar"></div><h3>JP</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Becky&backgroundColor=f1ead9" alt="Becky — cartoon avatar"></div><h3>Becky</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Cynthia&backgroundColor=f1ead9" alt="Cynthia — cartoon avatar"></div><h3>Cynthia</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jon&backgroundColor=f1ead9" alt="Jon — cartoon avatar"></div><h3>Jon</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Patti&backgroundColor=f1ead9" alt="Patti — cartoon avatar"></div><h3>Patti</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Ken&backgroundColor=f1ead9" alt="Ken — cartoon avatar"></div><h3>Ken</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Dawn&backgroundColor=f1ead9" alt="Dawn — cartoon avatar"></div><h3>Dawn</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Jeff&backgroundColor=f1ead9" alt="Jeff — cartoon avatar"></div><h3>Jeff</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Brian&backgroundColor=f1ead9" alt="Brian — cartoon avatar"></div><h3>Brian</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=Lauren&backgroundColor=f1ead9" alt="Lauren — cartoon avatar"></div><h3>Lauren</h3><div class="team-role">Operations</div></div>
      <div class="team-card reveal"><div class="avatar"><img src="https://api.dicebear.com/9.x/adventurer/svg?seed=RGM&backgroundColor=f1ead9" alt="RGMs — cartoon avatar"></div><h3>Our BK RGMs</h3><div class="team-role">Restaurant General Managers</div></div>
    </div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <h2>There's a seat at the table for you.</h2>
    <a class="btn btn-gold" href="careers.html">Join Our Team</a>
  </div>
</section>
"""

# ================================================================ CAREERS
CAREERS = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Join Our Team</span>
    <h1>Work somewhere that <em>knows your name.</em></h1>
    <p class="lead">From restaurant crews to construction sites to the home office,
    MHF hires people who take pride in their work — and treats them like family,
    because that's the whole point of the name.</p>
  </div>
</div>

<section class="tight">
  <div class="container">
    <div class="card-grid">
      <div class="card reveal">
        <span class="eyebrow">Stability</span>
        <h3>Here since 1980</h3>
        <p>Two generations, forty-five years, and restaurants we sold once and
        bought right back. The family doesn't leave — and doesn't let go of good
        people either.</p>
      </div>
      <div class="card reveal">
        <span class="eyebrow">No Ceiling</span>
        <h3>The founder started at 16</h3>
        <p>J. went from hourly crew to owning the restaurants. We promote from
        within because that's how this whole company happened.</p>
      </div>
      <div class="card reveal">
        <span class="eyebrow">Family, For Real</span>
        <h3>People, not headcount</h3>
        <p>It says "My Happy Family" on the door. You'll know the owners by name,
        and they'll know yours — that's the deal.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Open Positions</span>
      <h2>Current openings</h2>
    </div>
    <div class="job-list">
      <div class="job-card reveal">
        <div>
          <h3>Director of Operations</h3>
          <div class="job-meta">Full-time &middot; Williamsburg, VA &middot; Restaurant Operations</div>
        </div>
        <a class="btn btn-green" href="contact.html?topic=careers">Apply</a>
      </div>
      <div class="job-card reveal">
        <div>
          <h3>Construction Manager</h3>
          <div class="job-meta">Full-time &middot; Williamsburg, VA &middot; Development</div>
        </div>
        <a class="btn btn-green" href="contact.html?topic=careers">Apply</a>
      </div>
      <div class="job-card reveal">
        <div>
          <h3>CPA</h3>
          <div class="job-meta">Full-time &middot; Williamsburg, VA &middot; Home Office</div>
        </div>
        <a class="btn btn-green" href="contact.html?topic=careers">Apply</a>
      </div>
      <div class="job-card reveal">
        <div>
          <h3>Administrative Assistant</h3>
          <div class="job-meta">Full-time &middot; Williamsburg, VA &middot; Home Office</div>
        </div>
        <a class="btn btn-green" href="contact.html?topic=careers">Apply</a>
      </div>
    </div>
  </div>
</section>

<section class="alt-band">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Restaurant Careers</span>
        <h2>Burger King crew and management</h2>
        <p class="lead">Our restaurants are always looking for great people — crew,
        shift leaders and Restaurant General Managers. J. started as an hourly
        employee at sixteen. There's no ceiling here.</p>
        <a class="btn btn-green" href="contact.html?topic=careers" style="margin-top:24px;">Ask About Restaurant Roles</a>
      </div>
      <div class="reveal">
        <div class="card">
          <h3>General Inquiries</h3>
          <p>Don't see your role listed? We still want to hear from you. Tell us
          what you're great at and we'll keep you in mind.</p>
          <a class="card-link" href="contact.html?topic=general">Send a general inquiry</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ================================================================ CONTACT
CONTACT = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Contact</span>
    <h1><em>Say hello.</em></h1>
    <p class="lead">Leasing, development, careers or just a good idea — there's a
    real person on the other end, and we'd love to hear from you.</p>
  </div>
</div>

<section>
  <div class="container">
    <div class="contact-grid">
      <div class="contact-aside reveal">
        <div class="office-card">
          <div id="office-map" aria-label="Map showing the MHF family office on North Boundary Street, Williamsburg"></div>
          <div class="office-body">
            <span class="eyebrow">The Family Office</span>
            <h3>423 N. Boundary St., Suite 100<br>Williamsburg, VA 23185</h3>
            <div class="office-rows">
              <a class="office-row" href="tel:+17575643175">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/></svg>
                757.564.3175</a>
              <a class="office-row" href="mailto:info@mhfamily.com">
                <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/></svg>
                info@mhfamily.com</a>
            </div>
            <div class="office-social" aria-label="MHF on social media">
              <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.22 8.09h4.56V23H.22zM8.34 8.09h4.37v2.04h.06c.61-1.15 2.1-2.36 4.32-2.36 4.62 0 5.47 3.04 5.47 7v8.23h-4.55v-7.3c0-1.74-.03-3.98-2.42-3.98-2.43 0-2.8 1.9-2.8 3.85V23H8.34z"/></svg></a>
              <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zM12 16a4 4 0 1 1 4-4 4 4 0 0 1-4 4zm6.4-11.85a1.44 1.44 0 1 0 1.44 1.44 1.44 1.44 0 0 0-1.44-1.44z"/></svg></a>
              <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.5h-2.8V24C19.62 23.09 24 18.1 24 12.07z"/></svg></a>
            </div>
          </div>
        </div>
        <p class="contact-promise">No phone trees, no ticket numbers. Call the office
        and a person picks up — that's the point of a family company.</p>
      </div>
      <form class="contact-form reveal">
        <div class="form-intro">
          <h3>Send us a note</h3>
          <p>Tell us a little about what you need — a real person reads every
          message and will point you to the right member of the family.</p>
        </div>
        <div class="form-row">
          <div>
            <label for="name">Name</label>
            <input id="name" name="name" type="text" autocomplete="name" required>
          </div>
          <div>
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
        </div>
        <div class="form-row">
          <div>
            <label for="phone">Phone <span class="label-soft">(optional)</span></label>
            <input id="phone" name="phone" type="tel" autocomplete="tel">
          </div>
          <div>
            <label for="topic">I'm interested in</label>
            <select id="topic" name="topic">
              <option value="general">General inquiry</option>
              <option value="leasing">Leasing — retail or commercial</option>
              <option value="residential">Leasing — residential</option>
              <option value="development">Development &amp; land</option>
              <option value="careers">Careers</option>
            </select>
          </div>
        </div>
        <div>
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="6" required
            placeholder="What can we help with?"></textarea>
        </div>
        <div class="form-foot">
          <button class="btn btn-gold" type="submit">Send Message</button>
          <p class="form-note">We only use your details to reply — never for
          mailing lists.</p>
        </div>
      </form>
    </div>
  </div>
</section>
"""

# ================================================================ PORTFOLIO
PORTFOLIO = """
<div class="hero page-hero">
  <div class="container">
    <span class="eyebrow">Portfolio</span>
    <h1>One family, <em>every property.</em></h1>
    <p class="lead">Restaurants, residential communities, retail centers and land
    holdings across Virginia and Pennsylvania. Tap a pin or browse the list below.</p>
  </div>
</div>

<section class="tight">
  <div class="container">
    <div id="property-map"></div>
    <div class="filter-bar" id="filter-bar" role="group" aria-label="Filter properties by category">
      <button class="filter-btn" data-filter="residential" aria-pressed="false">Residential</button>
      <button class="filter-btn" data-filter="operations" aria-pressed="false">Operations</button>
      <button class="filter-btn" data-filter="retail" aria-pressed="false">Retail</button>
      <button class="filter-btn" data-filter="land" aria-pressed="false">Vacant Land</button>
    </div>
    <p class="results-line" id="results-line" aria-live="polite"></p>
    <div class="property-grid" id="property-grid"></div>
  </div>
</section>

<section class="green-band cta-band">
  <div class="container reveal">
    <h2>Interested in one of our properties?</h2>
    <a class="btn btn-gold" href="contact.html?topic=leasing">Contact the Family Office</a>
  </div>
</section>
"""

PORTFOLIO_HEAD = """<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">"""
PORTFOLIO_SCRIPTS = """<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="js/properties.js"></script>
<script src="js/portfolio.js"></script>"""
HOME_SCRIPTS = """<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="js/properties.js"></script>
<script src="js/home-map.js"></script>"""


def main():
    OUT.mkdir(exist_ok=True)
    page("index.html", "MHF — My Happy Family | Development · Operations · Management",
         "MHF is a second-generation family company in Williamsburg, VA: land development, Burger King restaurant operations, and commercial & multi-family property management.",
         HOME, extra_head=PORTFOLIO_HEAD, extra_scripts=HOME_SCRIPTS)
    page("about.html", "About — MHF | My Happy Family",
         "The story of J. Naparlo and the family company behind 30+ Burger Kings, residential communities and a growing property portfolio.",
         ABOUT)
    page("portfolio.html", "Portfolio — MHF | My Happy Family",
         "Explore the MHF portfolio on an interactive map: residential communities, 22 Burger King restaurants, retail centers and land holdings.",
         PORTFOLIO, extra_head=PORTFOLIO_HEAD, extra_scripts=PORTFOLIO_SCRIPTS)
    page("development.html", "Development — MHF | My Happy Family",
         "Land acquisition, entitlement and ground-up development across Virginia and Pennsylvania — The Orchards, Yalick Farms, Madison Crest and more.",
         DEVELOPMENT)
    page("operations.html", "Operations — MHF | My Happy Family",
         "22 Burger King restaurants, a c-store and the Virginia Car Wash Co. — operated hands-on, the family way, since 1980.",
         OPERATIONS)
    page("management.html", "Management — MHF | My Happy Family",
         "Commercial and multi-family property management with an owner's eye — Ewell Station, The Orchards, Yalick Shoppes and more.",
         MANAGEMENT)
    page("team.html", "Team — MHF | My Happy Family",
         "Meet the two generations of family — and the family we've hired — behind MHF.",
         TEAM)
    page("careers.html", "Join Our Team — MHF | My Happy Family",
         "Open positions at MHF: Director of Operations, Construction Manager, CPA, Administrative Assistant — plus restaurant careers.",
         CAREERS)
    page("contact.html", "Contact — MHF | My Happy Family",
         "Contact MHF in Williamsburg, VA — leasing, development, careers and general inquiries.",
         CONTACT, extra_head=PORTFOLIO_HEAD,
         extra_scripts='<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n<script src="js/contact.js"></script>')
    print("done.")


if __name__ == "__main__":
    main()
