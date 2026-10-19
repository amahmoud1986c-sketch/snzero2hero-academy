/**
 * Zero²Hero Academy — Author branding injector
 * Ahmed Mahmoud Abdelmaksoud · LinkedIn
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
      '<a href="https://snzero2hero.com" target="_blank" rel="noopener">snzero2hero.com</a>' +
      "</div>";
    return bar;
  }

  var STATS_APIS = [
    "https://snzero2hero.com/api/stats",
    "https://snzero2hero.pages.dev/api/stats",
    "/api/stats"
  ];
  var VISIT_APIS = [
    "https://snzero2hero.com/api/visit",
    "https://snzero2hero.pages.dev/api/visit",
    "/api/visit"
  ];

  function buildFooter() {
    var foot = el("footer", { className: "z2h-site-footer", role: "contentinfo" });
    foot.innerHTML =
      '<div class="z2h-foot-inner">' +
      '<img class="z2h-avatar" src="' + photo + '" width="48" height="48" alt="Ahmed Abdelmaksoud — Zero²Hero Academy founder" />' +
      "<div>" +
      "<div><strong>" + NAME_EN + "</strong> · " + NAME_AR + "</div>" +
      "<div>Built &amp; authored this academy · " +
      '<a href="' + LI + '" target="_blank" rel="noopener noreferrer">LinkedIn Profile</a> · ' +
      '<a href="https://snzero2hero.com" target="_blank" rel="noopener">snzero2hero.com</a> · ' +
      '<a href="https://snzero2hero.com/stats.html" target="_blank" rel="noopener">Stats · الإحصائيات</a></div>' +
      '<div class="z2h-disc">Visitors: <span class="z2h-visit-count">…</span> · Country-only analytics (no signup, no personal data). Independent educational resource. Not affiliated with ServiceNow, Inc.</div>' +
      "</div></div>";
    return foot;
  }

  function recordVisitOnce() {
    try {
      if (sessionStorage.getItem("z2h_visit_sent") === "1") return;
      sessionStorage.setItem("z2h_visit_sent", "1");
    } catch (e) {}
    VISIT_APIS.forEach(function (url) {
      try {
        fetch(url, { method: "POST", mode: "cors", keepalive: true }).catch(function () {});
      } catch (e) {}
    });
  }

  function loadVisitCount() {
    var nodes = document.querySelectorAll(".z2h-visit-count");
    if (!nodes.length) return;
    function apply(n) {
      nodes.forEach(function (el) {
        el.textContent = Number(n || 0).toLocaleString();
      });
    }
    (function tryNext(i) {
      if (i >= STATS_APIS.length) {
        apply(0);
        return;
      }
      fetch(STATS_APIS[i], { cache: "no-store", mode: "cors" })
        .then(function (r) {
          return r.ok ? r.json() : Promise.reject();
        })
        .then(function (d) {
          if (d && d.ok) apply(d.totalVisits);
          else tryNext(i + 1);
        })
        .catch(function () {
          tryNext(i + 1);
        });
    })(0);
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
      var body = document.body;
      if (body.firstChild) body.insertBefore(bar, body.firstChild);
      else body.appendChild(bar);
    }

    if (!document.querySelector(".z2h-site-footer")) {
      document.body.appendChild(buildFooter());
    }

    recordVisitOnce();
    loadVisitCount();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
