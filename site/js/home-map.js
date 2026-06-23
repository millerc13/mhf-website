// Homepage map + auto-rotating location carousel, kept in sync:
// the carousel advances -> the matching pin pulses gold;
// clicking a pin -> the carousel jumps to that property.
// Slides use the branded category placeholder images; a property's
// `photo` field (when John supplies a real photograph) overrides it.
(function () {
  const mapEl = document.getElementById('home-map');
  if (!mapEl || !window.L) return;

  const META = {
    residential: { label: 'Residential', color: '#1b3527' },
    operations: { label: 'Operations', color: '#c8973a' },
    retail: { label: 'Retail', color: '#7a5c33' },
    land: { label: 'Vacant Land', color: '#5d7d5a' },
  };

  const slideImg = (p) => p.photo || p.image || `assets/photos/placeholder-${p.category}.jpg`;
  const pinned = (window.MHF_PROPERTIES || []).filter((p) => p.coords);
  if (!pinned.length) return;

  // Order slides by geographic closeness (greedy nearest-neighbor tour)
  // so the fly-to animations glide between neighbors instead of leaping
  // across states on every slide.
  const remaining = pinned.slice();
  const slides = [remaining.shift()];
  while (remaining.length) {
    const at = slides[slides.length - 1].coords;
    let nearest = 0;
    let best = Infinity;
    remaining.forEach((p, i) => {
      const dy = p.coords[0] - at[0];
      const dx = (p.coords[1] - at[1]) * Math.cos((at[0] * Math.PI) / 180);
      const d = dy * dy + dx * dx;
      if (d < best) { best = d; nearest = i; }
    });
    slides.push(remaining.splice(nearest, 1)[0]);
  }

  // ---- Map ----
  // dragging off on touch devices: a one-finger pan would trap the page
  // swipe and make the page impossible to scroll past the map.
  const map = L.map(mapEl, {
    scrollWheelZoom: false,
    dragging: !L.Browser.mobile,
  });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  function pinSvg(color, w, h) {
    return (
      `<svg width="${w}" height="${h}" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">` +
      `<path d="M16 1C8 1 1.5 7.5 1.5 15.5 1.5 26 16 41 16 41s14.5-15 14.5-25.5C30.5 7.5 24 1 16 1z" ` +
      `fill="${color}" stroke="#f7f1e2" stroke-width="2"/>` +
      `<circle cx="16" cy="15.5" r="5.5" fill="#f7f1e2"/></svg>`
    );
  }

  function baseIcon(color) {
    return L.divIcon({
      className: '',
      html: pinSvg(color, 26, 34),
      iconSize: [26, 34],
      iconAnchor: [13, 33],
    });
  }

  function activeIcon() {
    return L.divIcon({
      className: '',
      html: `<span class="pin-wrap"><span class="pin-pulse"></span>${pinSvg('#c8973a', 38, 50)}</span>`,
      iconSize: [38, 50],
      iconAnchor: [19, 49],
    });
  }

  const slideMarkers = [];
  const allMarkers = pinned.map((p) => {
    const m = L.marker(p.coords, { icon: baseIcon(META[p.category].color) }).addTo(map);
    const slideIdx = slides.indexOf(p);
    if (slideIdx >= 0) {
      slideMarkers[slideIdx] = m;
      m.on('click', () => { setActive(slideIdx); restartTimer(); });
    } else {
      m.bindPopup(
        `<div class="map-popup"><span class="popup-tag">${META[p.category].label}</span>` +
        `<h4>${p.name}</h4><p>${p.location}</p></div>`
      );
    }
    return m;
  });

  map.fitBounds(L.featureGroup(allMarkers).getBounds().pad(0.16));

  // Close-up zoom per category — tight on buildings, wider on raw land
  const zoomFor = (p) => (p.category === 'land' ? 13 : 15);

  // ---- Carousel ----
  const imgEl = document.querySelector('.loc-img');
  const tagEl = document.querySelector('.loc-body .prop-tag');
  const nameEl = document.querySelector('.loc-body h3');
  const locEl = document.querySelector('.loc-loc');
  const blurbEl = document.querySelector('.loc-body p');
  const slideEl = document.getElementById('loc-slide');
  const dotsEl = document.getElementById('loc-dots');
  const barEl = document.getElementById('loc-progress-bar');
  const INTERVAL = 5200;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!slides.length || !slideEl) return;

  slides.forEach((p, i) => {
    const d = document.createElement('button');
    d.className = 'loc-dot';
    d.setAttribute('aria-label', p.name);
    d.addEventListener('click', () => { setActive(i); restartTimer(); });
    dotsEl.appendChild(d);
  });
  const dots = Array.from(dotsEl.children);

  // Warm the cache so the first lap never flashes a blank panel
  slides.forEach((p) => { new Image().src = slideImg(p); });

  let current = -1;
  let timer = null;

  function setActive(i) {
    if (i === current) return;
    if (current >= 0) {
      slideMarkers[current].setIcon(baseIcon(META[slides[current].category].color));
      slideMarkers[current].setZIndexOffset(0);
      dots[current].classList.remove('active');
      dots[current].removeAttribute('aria-current');
    }
    current = i;
    const p = slides[i];
    slideMarkers[i].setIcon(activeIcon());
    slideMarkers[i].setZIndexOffset(1000);
    dots[i].classList.add('active');
    dots[i].setAttribute('aria-current', 'true');

    // Fly in close on the active location
    map.flyTo(p.coords, zoomFor(p), { duration: 1.6, easeLinearity: 0.2 });

    slideEl.classList.remove('swap');
    void slideEl.offsetWidth; // restart the entrance animation
    imgEl.style.backgroundImage = `url('${slideImg(p)}')`;
    tagEl.textContent = META[p.category].label;
    nameEl.textContent = p.name;
    locEl.textContent = p.location;
    blurbEl.textContent = p.blurb;
    slideEl.classList.add('swap');

    if (barEl) {
      if (reduceMotion) {
        barEl.style.width = '100%';
      } else {
        barEl.style.transition = 'none';
        barEl.style.width = '0%';
        void barEl.offsetWidth;
        barEl.style.transition = `width ${INTERVAL}ms linear`;
        barEl.style.width = '100%';
      }
    }
  }

  function next() { setActive((current + 1) % slides.length); }

  function restartTimer() {
    clearInterval(timer);
    timer = setInterval(next, INTERVAL);
  }

  // No pause-on-hover: the progress bar is CSS-driven and keeps filling,
  // so a paused rotation reads as a bug. Clicking a dot or pin restarts
  // the timer, which is all the manual control needed.
  setActive(0);
  restartTimer();
})();
