
(function () {
  var STORAGE_KEY = "hrl_instance_base";

  function normalizeBase(raw) {
    if (!raw) return "";
    var b = String(raw).trim().replace(/\/+$/, "");
    if (!/^https?:\/\//i.test(b)) b = "https://" + b;
    return b;
  }

  function applyBase(base) {
    if (!base) return;
    document.querySelectorAll('a[href*="{BASE}"]').forEach(function (a) {
      var href = a.getAttribute("href") || "";
      a.setAttribute("href", href.split("{BASE}").join(base));
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener");
    });
    document.querySelectorAll(".url-box code, .meta-grid code").forEach(function (el) {
      if ((el.textContent || "").indexOf("{BASE}") >= 0) {
        el.textContent = (el.textContent || "").split("{BASE}").join(base);
      }
    });
  }

  function mountBaseBar() {
    if (document.getElementById("instance-base-bar")) return;
    var bar = document.createElement("div");
    bar.id = "instance-base-bar";
    bar.style.cssText = "max-width:1100px;margin:.75rem auto 0;padding:0 1.25rem;";
    bar.innerHTML =
      '<div class="url-box" style="background:#eff6ff;border-color:#bfdbfe">' +
      "<strong>Your instance</strong>" +
      '<input id="instance-base-input" type="text" placeholder="https://dev12345.service-now.com" ' +
      'style="flex:1;min-width:220px;border:1px solid #93c5fd;border-radius:8px;padding:.35rem .55rem;font-family:inherit" />' +
      '<button type="button" id="instance-base-save" class="copy-btn" style="position:static">Apply URLs</button>' +
      "</div>";
    var layout = document.querySelector("main.layout");
    if (layout) layout.insertBefore(bar, layout.firstChild);
    var input = document.getElementById("instance-base-input");
    var saved = normalizeBase(localStorage.getItem(STORAGE_KEY) || "");
    if (saved) {
      input.value = saved;
      applyBase(saved);
    }
    document.getElementById("instance-base-save").addEventListener("click", function () {
      var base = normalizeBase(input.value);
      if (!base) return;
      localStorage.setItem(STORAGE_KEY, base);
      // reload so all {BASE} hrefs refresh cleanly
      location.reload();
    });
  }

  function enhance() {
    document.querySelectorAll('a[href*="{BASE}"]').forEach(function (a) {
      if (!a.closest(".url-box")) a.classList.add("direct-link");
    });
    mountBaseBar();
    var saved = normalizeBase(localStorage.getItem(STORAGE_KEY) || "");
    if (saved) applyBase(saved);

    document.querySelectorAll("pre").forEach(function (pre) {
      if (pre.parentElement && pre.parentElement.classList.contains("pre-wrap")) return;
      var wrap = document.createElement("div");
      wrap.className = "pre-wrap";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.addEventListener("click", function () {
        var text = pre.innerText || pre.textContent || "";
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          setTimeout(function () {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
          }, 1400);
        });
      });
      wrap.appendChild(btn);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhance);
  } else {
    enhance();
  }
})();
