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

  // "¿Atendemos llamadas ahora?" from the hours in data-hours (generated from data/site.json)
  var DAY_NAMES = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes'];
  Array.prototype.forEach.call(document.querySelectorAll('[data-call-status]'), function (box) {
    var hours = JSON.parse(box.getAttribute('data-hours')).map(function (h) {
      var r = h[1].split(/[–-]/);
      return { day: DAY_NAMES.indexOf(h[0].toLowerCase()), from: r[0].trim(), to: r[1].trim() };
    });
    function mins(t) { var p = t.split(':'); return +p[0] * 60 + +p[1]; }
    function render() {
      var now = new Date(), d = now.getDay() - 1, m = now.getHours() * 60 + now.getMinutes();
      var today = hours.filter(function (h) { return h.day === d; })[0];
      var open = !!today && m >= mins(today.from) && m < mins(today.to);
      var text;
      if (open) text = 'Ahora atendemos llamadas, hasta las ' + today.to + '.';
      else if (today && m < mins(today.from)) text = 'Hoy atendemos llamadas de ' + today.from + ' a ' + today.to + '.';
      else {
        var next = null;
        for (var k = 1; k <= 7 && !next; k++) { var dd = (now.getDay() - 1 + k + 7) % 7; next = hours.filter(function (h) { return h.day === dd; })[0]; }
        if (!next) return;
        // tomorrow's index is today's getDay()
        text = 'Ahora no atendemos llamadas. Llámanos ' + (next.day === now.getDay() ? 'mañana' + (now.getDay() === 0 ? ' lunes' : '') : 'el ' + DAY_NAMES[next.day]) + ' de ' + next.from + ' a ' + next.to + ', o escríbenos por WhatsApp.';
      }
      box.classList.toggle('is-open', open);
      box.textContent = text;
    }
    render();
    setInterval(function () { if (!document.hidden) render(); }, 60000);
  });

  // Print the timetable
  Array.prototype.forEach.call(document.querySelectorAll('[data-print]'), function (b) {
    b.style.display = 'inline-flex';
    b.addEventListener('click', function () { window.print(); });
  });

  // Links that open a new tab say so to screen readers
  Array.prototype.forEach.call(document.querySelectorAll('a[target="_blank"]'), function (link) {
    if (link.querySelector('.sr-only')) return;
    var hint = document.createElement('span');
    hint.className = 'sr-only';
    hint.textContent = ' (se abre en otra pestaña)';
    link.appendChild(hint);
  });

  // Footer year
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
