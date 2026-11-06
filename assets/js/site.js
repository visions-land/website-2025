/* Visions — static site behaviour.
   Two things only: the EN/IT switch and the mobile menu.
   Without JavaScript the site still works and reads in English. */
(function () {
  "use strict";

  var STORE_KEY = "visions.lang";
  var html = document.documentElement;

  /* ---------- language ---------- */
  function readStored() {
    try {
      return localStorage.getItem(STORE_KEY);
    } catch (e) {
      return null;
    }
  }

  function writeStored(lang) {
    try {
      localStorage.setItem(STORE_KEY, lang);
    } catch (e) {
      /* private mode / blocked storage: the choice just won't persist */
    }
  }

  function applyLang(lang) {
    lang = lang === "it" ? "it" : "en";
    html.setAttribute("data-lang", lang);
    html.setAttribute("lang", lang);

    // <title> and anything else carrying a translated attribute
    var titleEl = document.querySelector("title[data-it]");
    if (titleEl) {
      if (!titleEl.hasAttribute("data-en")) {
        titleEl.setAttribute("data-en", titleEl.textContent);
      }
      titleEl.textContent = titleEl.getAttribute("data-" + lang);
    }

    var attrEls = document.querySelectorAll("[data-ph-it]");
    for (var i = 0; i < attrEls.length; i++) {
      var el = attrEls[i];
      if (!el.hasAttribute("data-ph-en")) {
        el.setAttribute("data-ph-en", el.getAttribute("placeholder") || "");
      }
      el.setAttribute("placeholder", el.getAttribute("data-ph-" + lang));
    }

    var selects = document.querySelectorAll(".lang-switch select");
    for (var j = 0; j < selects.length; j++) {
      selects[j].value = lang;
    }
  }

  applyLang(readStored() || "en");

  document.addEventListener("change", function (ev) {
    var select = ev.target.closest
      ? ev.target.closest(".lang-switch select")
      : null;
    if (!select) return;
    applyLang(select.value);
    writeStored(select.value);
  });

  /* ---------- mobile menu ---------- */
  var body = document.body;

  function setMenu(open) {
    body.classList.toggle("menu-open", open);
    var panel = document.querySelector(".menu-panel");
    if (panel) panel.setAttribute("aria-hidden", open ? "false" : "true");
  }

  document.addEventListener("click", function (ev) {
    var t = ev.target;
    if (!t.closest) return;
    if (t.closest(".menu-btn")) {
      setMenu(!body.classList.contains("menu-open"));
      return;
    }
    if (t.closest(".menu-scrim") || t.closest("[data-menu-close]")) {
      setMenu(false);
    }
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") setMenu(false);
  });

  /* Staggered entry for the menu items, as in the original. */
  var items = document.querySelectorAll(".menu-panel li");
  for (var k = 0; k < items.length; k++) {
    items[k].style.transitionDelay = (items.length - k) * 100 + "ms";
  }
})();
