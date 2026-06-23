/* ============================================================
   MHF — Color Theme Previewer  (CLIENT PREVIEW TOOL ONLY)
   ------------------------------------------------------------
   This is a non-destructive overlay for John to click through
   palette options and pick a favorite. It changes NOTHING about
   the site's content or layout — it only swaps the CSS color
   variables defined in styles.css (:root), live, and remembers
   the choice across pages via localStorage.

   To REMOVE before final launch: delete this file and the
   <script src="js/theme-switcher.js"></script> line in build.py
   (then re-run python3 build.py). The site reverts to Heritage.
   ============================================================ */
(function () {
  "use strict";

  // Each theme maps the same color ROLES used throughout styles.css.
  // --green*  = primary brand / dark surfaces
  // --cream*  = warm paper background
  // --gold*   = accent (buttons, highlights, selection)
  // --ink*    = body text   |   --white = light surface cards
  // --rule / --press* are borders + letterpress offset shadows.
  var THEMES = [
    {
      id: "heritage",
      name: "Heritage Green & Gold",
      note: "The current site palette",
      vars: {
        "--green": "#1b3527", "--green-deep": "#122419", "--green-soft": "#2c5243",
        "--cream": "#f7f1e2", "--cream-dark": "#ede4cd",
        "--gold": "#c8973a", "--gold-soft": "#e2c179",
        "--ink": "#20251e", "--ink-soft": "#59604f", "--white": "#fffdf7",
        "--rule": "rgba(27,53,39,0.25)",
        "--press": "6px 6px 0 rgba(18,36,25,0.12)",
        "--press-lg": "9px 9px 0 rgba(18,36,25,0.14)"
      }
    },
    {
      id: "navy-brass",
      name: "Midnight Navy & Brass",
      note: "Old-money, banking blue",
      vars: {
        "--green": "#1d2d44", "--green-deep": "#131f30", "--green-soft": "#34506e",
        "--cream": "#f4f0e6", "--cream-dark": "#e7e0cd",
        "--gold": "#b5894a", "--gold-soft": "#d8b876",
        "--ink": "#1c2330", "--ink-soft": "#586073", "--white": "#fffdf8",
        "--rule": "rgba(29,45,68,0.25)",
        "--press": "6px 6px 0 rgba(19,31,48,0.12)",
        "--press-lg": "9px 9px 0 rgba(19,31,48,0.14)"
      }
    },
    {
      id: "oxblood",
      name: "Oxblood & Antique Gold",
      note: "Leather-bound library",
      vars: {
        "--green": "#5a2231", "--green-deep": "#3d141f", "--green-soft": "#7c3a48",
        "--cream": "#f6efe5", "--cream-dark": "#ebdfca",
        "--gold": "#b08237", "--gold-soft": "#d7b06a",
        "--ink": "#2a1c1f", "--ink-soft": "#6a5559", "--white": "#fffaf4",
        "--rule": "rgba(90,34,49,0.25)",
        "--press": "6px 6px 0 rgba(61,20,31,0.12)",
        "--press-lg": "9px 9px 0 rgba(61,20,31,0.14)"
      }
    },
    {
      id: "charcoal",
      name: "Charcoal & Champagne",
      note: "Modern, understated luxury",
      vars: {
        "--green": "#2b2b2b", "--green-deep": "#161616", "--green-soft": "#474747",
        "--cream": "#f5f1ea", "--cream-dark": "#e6dfd1",
        "--gold": "#bfa06a", "--gold-soft": "#ddc69a",
        "--ink": "#1f1d1a", "--ink-soft": "#5c574d", "--white": "#fffdf9",
        "--rule": "rgba(43,43,43,0.22)",
        "--press": "6px 6px 0 rgba(22,22,22,0.12)",
        "--press-lg": "9px 9px 0 rgba(22,22,22,0.14)"
      }
    },
    {
      id: "forest-copper",
      name: "Forest & Copper",
      note: "Warm, earthy, hand-crafted",
      vars: {
        "--green": "#243b2f", "--green-deep": "#15241b", "--green-soft": "#3b5a49",
        "--cream": "#f4efe3", "--cream-dark": "#e6dcc6",
        "--gold": "#b96f3f", "--gold-soft": "#d99e6f",
        "--ink": "#221f1a", "--ink-soft": "#5b5247", "--white": "#fffcf6",
        "--rule": "rgba(36,59,47,0.25)",
        "--press": "6px 6px 0 rgba(21,36,27,0.12)",
        "--press-lg": "9px 9px 0 rgba(21,36,27,0.14)"
      }
    },
    {
      id: "slate-gold",
      name: "Slate Blue & Gold",
      note: "Coastal, calm, maritime",
      vars: {
        "--green": "#20414a", "--green-deep": "#122a31", "--green-soft": "#356069",
        "--cream": "#f3f1e9", "--cream-dark": "#e3dfcf",
        "--gold": "#c39a3e", "--gold-soft": "#e0c47f",
        "--ink": "#1c2426", "--ink-soft": "#54605f", "--white": "#fdfdf8",
        "--rule": "rgba(32,65,74,0.25)",
        "--press": "6px 6px 0 rgba(18,42,49,0.12)",
        "--press-lg": "9px 9px 0 rgba(18,42,49,0.14)"
      }
    },
    {
      id: "plum",
      name: "Plum & Antique Gold",
      note: "Distinguished, regal",
      vars: {
        "--green": "#3a2742", "--green-deep": "#261829", "--green-soft": "#543b5e",
        "--cream": "#f5f0e9", "--cream-dark": "#e7ddd0",
        "--gold": "#b58a4c", "--gold-soft": "#d6b67e",
        "--ink": "#241d28", "--ink-soft": "#5d5360", "--white": "#fffcf7",
        "--rule": "rgba(58,39,66,0.25)",
        "--press": "6px 6px 0 rgba(38,24,41,0.12)",
        "--press-lg": "9px 9px 0 rgba(38,24,41,0.14)"
      }
    },
    {
      id: "espresso",
      name: "Espresso & Cognac",
      note: "Whiskey, walnut, timeless",
      vars: {
        "--green": "#3a2c20", "--green-deep": "#241a12", "--green-soft": "#574332",
        "--cream": "#f5eee0", "--cream-dark": "#e8dcc4",
        "--gold": "#c08a3e", "--gold-soft": "#ddb678",
        "--ink": "#2a2118", "--ink-soft": "#635647", "--white": "#fffbf3",
        "--rule": "rgba(58,44,32,0.25)",
        "--press": "6px 6px 0 rgba(36,26,18,0.12)",
        "--press-lg": "9px 9px 0 rgba(36,26,18,0.14)"
      }
    },
    {
      id: "indigo",
      name: "Royal Indigo & Gold",
      note: "Bold, confident, executive",
      vars: {
        "--green": "#283164", "--green-deep": "#181d3e", "--green-soft": "#3f4a87",
        "--cream": "#f3f1ea", "--cream-dark": "#e3dfd0",
        "--gold": "#c6a44a", "--gold-soft": "#e2c97f",
        "--ink": "#1f2230", "--ink-soft": "#555a6b", "--white": "#fffdf8",
        "--rule": "rgba(40,49,100,0.25)",
        "--press": "6px 6px 0 rgba(24,29,62,0.12)",
        "--press-lg": "9px 9px 0 rgba(24,29,62,0.14)"
      }
    }
  ];

  var STORAGE_KEY = "mhf-preview-theme";
  var DEFAULT_ID = "heritage";

  function applyTheme(theme) {
    var root = document.documentElement;
    Object.keys(theme.vars).forEach(function (k) {
      root.style.setProperty(k, theme.vars[k]);
    });
  }

  function findTheme(id) {
    for (var i = 0; i < THEMES.length; i++) {
      if (THEMES[i].id === id) return THEMES[i];
    }
    return THEMES[0];
  }

  function saveChoice(id) {
    try { localStorage.setItem(STORAGE_KEY, id); } catch (e) {}
  }

  function loadChoice() {
    try { return localStorage.getItem(STORAGE_KEY) || DEFAULT_ID; }
    catch (e) { return DEFAULT_ID; }
  }

  // ---- Apply saved theme immediately (before paint, to avoid flash) ----
  var currentId = loadChoice();
  applyTheme(findTheme(currentId));

  // ---- Build the floating previewer UI once the DOM is ready ----
  function buildUI() {
    var css = document.createElement("style");
    css.textContent =
      "#mhf-tp-btn{position:fixed;right:20px;bottom:20px;z-index:9000;" +
      "display:flex;align-items:center;gap:9px;cursor:pointer;border:0;" +
      "font:600 13px/1 'Archivo',system-ui,sans-serif;letter-spacing:.04em;" +
      "text-transform:uppercase;color:#fff;background:#16181c;" +
      "padding:13px 18px;border-radius:999px;box-shadow:0 8px 26px rgba(0,0,0,.32);" +
      "transition:transform .15s ease}" +
      "#mhf-tp-btn:hover{transform:translateY(-2px)}" +
      "#mhf-tp-btn .dot{width:13px;height:13px;border-radius:50%;" +
      "background:conic-gradient(#c8973a,#5a2231,#283164,#243b2f,#c8973a);" +
      "box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.6)}" +
      "#mhf-tp-panel{position:fixed;right:20px;bottom:74px;z-index:9001;" +
      "width:312px;max-width:calc(100vw - 40px);max-height:78vh;overflow:auto;" +
      "background:#fff;color:#1c1c1c;border-radius:16px;" +
      "box-shadow:0 18px 50px rgba(0,0,0,.34);" +
      "font-family:'Archivo',system-ui,sans-serif;display:none;" +
      "-webkit-overflow-scrolling:touch}" +
      "#mhf-tp-panel.open{display:block}" +
      "#mhf-tp-panel header{padding:17px 18px 12px;border-bottom:1px solid #ececec}" +
      "#mhf-tp-panel header b{display:block;font-size:14px;letter-spacing:.02em;color:#16181c}" +
      "#mhf-tp-panel header span{display:block;margin-top:3px;font-size:11.5px;color:#8a8a8a;" +
      "font-weight:500;line-height:1.45}" +
      "#mhf-tp-list{padding:10px}" +
      ".mhf-tp-item{display:flex;align-items:center;gap:12px;width:100%;text-align:left;" +
      "border:1.5px solid transparent;background:transparent;border-radius:11px;" +
      "padding:10px 11px;cursor:pointer;margin:2px 0;transition:background .12s,border-color .12s}" +
      ".mhf-tp-item:hover{background:#f5f5f3}" +
      ".mhf-tp-item.active{border-color:#16181c;background:#f5f5f3}" +
      ".mhf-tp-sw{flex:0 0 auto;display:flex;border-radius:7px;overflow:hidden;" +
      "box-shadow:0 1px 3px rgba(0,0,0,.18)}" +
      ".mhf-tp-sw i{display:block;width:15px;height:34px}" +
      ".mhf-tp-meta{flex:1;min-width:0}" +
      ".mhf-tp-meta b{display:block;font-size:12.5px;font-weight:600;color:#1c1c1c;" +
      "white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" +
      ".mhf-tp-meta span{display:block;font-size:11px;color:#999;font-weight:500;margin-top:2px}" +
      ".mhf-tp-check{flex:0 0 auto;width:18px;height:18px;color:#16181c;opacity:0}" +
      ".mhf-tp-item.active .mhf-tp-check{opacity:1}" +
      "#mhf-tp-panel footer{padding:11px 18px 15px;border-top:1px solid #ececec;" +
      "font-size:10.5px;color:#a5a5a5;font-weight:500;line-height:1.5}";
    document.head.appendChild(css);

    var btn = document.createElement("button");
    btn.id = "mhf-tp-btn";
    btn.type = "button";
    btn.setAttribute("aria-label", "Preview color themes");
    btn.innerHTML = '<span class="dot"></span><span>Theme</span>';

    var panel = document.createElement("div");
    panel.id = "mhf-tp-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Color theme previewer");

    var head = document.createElement("header");
    head.innerHTML = "<b>Choose a color palette</b><span>Click any option to preview it live. " +
      "Your pick follows you across every page. This panel is for review only.</span>";
    panel.appendChild(head);

    var list = document.createElement("div");
    list.id = "mhf-tp-list";

    THEMES.forEach(function (theme) {
      var item = document.createElement("button");
      item.type = "button";
      item.className = "mhf-tp-item" + (theme.id === currentId ? " active" : "");
      item.setAttribute("data-id", theme.id);

      var sw = '<span class="mhf-tp-sw">' +
        '<i style="background:' + theme.vars["--green"] + '"></i>' +
        '<i style="background:' + theme.vars["--cream"] + '"></i>' +
        '<i style="background:' + theme.vars["--gold"] + '"></i>' +
        '<i style="background:' + theme.vars["--green-soft"] + '"></i>' +
        '</span>';
      var meta = '<span class="mhf-tp-meta"><b>' + theme.name + '</b><span>' + theme.note + '</span></span>';
      var check = '<svg class="mhf-tp-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
        'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
      item.innerHTML = sw + meta + check;

      item.addEventListener("click", function () {
        currentId = theme.id;
        applyTheme(theme);
        saveChoice(theme.id);
        var items = list.querySelectorAll(".mhf-tp-item");
        for (var i = 0; i < items.length; i++) items[i].classList.remove("active");
        item.classList.add("active");
      });

      list.appendChild(item);
    });
    panel.appendChild(list);

    var foot = document.createElement("footer");
    foot.textContent = "MHF palette previewer — removable before launch.";
    panel.appendChild(foot);

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      panel.classList.toggle("open");
    });
    document.addEventListener("click", function (e) {
      if (panel.classList.contains("open") &&
          !panel.contains(e.target) && e.target !== btn) {
        panel.classList.remove("open");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") panel.classList.remove("open");
    });

    document.body.appendChild(btn);
    document.body.appendChild(panel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildUI);
  } else {
    buildUI();
  }
})();
