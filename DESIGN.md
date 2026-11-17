# DESIGN.md — Nadia Fitness Dance Studio (v3)

## The decision this page supports

A parent or an adult in Torrox Costa wants to **pick a class that fits who it is for and when they are free, then call to reserve a place.** Everything on the page serves that, in that order:

1. Hero: what the studio is, where, when, and the call button. Real photo of Nadia.
2. Classes: the seven classes, split into Baile and Fitness, each with its days and times.
3. Week: the full timetable to compare days at a glance (a compact table is right here: comparison is the task).
4. Nadia: who teaches, plus the real Google rating.
5. Reserve: phone, call hours, WhatsApp, address and map.

A section that does not help that decision does not ship.

## Tokens (use only these)

```css
--bg: #F6F3EE;      /* warm stone, never pure white */
--card: #FCFBF9;    /* raised surfaces */
--ink: #1C1917;     /* text 15.8:1 on --bg */
--muted: #57534E;   /* secondary text 6.9:1 */
--line: #E2DDD5;    /* borders (decorative) */
--accent: #BF0067;  /* brand pink: primary action and key highlights ONLY (white on it 6.2:1) */
--dark: #16120F;    /* logo badge and map button */
--radius-s: 4px; --radius-m: 8px; --radius-l: 16px;
--section-y: 96px (desktop) / 64px (mobile)
```

- One family: **Bricolage Grotesque** (variable). Headings 650–700, tight tracking (−0.02em). Body 400, 17px/1.6.
- Body text at most **65ch** (≈480px).
- Light mode only for v1.
- Icons: Lucide, 20px, stroke 2, inline beside the text they label.

## Bans (fix the spec, not the page, if 3+ of these slip)

1. No pill label above the hero headline, and **no small uppercase eyebrow above section headings**: put the meaning in the heading.
2. No buzzword headings. Headings state facts: days, times, counts, the phone number.
3. No gradients (backgrounds, text or buttons), no glows, no floating orbs.
4. No centered hero with two buttons. Two columns: copy left, real photo right.
5. No rows of identical tiles or icon-in-a-tinted-square. Use lists and bordered panels.
6. Only one pill-shaped button: the primary "Llamar". Everything else is rectangular (radius 4–8).
7. Shadows only on elevated elements (the hero photo caption). Nothing else casts a shadow.
8. The accent colour is for the primary action and key highlights only. Not for decoration.
9. No invented content: no stats, testimonials, ages or prices we have not been given.
10. No scroll animations, no auto-scrolling strips, no emoji as icons, no "made with ❤️" footer.

## Content rules

- Spanish, second person (tú), direct.
- Real data only (classes, times, address, rating 5,0 · 29 reseñas). Unknown facts stay out.
- Test with long names (e.g. "WeDance Grupo Adulto") and with a day that has no classes in a slot.
