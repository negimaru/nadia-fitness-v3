# Project rules

- Read `DESIGN.md` before any UI task, and follow its tokens and bans.
- Pages are generated: edit `data/site.json` (content) or `tools/build.py` (markup), then run `python3 tools/build.py`. Do not hand-edit the generated `.html` files.
- Code (identifiers, CSS classes, comments) in English; visible content in Spanish.
- Use only the CSS variables defined in `assets/css/site.css` `:root`. Do not add new colours, radii or fonts.
- Content comes from the client. Never invent prices, ages, testimonials or stats.
- If three or more DESIGN.md bans fail in a change, update DESIGN.md first, then redo the change.
