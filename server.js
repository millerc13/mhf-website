/* Minimal zero-dependency static file server for Forge hosting.
   - Serves the live MHF site (the `site/` folder) at the web root.
   - Serves the client palette gallery (the `theme-previews/` folder) under /preview.
   - Honors cleanUrls (e.g. /about -> about.html), matching site/vercel.json.
   No npm dependencies, so the Forge build is just `npm start`. */
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;
const SITE_DIR = path.join(__dirname, "site");
const PREVIEW_DIR = path.join(__dirname, "theme-previews");
const LOGOS_DIR = path.join(__dirname, "logoMockups");

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
};

function contentType(p) {
  return TYPES[path.extname(p).toLowerCase()] || "application/octet-stream";
}

function send(res, status, body, type) {
  res.writeHead(status, { "Content-Type": type || "text/plain; charset=utf-8" });
  res.end(body);
}

function sendFile(res, filePath) {
  fs.readFile(filePath, (err, data) => {
    if (err) return send(res, 404, "404 — Not Found");
    res.writeHead(200, { "Content-Type": contentType(filePath) });
    res.end(data);
  });
}

// Resolve a request path safely within a base dir; returns a file path or null.
function resolveIn(baseDir, relPath) {
  const decoded = decodeURIComponent(relPath.split("?")[0]);
  const target = path.normalize(path.join(baseDir, decoded));
  if (target !== baseDir && !target.startsWith(baseDir + path.sep)) return null; // no traversal
  return target;
}

const server = http.createServer((req, res) => {
  let urlPath = req.url.split("?")[0];

  // ---- Gallery: anything under /preview maps into theme-previews/ ----
  if (urlPath === "/preview" || urlPath === "/preview/") {
    return sendFile(res, path.join(PREVIEW_DIR, "gallery.html"));
  }
  if (urlPath.startsWith("/preview/")) {
    const f = resolveIn(PREVIEW_DIR, urlPath.slice("/preview".length));
    if (!f) return send(res, 400, "400 — Bad Request");
    return sendFile(res, f);
  }

  // ---- Logo mockups gallery: anything under /logos maps into logoMockups/ ----
  if (urlPath === "/logos" || urlPath === "/logos/") {
    return sendFile(res, path.join(LOGOS_DIR, "gallery.html"));
  }
  if (urlPath.startsWith("/logos/")) {
    const f = resolveIn(LOGOS_DIR, urlPath.slice("/logos".length));
    if (!f) return send(res, 400, "400 — Bad Request");
    return sendFile(res, f);
  }

  // ---- Live site (site/ as web root) ----
  if (urlPath === "/") return sendFile(res, path.join(SITE_DIR, "index.html"));

  const f = resolveIn(SITE_DIR, urlPath);
  if (!f) return send(res, 400, "400 — Bad Request");

  fs.stat(f, (err, stat) => {
    if (!err && stat.isDirectory()) return sendFile(res, path.join(f, "index.html"));
    if (!err && stat.isFile()) return sendFile(res, f);
    // cleanUrls: /about -> about.html
    if (!path.extname(f)) {
      return fs.stat(f + ".html", (e2, s2) => {
        if (!e2 && s2.isFile()) return sendFile(res, f + ".html");
        return send(res, 404, "404 — Not Found");
      });
    }
    return send(res, 404, "404 — Not Found");
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`MHF site listening on :${PORT}  (gallery at /preview)`);
});
