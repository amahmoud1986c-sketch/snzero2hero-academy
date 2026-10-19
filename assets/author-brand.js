/**
 * Zero²Hero Academy — Author branding + privacy-friendly visit ping
 * Ahmed Mahmoud Abdelmaksoud · LinkedIn
 * Stores no names/emails/IPs — only anonymous aggregates via /api/visit
 */
(function () {
  if (window.__z2hAuthorBrand) return;
  window.__z2hAuthorBrand = true;

  var LI = "https://www.linkedin.com/in/ahmed-abdelmaksoud-44917a89/";
  var NAME_EN = "Ahmed Abdelmaksoud";
  var NAME_AR = "أحمد محمود عبدالمقصود";
  var ROLE = "Founder · Zero²Hero Academy · ServiceNow";

  function assetBase() {
    var scripts = document.getElementsByTagName("script");
    for (var i = scripts.length - 1; i >= 0; i--) {
      var src = scripts[i].src || "";
      if (src.indexOf("author-brand.js") !== -1) {
        return src.replace(/author-brand\.js(\?.*)?$/, "");
      }
    }
    return "assets/";
  }

  var base = assetBase();
  var photo = base + "ahmed-abdelmaksoud.png";

  function el(tag, attrs, html) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "className") node.className = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    if (html != null) node.innerHTML = html;
    return node;
  }

  function statsHref() {
    try {
      var u = new URL("stats.html", window.location.href);
      return u.pathname.replace(/\/[^/]*$/, "/stats.html").replace(/\/stats\.html$/, "/stats.html");
    } catch (e) {
      return "/stats.html";
    }
  }

  function buildBar() {
    var bar = el("div", {
      className: "z2h-author-bar",
      role: "banner",
      "aria-label": "Author — Ahmed Abdelmaksoud"
    });
    bar.innerHTML =
      '<div class="z2h-author-left">' +
      '<img class="z2h-avatar" src="' + photo + '" width="36" height="36" alt="Professional portrait of Ahmed Abdelmaksoud, ServiceNow Instructor" />' +
      '<div><div class="z2h-name">' + NAME_AR + ' · ' + NAME_EN + '</div>' +
      '<div class="z2h-role">' + ROLE + '</div></div></div>' +
      '<div class="z2h-author-right">' +
      '<a class="z2h-li" href="' + LI + '" target="_blank" rel="noopener noreferrer" title="LinkedIn — Ahmed Abdelmaksoud">in LinkedIn</a>' +
      '<a href="/stats.html" title="Public visit stats">Stats</a>' +
      '<a href="https://snzero2hero.com" target="_blank" rel="noopener">snzero2hero.com</a>' +
      "</div>";
    return bar;
  }

  function buildFooter() {
    var foot = el("footer", { className: "z2h-site-footer", role: "contentinfo" });
    foot.innerHTML =
      '<div class="z2h-foot-inner">' +
      '<img class="z2h-avatar" src="' + photo + '" width="48" height="48" alt="Ahmed Abdelmaksoud — Zero²Hero Academy founder" />' +
      "<div>" +
      "<div><strong>" + NAME_EN + "</strong> · " + NAME_AR + "</div>" +
      "<div>Built &amp; authored this academy · " +
      '<a href="' + LI + '" target="_blank" rel="noopener noreferrer">LinkedIn</a> · ' +
      '<a href="https://snzero2hero.com" target="_blank" rel="noopener">snzero2hero.com</a> · ' +
      '<a href="/stats.html">Stats · الإحصائيات</a></div>' +
      '<div class="z2h-disc">Visitors: <span class="z2h-visit-count">…</span> · Country-only analytics (no signup, no personal data). Not affiliated with ServiceNow, Inc.</div>' +
      "</div></div>";
    return foot;
  }

  function utmSource() {
    try {
      return new URLSearchParams(window.location.search).get("utm_source") || "";
    } catch (e) {
      return "";
    }
  }

  function recordVisit() {
    var newSession = false;
    try {
      if (!sessionStorage.getItem("z2h_session")) {
        sessionStorage.setItem("z2h_session", "1");
        newSession = true;
      }
      var pathKey = "z2h_path:" + location.pathname;
      if (sessionStorage.getItem(pathKey) === "1") return;
      sessionStorage.setItem(pathKey, "1");
    } catch (e) {
      newSession = true;
    }

    var payload = JSON.stringify({
      path: location.pathname + location.search,
      referrer: document.referrer || "",
      utm_source: utmSource(),
      newSession: newSession
    });

    try {
      fetch("/api/visit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        keepalive: true,
        mode: "cors",
        credentials: "omit"
      }).catch(function () {});
    } catch (e) {}
  }

  function loadVisitCount() {
    var nodes = document.querySelectorAll(".z2h-visit-count");
    if (!nodes.length) return;
    fetch("/api/stats", { cache: "no-store", credentials: "omit" })
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (d) {
        if (!d || !d.ok) return;
        nodes.forEach(function (n) {
          n.textContent = Number(d.totalVisits || 0).toLocaleString();
        });
      })
      .catch(function () {});
  }

  function inject() {
    if (!document.getElementById("z2h-author-brand-css")) {
      var link = document.createElement("link");
      link.id = "z2h-author-brand-css";
      link.rel = "stylesheet";
      link.href = base + "author-brand.css";
      document.head.appendChild(link);
    }

    if (!document.querySelector(".z2h-author-bar")) {
      var bar = buildBar();
      if (document.body.firstChild) document.body.insertBefore(bar, document.body.firstChild);
      else document.body.appendChild(bar);
    }

    if (!document.querySelector(".z2h-site-footer")) {
      document.body.appendChild(buildFooter());
    }

    recordVisit();
    loadVisitCount();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
