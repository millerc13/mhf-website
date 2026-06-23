// Contact page: office mini-map + topic preselect from ?topic= links.

// Mini-map of the family office (423 N. Boundary St., Williamsburg VA)
const officeEl = document.getElementById('office-map');
if (officeEl && window.L) {
  const OFFICE = [37.27522, -76.70762];
  const map = L.map(officeEl, {
    zoomControl: false,
    scrollWheelZoom: false,
    dragging: false,
    touchZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
  });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);
  map.setView(OFFICE, 16);
  const icon = L.divIcon({
    className: '',
    html:
      '<svg width="34" height="45" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M16 1C8 1 1.5 7.5 1.5 15.5 1.5 26 16 41 16 41s14.5-15 14.5-25.5C30.5 7.5 24 1 16 1z" ' +
      'fill="#c8973a" stroke="#122419" stroke-width="2"/>' +
      '<circle cx="16" cy="15.5" r="5.5" fill="#f7f1e2"/></svg>',
    iconSize: [34, 45],
    iconAnchor: [17, 44],
    popupAnchor: [0, -40],
  });
  L.marker(OFFICE, { icon })
    .addTo(map)
    .bindPopup('<div class="map-popup"><h4>MHF Family Office</h4><p>423 N. Boundary St., Suite 100</p></div>');
}

// Preselect the inquiry topic when arriving from a routed CTA
// (e.g. careers "Apply" links use contact.html?topic=careers)
const topicParam = new URLSearchParams(location.search).get('topic');
const topicSelect = document.getElementById('topic');
if (topicParam && topicSelect) {
  const match = Array.from(topicSelect.options).some((o) => o.value === topicParam);
  if (match) topicSelect.value = topicParam;
}
