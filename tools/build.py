"""Build every page of the v3 site from data/site.json.

Usage (from the repo root):  python3 tools/build.py

Pages share one header, footer and mobile bar, so they stay consistent.
Classes and the weekly schedule live only in data/site.json.
Read DESIGN.md before changing anything visual.
"""
import html
import json
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8"))
CLASSES = DATA["classes"]
BY_SLUG = {c["c"]: c for c in CLASSES}
SESSIONS = DATA["sessions"]
CSS_V, JS_V = 9, 3

DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
SHORT = ["Lun", "Mar", "Mié", "Jue", "Vie"]
SLOTS = ["Mañana", "Mediodía", "Tarde", "Noche"]
PHONE_HREF = "tel:+34654691336"
PHONE = "654 691 336"
WHATSAPP = "https://wa.me/34654691336?text=%C2%A1Hola!%20Quiero%20informaci%C3%B3n%20sobre%20las%20clases."
MAPS = "https://maps.app.goo.gl/jp69zpacG6Zni4Du5"
REVIEWS = "https://www.google.com/maps/search/?api=1&amp;query=Nadia%20Fitness%20Dance%20Studio%20Torrox"
INSTAGRAM = "https://www.instagram.com/nadiafitnessdancestudio/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61571423443783"
LIVE = "https://negimaru.github.io/nadia-fitness/"
ADDRESS_1, ADDRESS_2 = "Urb. Santa Rosa, Calle Margarita 6", "29793 Torrox Costa, Málaga"

e = html.escape


