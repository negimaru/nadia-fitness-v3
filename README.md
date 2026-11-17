# Nadia Fitness Dance Studio — propuesta v3

Tercera versión de la web de [Nadia Fitness Dance Studio](https://negimaru.github.io/nadia-fitness/), hecha para no parecer una plantilla generada con IA. Las reglas están en [`DESIGN.md`](DESIGN.md): tokens, 10 prohibiciones y la decisión que la página ayuda a tomar. [`CLAUDE.md`](CLAUDE.md) obliga a leerlas antes de cualquier cambio de diseño.

- **Decisión primero:** elegir clase y hora, y llamar para reservar. El orden de las secciones sigue esa decisión: hero, clases, semana, Nadia y reservar.
- **Títulos con datos:** «22 clases a la semana, de 9:30 a 21:30», «Reserva tu plaza llamando al 654 691 336». No hay etiquetas pequeñas en mayúsculas sobre los títulos ni una píldora sobre el titular principal.
- **Hero en dos columnas:** el texto a la izquierda y una foto real de Nadia a la derecha, con su valoración real de Google.
- **Sin rasgos de plantilla:** una sola tipografía (Bricolage Grotesque), neutros cálidos sin blanco puro y un único acento rosa reservado a la acción principal. Sin degradados ni brillos, con una única píldora (el botón «Llamar»), radios de 4, 8 y 16 px y sombra solo en la tarjeta que flota sobre la foto. Iconos Lucide de 20 px junto al texto.
- **Modo claro y oscuro:** sigue al sistema, con un botón sol/luna en la cabecera. El único JavaScript es el del cambio de tema. Lleva `noindex`, y los enlaces legales apuntan a la web actual.

Comparativa: [web actual](https://negimaru.github.io/nadia-fitness/) · [propuesta v2](https://negimaru.github.io/nadia-fitness-alt/) · propuesta v3.

Para probarla en local: `python3 -m http.server` y abre `http://localhost:8000`.
