// Shared behaviour for every page: theme toggle, mobile menu, footer year.
(function () {
  // Light / dark: follows the OS until a choice is made, then remembered per browser
  var KEY = 'nf3-theme';
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var themeBtn = document.querySelector('.theme');
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeBtn) themeBtn.setAttribute('aria-label', theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
  }
  applyTheme(stored() || (media && media.matches ? 'dark' : 'light'));
  if (media && media.addEventListener) {
    media.addEventListener('change', function (e) { if (!stored()) applyTheme(e.matches ? 'dark' : 'light'); });
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(KEY, next); } catch (e) {}
      applyTheme(next);
    });
  }

  // Mobile menu
  var menuBtn = document.querySelector('.menu');
  var menu = document.getElementById('menu');
  function setMenu(open) {
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    menu.classList.toggle('is-open', open);
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); menuBtn.focus(); }
    });
  }

  // "Volver" on legal pages: go back if we came from this site, otherwise the link's href (home)
  Array.prototype.forEach.call(document.querySelectorAll('[data-back]'), function (a) {
    a.addEventListener('click', function (e) {
      var ref = document.referrer;
      if (ref && ref.indexOf(location.origin) === 0 && ref !== location.href && history.length > 1) {
        e.preventDefault();
        history.back();
      }
    });
  });

  // Footer year
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
