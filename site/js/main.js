// MHF — shared site behavior

// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Highlight the current page in the nav
const here = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach((a) => {
  const target = a.getAttribute('href');
  if (target === here && !a.classList.contains('nav-cta')) a.classList.add('active');
});

// Scroll-reveal animations (hide-state is gated on this class so no-JS still renders)
document.documentElement.classList.add('js-anim');

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealEls = Array.from(document.querySelectorAll('.reveal'));

// CSS fallback path: IntersectionObserver + transition with sibling stagger
function cssReveals() {
  revealEls.forEach((el) => {
    const siblings = Array.from(el.parentElement.children).filter((c) => c.classList.contains('reveal'));
    if (siblings.length > 1) {
      const i = siblings.indexOf(el);
      el.style.transitionDelay = `${Math.min(i * 90, 540)}ms`;
      el.addEventListener('transitionend', function clearDelay() {
        el.style.transitionDelay = '0ms';
        el.removeEventListener('transitionend', clearDelay);
      });
    }
  });
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          const spine = e.target.closest('.timeline');
          if (spine) spine.classList.add('spine-on');
          observer.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  revealEls.forEach((el) => observer.observe(el));
}

// Preferred path: Motion (vanilla Framer Motion) — spring-eased, staggered
// group reveals. Degrades to the CSS path if the CDN module fails.
if (!prefersReducedMotion && revealEls.length) {
  import('https://cdn.jsdelivr.net/npm/motion@11.13.5/+esm')
    .then(({ animate, inView, stagger }) => {
      document.documentElement.classList.add('motion-on');
      const groups = new Map();
      revealEls.forEach((el) => {
        const parent = el.parentElement;
        if (!groups.has(parent)) groups.set(parent, []);
        groups.get(parent).push(el);
      });
      const markVisible = (el) => {
        el.classList.add('visible');
        const spine = el.closest('.timeline');
        if (spine) spine.classList.add('spine-on');
      };
      groups.forEach((els, parent) => {
        if (parent.classList.contains('timeline')) {
          // Timeline entries reveal one-by-one as each scrolls into view,
          // so the spine/diamond choreography reads as a story, not a dump.
          els.forEach((el) => {
            const stopOne = inView(
              el,
              () => {
                animate(
                  el,
                  { opacity: [0, 1], transform: ['translateY(26px)', 'translateY(0px)'] },
                  { type: 'spring', stiffness: 90, damping: 17 }
                );
                markVisible(el);
                stopOne();
              },
              { amount: 0.45 }
            );
          });
          return;
        }
        const stop = inView(
          parent,
          () => {
            animate(
              els,
              { opacity: [0, 1], transform: ['translateY(32px) scale(0.985)', 'translateY(0px) scale(1)'] },
              { delay: stagger(0.11), type: 'spring', stiffness: 90, damping: 16 }
            );
            els.forEach(markVisible);
            stop();
          },
          { amount: 0.12 }
        );
      });
    })
    .catch(cssReveals);
} else {
  cssReveals();
}

// Count-up stats when they scroll into view
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('.stat-num').forEach((el) => {
  const m = el.textContent.trim().match(/^(\d+)(.*)$/);
  if (!m || reduceMotion) return;
  const target = +m[1];
  const suffix = m[2];
  el.textContent = '0' + suffix;
  const counterObs = new IntersectionObserver((entries) => {
    if (!entries[0].isIntersecting) return;
    counterObs.disconnect();
    const t0 = performance.now();
    const dur = 1300;
    (function tick(t) {
      const p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }, { threshold: 0.6 });
  counterObs.observe(el);
});

// Contact form (no backend yet — validate, then show a friendly confirmation)
const form = document.querySelector('form.contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    form.innerHTML =
      '<div class="form-success">' +
      '<svg viewBox="0 0 64 60" width="64" height="56" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
      '<path d="M32 4 C17 4 6.5 15 4.5 28.5 C8.5 24 15 24 18.5 28.5 C22 24 28.5 24 32 28.5 C35.5 24 42 24 45.5 28.5 C49 24 55.5 24 59.5 28.5 C57.5 15 47 4 32 4 Z" fill="#c8973a"/>' +
      '<rect x="30.6" y="6" width="2.8" height="40" rx="1.4" fill="#1b3527"/>' +
      '<path d="M33.4 46 c0 7 -10.5 7 -10.5 0" fill="none" stroke="#1b3527" stroke-width="2.8" stroke-linecap="round"/></svg>' +
      '<h3>Thank you — it’s on its way.</h3>' +
      '<p>Your note is headed to the family office. Someone from MHF will be in touch shortly.</p>' +
      '</div>';
  });
}
