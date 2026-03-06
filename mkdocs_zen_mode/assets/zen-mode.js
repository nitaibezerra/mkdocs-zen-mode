(function() {
  "use strict";

  var STORAGE_KEY = "{{STORAGE_KEY}}";
  var SHORTCUT = "{{SHORTCUT}}";

  /* --- State helpers --- */
  function isActive() {
    try { return localStorage.getItem(STORAGE_KEY) === "true"; }
    catch (e) { return false; }
  }

  function setActive(state) {
    try { localStorage.setItem(STORAGE_KEY, state ? "true" : "false"); }
    catch (e) { /* private browsing */ }
  }

  function applyState(active) {
    if (active) {
      document.body.classList.add("zen-mode-active");
    } else {
      document.body.classList.remove("zen-mode-active");
    }
    var buttons = document.querySelectorAll(".zen-mode-toggle, .zen-mode-fab");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute("aria-pressed", active ? "true" : "false");
    }
  }

  function toggle() {
    var active = !document.body.classList.contains("zen-mode-active");
    applyState(active);
    setActive(active);
  }

  /* --- FAB creation (once) --- */
  function ensureFab() {
    if (document.querySelector(".zen-mode-fab")) return;
    var fab = document.createElement("button");
    fab.className = "zen-mode-fab";
    fab.title = "Exit Zen Mode (" + SHORTCUT + ")";
    fab.setAttribute("aria-label", "Exit Zen Mode");
    fab.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' +
      '<path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/>' +
      '</svg>';
    fab.addEventListener("click", toggle);
    document.body.appendChild(fab);
  }

  /* --- Button binding --- */
  function setupButtons() {
    var btns = document.querySelectorAll(".zen-mode-toggle");
    for (var i = 0; i < btns.length; i++) {
      if (!btns[i].__zenBound) {
        btns[i].addEventListener("click", toggle);
        btns[i].__zenBound = true;
      }
    }
  }

  /* --- Keyboard shortcut --- */
  function parseShortcut(str) {
    var parts = str.toLowerCase().split("+");
    return {
      alt:   parts.indexOf("alt")   !== -1,
      ctrl:  parts.indexOf("ctrl")  !== -1,
      shift: parts.indexOf("shift") !== -1,
      meta:  parts.indexOf("meta")  !== -1,
      key:   parts[parts.length - 1]
    };
  }

  var shortcut = parseShortcut(SHORTCUT);

  function handleKeydown(e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" ||
        e.target.isContentEditable) return;
    if (e.altKey   === shortcut.alt  &&
        e.ctrlKey  === shortcut.ctrl &&
        e.shiftKey === shortcut.shift &&
        e.metaKey  === shortcut.meta &&
        e.key.toLowerCase() === shortcut.key) {
      e.preventDefault();
      toggle();
    }
  }

  /* --- Init --- */
  function init() {
    setupButtons();
    ensureFab();
    applyState(isActive());
  }

  /* Keyboard: bind once */
  if (!window.__zenModeKeybound) {
    document.addEventListener("keydown", handleKeydown);
    window.__zenModeKeybound = true;
  }

  /* --- Instant navigation compatibility --- */
  /* MkDocs Material exposes document$ (RxJS observable) when navigation.instant is on */
  if (typeof document$ !== "undefined") {
    document$.subscribe(function() { init(); });
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
