# Nadia Fitness Dance Studio — propuesta v3

Web completa de [Nadia Fitness Dance Studio](https://negimaru.github.io/nadia-fitness/) con un diseño hecho para no parecer una plantilla generada con IA. Las reglas están en [`DESIGN.md`](DESIGN.md): la decisión que ayuda a tomar cada página, los tokens, los componentes y 10 prohibiciones. [`CLAUDE.md`](CLAUDE.md) obliga a leerlas.

**Páginas:** Inicio · Clases · Horario · Quién soy · Contacto · Aviso legal · Privacidad · 404.

- **Títulos con datos:** «22 clases a la semana, de 9:30 a 21:30», «Reserva tu plaza llamando al 654 691 336». No hay etiquetas pequeñas sobre los títulos.
- **Sistema contenido:** una tipografía (Bricolage Grotesque), neutros cálidos, un único acento rosa y una sola píldora (el botón «Llamar»). Radios de 4, 8 y 16 px e iconos Lucide.
- **Fotos:** las clases con foto real la muestran. Las demás llevan una imagen de muestra con el estilo de la web en `assets/img/clases/<clase>.webp`; para poner la foto real, sustituye el archivo por otro con el mismo nombre (horizontal, ~1200×750). `tools/make_placeholders.py` regenera las de muestra.
- **Horario interactivo:** botones para resaltar una clase. En el móvil, pestañas por día que abren en el de hoy, y se puede deslizar.
- **Contacto:** formulario que abre WhatsApp con el mensaje escrito (no guarda nada), mapa fijo de OpenStreetMap y 3 pasos.
- **Modo claro y oscuro** según el sistema, con botón sol/luna. Barra de Llamar/WhatsApp en el móvil. Lleva `noindex`.

## Cómo se edita

El contenido (clases, horario, horario de llamadas y textos legales) está en `data/site.json`. Las páginas se generan con:

```
python3 tools/build.py
```

```
data/site.json          Contenido: una sola fuente para clases y horario
tools/build.py          Plantillas y generación de todas las páginas
assets/css/site.css     Estilos (solo los tokens de DESIGN.md)
assets/js/site.js       Tema, menú móvil, año del pie
assets/js/schedule.js   Filtros del horario y pestañas por día en el móvil
assets/js/contact.js    Formulario → WhatsApp
```

Comparativa: [web actual](https://negimaru.github.io/nadia-fitness/) · [propuesta v2](https://negimaru.github.io/nadia-fitness-alt/) · propuesta v3.

## Funciones

- **«¿Atendemos llamadas ahora?»** junto al teléfono, calculado a partir del horario de llamadas de `data/site.json`.
- **Horario imprimible** en un folio A4 apaisado, con el botón «Imprimir horario».
- **Imagen para compartir el Horario** (`assets/img/og-horario.jpg`): se genera en la v2 con `tools/make_og_horario.py`. Si cambia el horario, hay que regenerarla y copiarla aquí.
