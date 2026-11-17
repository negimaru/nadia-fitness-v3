// Interactive schedule. Reads the JSON next to each weekly table and adds:
//  - class filter buttons (highlight that class in the table),
//  - on mobile, day tabs that open on today (Monday at weekends) with a list per day;
//    with a class selected, the list shows that class across the week.
// Without JS the plain table stays visible.
(function () {
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function minutes(t) { var p = t.split(':'); return +p[0] * 60 + +p[1]; }

  Array.prototype.forEach.call(document.querySelectorAll('[data-schedule]'), function (root) {
    var data = JSON.parse(root.querySelector('.schedule-data').textContent);
    var table = root.querySelector('.week');
    var items = table.querySelectorAll('li[data-c]');
    var byClass = {};
    data.classes.forEach(function (c) { byClass[c.c] = c; });
    var sessions = data.sessions.slice().sort(function (a, b) { return minutes(a.start) - minutes(b.start); });
    var current = '';

    // --- Filter buttons
    var filters = el('div', 'filters');
    filters.setAttribute('role', 'group');
    filters.setAttribute('aria-label', 'Filtrar el horario por clase');
    var status = el('p', 'sr-only');
    status.setAttribute('aria-live', 'polite');
    function filterButton(slug, label) {
      var b = el('button', 'filter' + (slug ? ' g-' + byClass[slug].group : ''), label);
      b.type = 'button';
      b.setAttribute('data-c', slug);
      b.addEventListener('click', function () {
        select(b.getAttribute('aria-pressed') === 'true' || !slug ? '' : slug);
      });
      filters.appendChild(b);
    }
    filterButton('', 'Todas');
    data.classes.forEach(function (c) { filterButton(c.c, c.name); });

    // --- Mobile agenda
    var agenda = el('div', 'agenda');
    var tabs = el('div', 'tabs');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', 'Día de la semana');
    var panel = el('div', 'agenda-panel');
    panel.setAttribute('role', 'tabpanel');
    panel.id = 'agenda-' + Math.random().toString(36).slice(2, 7);
    var weekday = new Date().getDay();
    var todayIdx = weekday >= 1 && weekday <= 5 ? weekday - 1 : -1;
    var day = todayIdx >= 0 ? todayIdx : 0;
    var tabButtons = data.days.map(function (name, i) {
      var count = sessions.filter(function (s) { return s.day === i; }).length;
      var t = el('button', 'tab');
      t.type = 'button';
      t.id = panel.id + '-t' + i;
      t.setAttribute('role', 'tab');
      t.setAttribute('aria-controls', panel.id);
      t.appendChild(el('b', null, name.slice(0, 3)));
      t.appendChild(el('span', null, i === todayIdx ? 'Hoy' : count + ' clases'));
      t.addEventListener('click', function () { day = i; if (current) select(''); else render(); });
      t.addEventListener('keydown', function (e) {
        var step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!step || current) return;
        e.preventDefault();
        day = (day + step + data.days.length) % data.days.length;
        render();
        tabButtons[day].focus();
      });
      tabs.appendChild(t);
      return t;
    });
    agenda.appendChild(tabs);
    agenda.appendChild(panel);

    function row(s) {
      var a = el('a', 'agenda-row g-' + byClass[s.c].group);
      a.href = data.classesHref + '#' + s.c;
      var time = el('span', 'agenda-time');
      time.appendChild(el('b', null, s.start));
      time.appendChild(el('span', null, s.end));
      var info = el('span', 'agenda-info');
      info.appendChild(el('b', null, s.name));
      info.appendChild(el('span', null, (s.note ? s.note + ' · ' : '') + (minutes(s.end) - minutes(s.start)) + ' min'));
      a.appendChild(time);
      a.appendChild(info);
      a.setAttribute('aria-label', s.name + ', de ' + s.start + ' a ' + s.end + '. Ver la clase');
      return a;
    }

    function render() {
      panel.innerHTML = '';
      tabButtons.forEach(function (t, i) {
        var has = current && sessions.some(function (s) { return s.day === i && s.c === current; });
        t.setAttribute('aria-selected', String(!current && i === day));
        t.tabIndex = !current && i === day ? 0 : -1;
        t.classList.toggle('has', !!has);
      });
      agenda.classList.toggle('is-class', !!current);
      var list, groupOf;
      if (current) {
        list = sessions.filter(function (s) { return s.c === current; })
          .sort(function (a, b) { return a.day - b.day || minutes(a.start) - minutes(b.start); });
        groupOf = function (s) { return data.days[s.day]; };
        panel.removeAttribute('aria-labelledby');
        panel.setAttribute('aria-label', 'Semana de ' + byClass[current].name);
      } else {
        list = sessions.filter(function (s) { return s.day === day; });
        groupOf = function (s) { return s.slot; };
        panel.removeAttribute('aria-label');
        panel.setAttribute('aria-labelledby', tabButtons[day].id);
      }
      if (!list.length) { panel.appendChild(el('p', 'muted', 'No hay clases este día.')); return; }
      var last = null, ul;
      list.forEach(function (s) {
        var g = groupOf(s);
        if (g !== last) { panel.appendChild(el('h3', 'agenda-group', g)); ul = el('ul', 'agenda-list'); panel.appendChild(ul); last = g; }
        var li = el('li'); li.appendChild(row(s)); ul.appendChild(li);
      });
    }

    // Swipe left/right on the list to change day
    var x0 = null, y0 = 0;
    panel.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    panel.addEventListener('touchend', function (e) {
      if (x0 === null || current) { x0 = null; return; }
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        day = (day + (dx < 0 ? 1 : -1) + data.days.length) % data.days.length;
        render();
      }
    });

    function select(slug) {
      current = slug;
      var n = 0;
      Array.prototype.forEach.call(items, function (li) {
        var on = !!slug && li.getAttribute('data-c') === slug;
        li.classList.toggle('is-on', on);
        if (on) n++;
      });
      table.classList.toggle('is-filtering', !!slug);
      Array.prototype.forEach.call(filters.children, function (b) {
        b.setAttribute('aria-pressed', String(b.getAttribute('data-c') === slug));
      });
      status.textContent = slug ? byClass[slug].name + ': ' + n + (n === 1 ? ' sesión' : ' sesiones') + ' a la semana' : 'Mostrando todas las clases';
      render();
    }

    root.insertBefore(filters, root.firstChild);
    root.insertBefore(status, filters.nextSibling);
    root.appendChild(agenda);
    root.classList.add('is-enhanced');
    select('');
    status.textContent = '';
  });
})();