def minutes(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


# ---------- Lucide icons (20px, stroke 2) ----------
def icon(body, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


I_PHONE = icon('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>')
I_MSG = icon('<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>')
I_PIN = icon('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>')
I_CLOCK = icon('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>')
I_MUSIC = icon('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>')
I_PULSE = icon('<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>')
I_STAR = icon('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', "i i-star")
I_ARROW = icon('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', "i i-arrow")
I_INSTA = icon('<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>')
I_MENU = icon('<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>')
I_SUN = icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>', "i i-sun")
I_MOON = icon('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>', "i i-moon")

NAV = [("", "Inicio"), ("clases/", "Clases"), ("horario/", "Horario"), ("quien-soy/", "Quién soy"), ("contacto/", "Contacto")]


# ---------- Layout ----------
def head(p, title, description, path):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<!-- Design proposal v3: kept out of search results to avoid duplicating the live site -->
<meta name="robots" content="noindex">
<meta name="theme-color" content="#F6F3EE" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#171412" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{LIVE}assets/img/og-nadia-fitness.jpg">
<link rel="icon" href="{p}assets/img/favicon.svg?v=2" type="image/svg+xml">
<script>try{{var t=localStorage.getItem("nf3-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="preload" href="{p}assets/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/fonts.css?v=1">
<link rel="stylesheet" href="{p}assets/css/site.css?v={CSS_V}">
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
'''


def header(p, current):
    links = "".join(
        f'<li><a href="{p}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV)
    return f'''<header class="top">
<div class="wrap top-in">
<a class="logo" href="{p}"><img src="{p}assets/img/logo.png" alt="Nadia Fitness Dance Studio, inicio" width="110" height="60"></a>
<nav class="nav" aria-label="Principal">
<button class="menu" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú">{I_MENU}</button>
<ul id="menu">{links}</ul>
</nav>
<a class="top-phone" href="{PHONE_HREF}">{I_PHONE}{PHONE}</a>
<button class="theme" type="button" aria-label="Cambiar a modo oscuro">{I_MOON}{I_SUN}</button>
</div>
</header>
'''


def footer(p, scripts=()):
    calls = "".join(f"<li><span>{d}</span><span>{h}</span></li>" for d, h in DATA["calls"])
    nav = "".join(f'<li><a href="{p}{href}">{label}</a></li>' for href, label in NAV)
    js = "".join(f'<script src="{p}assets/js/{s}?v={JS_V}" defer></script>\n' for s in ("site.js",) + tuple(scripts))
    return f'''<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-brand">
<a class="logo" href="{p}"><img src="{p}assets/img/logo.png" alt="Nadia Fitness Dance Studio, inicio" width="110" height="60" loading="lazy"></a>
<p>Academia de baile y fitness en Torrox Costa.</p>
<a class="foot-social" href="{INSTAGRAM}" rel="noopener">{I_INSTA}@nadiafitnessdancestudio</a>
</div>
<div>
<h2 class="foot-h">Contacto</h2>
<p><a href="{PHONE_HREF}">{PHONE}</a><br><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></p>
<p>{ADDRESS_1}<br>{ADDRESS_2}</p>
</div>
<div>
<h2 class="foot-h">Horario de llamadas</h2>
<ul class="foot-calls">{calls}</ul>
</div>
<div>
<h2 class="foot-h">Páginas</h2>
<ul class="foot-nav">{nav}</ul>
</div>
</div>
<div class="wrap foot-legal">
<p>© <span id="year">2026</span> Nadia Fitness Dance Studio</p>
<p><a href="{FACEBOOK}" rel="noopener">Facebook</a> · <a href="{p}aviso-legal/">Aviso legal</a> · <a href="{p}privacidad/">Privacidad</a> · Propuesta v3 · <a href="{LIVE}">Web actual</a></p>
</div>
</footer>
<nav class="mbar" aria-label="Contacto rápido"><a class="btn-primary" href="{PHONE_HREF}">{I_PHONE}Llamar</a><a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">{I_MSG}WhatsApp</a></nav>
{js}</body>
</html>
'''


def page_hero(title, lead):
    return f'''<section class="page-hero wrap">
<h1>{title}</h1>
<p class="lead">{lead}</p>
</section>
'''


def rating():
    return f'<a class="rating" href="{REVIEWS}" target="_blank" rel="noopener">{I_STAR}<b>5,0</b> · 29 reseñas en Google</a>'


# ---------- Components ----------
def when_list(slug):
    items = sorted((s for s in SESSIONS if s["c"] == slug), key=lambda s: (s["day"], minutes(s["start"])))
    grouped = OrderedDict()
    for s in items:
        label = f'{s["start"]}–{s["end"]}' + (f' (Int. {s["name"].split()[-1]})' if slug == "dance-intermedio" else "")
        grouped.setdefault(label, []).append(s["day"])
    out = []
    for label, days in grouped.items():
        days = sorted(set(days))
        d = SHORT[days[0]] if len(days) == 1 else ", ".join(SHORT[x] for x in days[:-1]) + " y " + SHORT[days[-1]]
        out.append(f"<li>{d} · {label}</li>")
    return '<ul class="when">' + "".join(out) + "</ul>"


def class_media(c, p, eager=False):
    """Real photo when we have one; otherwise a typographic placeholder (no fake imagery)."""
    if c.get("photo"):
        lazy = "" if eager else ' loading="lazy"'
        if c.get("placeholder"):
            # Placeholder image: replace assets/img/{photo} with a real photo of the same name
            return (f'<img class="media media-placeholder" src="{p}assets/img/{c["photo"]}?v=1" alt="{e(c["photo_alt"])}" '
                    f'width="1200" height="750"{lazy}><!-- TODO: real photo → overwrite assets/img/{c["photo"]} -->')
        return (f'<img class="media" src="{p}assets/img/{c["photo"]}" alt="{e(c["photo_alt"])}" '
                f'width="840" height="840"{lazy}>')
    ico = I_MUSIC if c["group"] == "baile" else I_PULSE
    label = "Baile" if c["group"] == "baile" else "Fitness"
    return (f'<div class="media media-ph" aria-hidden="true">{ico}<span>{label}</span></div>'
            f'<!-- TODO: real photo for {c["name"]} -->')


def class_card(c, p, detail=False):
    group = "Baile" if c["group"] == "baile" else "Fitness"
    desc = c["desc_long"] if detail else c["desc"]
    actions = (f'<div class="card-actions"><a class="btn" href="{p}contacto/">Reservar plaza</a>'
               f'<a class="link" href="{p}horario/">Ver en el horario{I_ARROW}</a></div>') if detail else ""
    title = f'<h3>{e(c["name"])}</h3>' if detail else f'<h3><a href="{p}clases/#{c["c"]}">{e(c["name"])}</a></h3>'
    return f'''<article class="card{" card-detail" if detail else ""}" id="{c["c"] if detail else ""}">
{class_media(c, p)}
<div class="card-body">
<p class="who">{group} · {e(c["who"])}</p>
{title}
<p>{e(desc)}</p>
{when_list(c["c"])}
{actions}
</div>
</article>'''.replace(' id=""', "")


def schedule(p):
    """Weekly table (works without JS) + data for the interactive layer in schedule.js."""
    head_row = "".join(f'<th scope="col">{d}</th>' for d in DAYS)
    rows = []
    for slot in SLOTS:
        cells = []
        for d in range(5):
            items = sorted((s for s in SESSIONS if s["day"] == d and s["slot"] == slot), key=lambda s: minutes(s["start"]))
            if items:
                lis = "".join(
                    f'<li data-c="{s["c"]}" class="g-{BY_SLUG[s["c"]]["group"]}"><time>{s["start"]}–{s["end"]}</time>'
                    f'<span>{e(s["name"])}</span></li>' for s in items)
                cells.append(f"<td><ul>{lis}</ul></td>")
            else:
                cells.append('<td><span class="none">—</span></td>')
        rows.append(f'<tr><th scope="row">{slot}</th>{"".join(cells)}</tr>')
    payload = json.dumps({
        "days": DAYS,
        "classes": [{"c": c["c"], "name": c["name"], "group": c["group"], "who": c["who"]} for c in CLASSES],
        "sessions": [{k: s[k] for k in ("day", "start", "end", "c", "name", "note", "slot")} for s in SESSIONS],
        "classesHref": f"{p}clases/",
    }, ensure_ascii=False)
    return f'''<div class="schedule" data-schedule>
<div class="table-wrap"><table class="week"><caption class="sr-only">Horario semanal de lunes a viernes</caption>
<thead><tr><td></td>{head_row}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<script type="application/json" class="schedule-data">{payload}</script>
</div>
'''


def steps():
    return '''<ol class="steps">
<li><b>Elige tu clase</b><span>Mira el horario y busca el grupo que encaja con tu nivel y tu semana.</span></li>
<li><b>Llámanos o escríbenos</b><span>Te decimos si queda plaza en el grupo y te la guardamos.</span></li>
<li><b>Ven a clase</b><span>Con ropa cómoda, agua y ganas.</span></li>
</ol>
'''


def reserve_band(p):
    return f'''<section class="sec wrap band" aria-labelledby="band-h">
<div>
<h2 id="band-h">Reserva tu plaza llamando al <a href="{PHONE_HREF}">{PHONE}</a></h2>
<p class="intro">Llamadas de lunes a viernes; consulta el horario de llamadas en el pie. Si prefieres escribir, usa WhatsApp.</p>
</div>
<div class="band-actions"><a class="btn-primary" href="{PHONE_HREF}">{I_PHONE}Llamar</a><a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">{I_MSG}WhatsApp</a></div>
</section>
'''


# ---------- Pages ----------
def page_home():
    p = ""
    cards = "".join(class_card(c, p) for c in CLASSES)
    return head(p, "Nadia Fitness Dance Studio · Clases de baile y fitness en Torrox Costa",
                "Clases de baile y fitness en Torrox Costa, de lunes a viernes de 9:30 a 21:30: grupos de dance por niveles, Fitdance, PowerHIIT y Aquafitness. Reserva en el 654 691 336.", "") + header(p, "") + f'''<main id="main">
<section class="hero wrap">
<div class="hero-copy">
<h1>Clases de baile y fitness en Torrox Costa, de lunes a viernes</h1>
<p class="lead">De 9:30 a 21:30 en Urb. Santa Rosa. Grupos de dance por niveles, desde los más pequeños hasta adultos, y clases de Fitdance, PowerHIIT y Aquafitness. Plazas limitadas por grupo.</p>
<div class="actions"><a class="btn-primary" href="{PHONE_HREF}">{I_PHONE}Llamar al {PHONE}</a><a class="link" href="horario/">Ver el horario de la semana{I_ARROW}</a></div>
</div>
<figure class="hero-photo">
<img src="assets/img/monitora-fitdance.webp" alt="Nadia, monitora del estudio, con micrófono antes de una clase" width="840" height="840" fetchpriority="high">
<figcaption class="caption"><span><b>Nadia</b> · monitora del estudio</span>{rating()}</figcaption>
</figure>
</section>
<figure class="wrap banner"><img src="assets/img/clase-aire-libre-1.webp" alt="Tres monitoras de espaldas, con los brazos en alto, dirigen una clase de baile al aire libre junto al mar" width="1600" height="500" loading="lazy"></figure>

<section class="sec wrap" aria-labelledby="clases-h">
<div class="sec-head"><div><h2 id="clases-h">Siete clases, cada una con su grupo y su horario fijo</h2>
<p class="intro">Cuatro de baile por niveles y tres de fitness para adultos.</p></div>
<a class="link" href="clases/">Ver todas las clases{I_ARROW}</a></div>
<div class="cards cards-classes">{cards}</div>
</section>

<section class="sec wrap" aria-labelledby="semana-h">
<div class="sec-head"><div><h2 id="semana-h">{len(SESSIONS)} clases a la semana, de 9:30 a 21:30</h2>
<p class="intro">Curso 2026/27. Pulsa una clase para ver solo sus horas.</p></div>
<a class="link" href="horario/">Horario completo{I_ARROW}</a></div>
{schedule(p)}
</section>

<section class="sec wrap" aria-labelledby="nadia-h">
<div class="teaser">
<img class="avatar" src="assets/img/monitora-fitdance.webp" alt="" width="840" height="840" loading="lazy">
<div><h2 id="nadia-h">Nadia, monitora del estudio</h2>
<p class="intro">Da clase a todos los grupos: dance por niveles, Fitdance, PowerHIIT y Aquafitness.</p>
{rating()}</div>
<a class="link" href="quien-soy/">Conoce a Nadia{I_ARROW}</a>
</div>
</section>

<section class="sec wrap" aria-labelledby="pasos-h">
<h2 id="pasos-h">Apuntarse lleva tres pasos</h2>
{steps()}
</section>
{reserve_band(p)}</main>
''' + footer(p, ("schedule.js",))


def page_classes():
    p = "../"
    baile = "".join(class_card(c, p, True) for c in CLASSES if c["group"] == "baile")
    fitness = "".join(class_card(c, p, True) for c in CLASSES if c["group"] == "fitness")
    jump = "".join(f'<li><a href="#{c["c"]}">{e(c["name"])}</a></li>' for c in CLASSES)
    return head(p, "Clases de baile y fitness en Torrox Costa · Nadia Fitness",
                "Grupo Dance Baby, Intermedio, Avanzado y Adultos, Fitdance, PowerHIIT y Aquafitness en Torrox Costa. Horarios y reservas en el 654 691 336.", "clases/") + header(p, "clases/") + f'''<main id="main">
{page_hero("Siete clases de baile y fitness en Torrox Costa", "Cada clase tiene su grupo y su horario fijo de lunes a viernes. Para tarifas y plazas libres, llámanos al " + PHONE + ".")}
<nav class="wrap jump" aria-label="Ir a una clase"><ul>{jump}</ul></nav>
<section class="sec wrap" aria-labelledby="baile-h">
<h2 id="baile-h">{I_MUSIC}Baile: cuatro grupos por niveles</h2>
<div class="cards cards-detail">{baile}</div>
</section>
<section class="sec wrap" aria-labelledby="fitness-h">
<h2 id="fitness-h">{I_PULSE}Fitness: tres clases para adultos</h2>
<div class="cards cards-detail">{fitness}</div>
</section>
{reserve_band(p)}</main>
''' + footer(p)


def page_schedule():
    p = "../"
    return head(p, "Horario curso 26/27 · Nadia Fitness Dance Studio, Torrox Costa",
                "Horario de clases del curso 2026/27 en Nadia Fitness Dance Studio, Torrox Costa: dance por niveles, Fitdance, PowerHIIT y Aquafitness de lunes a viernes.", "horario/") + header(p, "horario/") + f'''<main id="main">
{page_hero(f"{len(SESSIONS)} clases a la semana, de 9:30 a 21:30", "Horario del curso 2026/27, de lunes a viernes. Pulsa una clase para ver solo sus horas. Plazas limitadas por grupo: llámanos para confirmar.")}
<section class="sec sec-first wrap" aria-label="Horario semanal">
{schedule(p)}
</section>
{reserve_band(p)}</main>
''' + footer(p, ("schedule.js",))


def page_about():
    p = "../"
    groups = []
    for key, title, ico in (("baile", "Baile", I_MUSIC), ("fitness", "Fitness", I_PULSE)):
        items = "".join(f'<li><a href="{p}clases/#{c["c"]}">{e(c["name"])}</a><span>{e(c["who"])}</span></li>'
                        for c in CLASSES if c["group"] == key)
        groups.append(f'<div class="panel"><h3>{ico}{title}</h3><ul class="plain">{items}</ul></div>')
    return head(p, "Quién soy · Nadia, monitora de baile y fitness en Torrox Costa",
                "Soy Nadia, monitora de Nadia Fitness Dance Studio en Torrox Costa: grupos de dance por niveles, Fitdance, PowerHIIT y Aquafitness.", "quien-soy/") + header(p, "quien-soy/") + f'''<main id="main">
<section class="hero wrap">
<div class="hero-copy">
<h1>Hola, soy Nadia, monitora de baile y fitness en Torrox Costa</h1>
<!-- TODO: replace with Nadia's own words (background, training, years teaching) -->
<p class="lead">Doy clase a los grupos de dance por niveles, desde los más pequeños hasta adultos, y a Fitdance, PowerHIIT y Aquafitness.</p>
<p class="lead">En mis clases cada persona avanza a su ritmo: técnica, coreografía y entrenamiento en serio, en buen ambiente. Si nunca has bailado, te ayudo a encontrar tu grupo.</p>
<div class="actions">{rating()}</div>
</div>
<figure class="hero-photo"><img src="{p}assets/img/monitora-fitdance.webp" alt="Nadia con micrófono antes de una clase" width="840" height="840" fetchpriority="high"></figure>
</section>
<figure class="wrap banner"><img src="{p}assets/img/clase-aire-libre-2.webp" alt="Tres monitoras de espaldas, en plena coreografía, dirigen una clase de baile al aire libre junto al mar" width="1600" height="478" loading="lazy"></figure>
<section class="sec wrap" aria-labelledby="mis-h">
<div class="sec-head"><h2 id="mis-h">Las siete clases que doy</h2><a class="link" href="{p}clases/">Ver todas las clases{I_ARROW}</a></div>
<div class="two">{"".join(groups)}</div>
</section>
{reserve_band(p)}</main>
''' + footer(p)


def page_contact():
    p = "../"
    options = "".join(f"<option>{e(c['name'])}</option>" for c in CLASSES) + "<option>Aún no lo sé</option>"
    calls = "".join(f"<tr><th scope='row'>{d}</th><td>{h}</td></tr>" for d, h in DATA["calls"])
    return head(p, "Contacto y reservas · Nadia Fitness Dance Studio, Torrox Costa",
                "Llama al 654 691 336 o escríbenos por WhatsApp para reservar tu plaza. Nadia Fitness Dance Studio, Urb. Santa Rosa, Torrox Costa.", "contacto/") + header(p, "contacto/") + f'''<main id="main">
{page_hero(f'Reserva tu plaza llamando al <a href="{PHONE_HREF}">{PHONE}</a>', "Te decimos si queda sitio en el grupo y te la guardamos. Si prefieres escribir, usa el formulario: abre WhatsApp con tu mensaje ya escrito.")}
<section class="sec sec-first wrap contact" aria-label="Formas de contacto">
<div class="contact-side">
<div class="panel"><h2>{I_CLOCK}Horario de llamadas</h2><table class="calls">{calls}</table>
<a class="btn-primary" href="{PHONE_HREF}">{I_PHONE}Llamar al {PHONE}</a></div>
<div class="panel"><h2>{I_PIN}{ADDRESS_1}</h2><p class="muted">{ADDRESS_2}</p>
<a class="map" href="{MAPS}" target="_blank" rel="noopener"><img src="{p}assets/img/mapa.webp" alt="Mapa de Urb. Santa Rosa con la academia en la Calle Margarita" width="1280" height="720" loading="lazy"><span class="pin" aria-hidden="true"></span><span class="map-go">Cómo llegar</span></a>
<p class="osm">Mapa © <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a></p></div>
</div>
<form class="panel form" id="contact-form">
<h2>{I_MSG}Escríbenos por WhatsApp</h2>
<div class="field"><label for="contact-name">Nombre</label><input id="contact-name" name="contact-name" autocomplete="name" required placeholder="Tu nombre"></div>
<div class="field"><label for="contact-phone">Teléfono <span class="opt">(opcional)</span></label><input id="contact-phone" name="contact-phone" type="tel" autocomplete="tel" placeholder="+34"></div>
<div class="field"><label for="contact-class">Clase que te interesa</label><select id="contact-class" name="contact-class">{options}</select></div>
<div class="field"><label for="contact-message">Mensaje <span class="opt">(opcional)</span></label><textarea id="contact-message" name="contact-message" rows="4" placeholder="Edad, nivel, dudas…"></textarea></div>
<button class="btn" type="submit">{I_MSG}Abrir WhatsApp con el mensaje</button>
<p class="muted small">No guardamos ningún dato en esta web: el mensaje solo se envía si lo mandas tú desde WhatsApp.</p>
</form>
</section>
<section class="sec wrap" aria-labelledby="pasos-h">
<h2 id="pasos-h">Apuntarse lleva tres pasos</h2>
{steps()}
</section>
</main>
''' + footer(p, ("contact.js",))


BACK = '<a class="link back-link" href="../" data-back><span aria-hidden="true">←</span> Volver</a>'


def page_legal(slug):
    p = "../"
    L = DATA["legal"][slug]
    return head(p, L["title"], L["lead"], f"{slug}/") + header(p, None) + f'''<main id="main">
<p class="wrap back">{BACK}</p>
{page_hero(e(L["h1"]), e(L["lead"]))}
<section class="sec sec-first wrap prose">
<!-- TODO: fill in the highlighted placeholders (.ph-mark) with the owner's details -->
{L["body"]}
<p class="back back-end">{BACK}</p>
</section>
</main>
''' + footer(p)


def page_404():
    p = "./"
    return head("", "Página no encontrada · Nadia Fitness Dance Studio", "Esta página no existe.", "").replace(
        'href="assets/', 'href="/nadia-fitness-v3/assets/').replace('src="assets/', 'src="/nadia-fitness-v3/assets/') + header("/nadia-fitness-v3/", None) + f'''<main id="main">
{page_hero("Esta página no existe", "Puede que el enlace esté mal o que la página se haya movido.")}
<section class="sec sec-first wrap"><a class="btn-primary" href="/nadia-fitness-v3/">Ir al inicio</a></section>
</main>
''' + footer("/nadia-fitness-v3/")


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


if __name__ == "__main__":
    write("index.html", page_home())
    write("clases/index.html", page_classes())
    write("horario/index.html", page_schedule())
    write("quien-soy/index.html", page_about())
    write("contacto/index.html", page_contact())
    write("aviso-legal/index.html", page_legal("aviso-legal"))
    write("privacidad/index.html", page_legal("privacidad"))
    write("404.html", page_404())
