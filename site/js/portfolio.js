// MHF portfolio — interactive map + filterable property list.
// Data lives in js/properties.js (window.MHF_PROPERTIES).

const CATEGORY_META = {
  residential: { label: 'Residential', color: '#1e3a2f', banner: '' },
  operations: { label: 'Operations', color: '#c79a3b', banner: 'banner-ops' },
  retail: { label: 'Retail', color: '#7a5c33', banner: 'banner-retail' },
  land: { label: 'Vacant Land', color: '#5d7d5a', banner: 'banner-land' },
};

const props = window.MHF_PROPERTIES || [];

// ---- Map ----
// dragging off on touch devices so page swipes aren't trapped by the map
const map = L.map('property-map', {
  scrollWheelZoom: false,
  dragging: !L.Browser.mobile,
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

function pinIcon(color) {
  return L.divIcon({
    className: '',
    html:
      `<svg width="32" height="42" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">` +
      `<path d="M16 1C8 1 1.5 7.5 1.5 15.5 1.5 26 16 41 16 41s14.5-15 14.5-25.5C30.5 7.5 24 1 16 1z" ` +
      `fill="${color}" stroke="#faf6ed" stroke-width="2"/>` +
      `<circle cx="16" cy="15.5" r="5.5" fill="#faf6ed"/></svg>`,
    iconSize: [32, 42],
    iconAnchor: [16, 41],
    popupAnchor: [0, -38],
  });
}

const markers = [];
props.forEach((p) => {
  if (!p.coords) return;
  const meta = CATEGORY_META[p.category];
  const m = L.marker(p.coords, { icon: pinIcon(meta.color) }).addTo(map);
  m.bindPopup(
    `<div class="map-popup"><span class="popup-tag">${meta.label}</span>` +
    `<h4>${p.name}</h4><p>${p.blurb}</p>` +
    `<p style="font-weight:600;color:#1e3a2f;">${p.location}</p></div>`
  );
  markers.push({ marker: m, category: p.category });
});

// Toggleable category filters — none selected means show everything
const activeCats = new Set();
const isShown = (category) => !activeCats.size || activeCats.has(category);

function fitTo() {
  const visible = markers.filter((m) => isShown(m.category));
  if (!visible.length) return;
  const group = L.featureGroup(visible.map((m) => m.marker));
  map.fitBounds(group.getBounds().pad(0.18));
}
fitTo();

// ---- Property cards ----
const grid = document.getElementById('property-grid');
const resultsLine = document.getElementById('results-line');

// Show how many properties sit behind each filter
document.querySelectorAll('.filter-btn').forEach((btn) => {
  const n = props.filter((p) => p.category === btn.dataset.filter).length;
  const span = document.createElement('span');
  span.className = 'filter-count';
  span.textContent = n;
  btn.appendChild(span);
});

function render() {
  grid.innerHTML = '';
  const shown = props.filter((p) => isShown(p.category));
  if (resultsLine) {
    const mapped = shown.filter((p) => p.coords).length;
    const scope = activeCats.size ? `${shown.length} ${shown.length === 1 ? 'property' : 'properties'}` : `all ${shown.length} properties`;
    resultsLine.textContent = `Showing ${scope} — ${mapped} on the map.`;
  }
  shown
    .forEach((p) => {
      const meta = CATEGORY_META[p.category];
      const card = document.createElement('div');
      card.className = 'property-card';
      // Prefer a real photograph, then a website screenshot, then the
      // branded category placeholder — every card gets an image banner.
      const banner =
        `<div class="prop-banner has-image" style="background-image:url('` +
        `${p.photo || p.image || `assets/photos/placeholder-${p.category}.jpg`}')">` +
        `<h3>${p.name}</h3></div>`;
      const siteLink = p.url
        ? `<a class="prop-site-link" href="${p.url}" target="_blank" rel="noopener">Visit website →</a>`
        : '';
      card.innerHTML =
        banner +
        `<div class="prop-body"><span class="prop-tag">${meta.label}</span>` +
        `<p>${p.blurb}</p><div class="prop-loc">${p.location}</div>${siteLink}</div>`;
      const link = card.querySelector('.prop-site-link');
      if (link) link.addEventListener('click', (e) => e.stopPropagation());
      if (p.coords) {
        card.addEventListener('click', () => {
          map.flyTo(p.coords, p.category === 'land' ? 14 : 16, { duration: 1.2 });
          const entry = markers.find((m) => m.marker.getLatLng().lat === p.coords[0]);
          if (entry) entry.marker.openPopup();
          document.getElementById('property-map').scrollIntoView({ behavior: 'smooth' });
        });
      }
      grid.appendChild(card);
    });
}
render();

// ---- Filters ----
document.querySelectorAll('.filter-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const cat = btn.dataset.filter;
    if (activeCats.has(cat)) activeCats.delete(cat);
    else activeCats.add(cat);
    btn.classList.toggle('active', activeCats.has(cat));
    btn.setAttribute('aria-pressed', String(activeCats.has(cat)));
    render();
    markers.forEach(({ marker, category }) => {
      if (isShown(category)) marker.addTo(map);
      else map.removeLayer(marker);
    });
    fitTo();
  });
});
