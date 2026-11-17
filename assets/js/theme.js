// Light / dark theme: follows the OS until a choice is made with the toggle,
// which is then remembered in this browser.
(function () {
  var KEY = 'nf3-theme';
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var button = document.querySelector('.theme');

  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(theme) {
    root.setAttribute('data-theme', theme);
    if (button) button.setAttribute('aria-label', theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
  }

  apply(stored() || (media && media.matches ? 'dark' : 'light'));
  if (media && media.addEventListener) {
    media.addEventListener('change', function (e) { if (!stored()) apply(e.matches ? 'dark' : 'light'); });
  }
  if (button) {
    button.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(KEY, next); } catch (e) {}
      apply(next);
    });
  }
})();
