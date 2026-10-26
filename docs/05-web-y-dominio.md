# 05 · Web y dominio: isla.capitaltorreon.com

[← Volver al README](../README.md)

## Cómo está conectado

| Pieza | Valor |
|---|---|
| Dominio | **https://isla.capitaltorreon.com** (dominio propio del Worker; Cloudflare crea DNS y certificado solo) |
| Worker | `isla` · cuenta SuperLeads de Cloudflare |
| Configuración | [`wrangler.jsonc`](../wrangler.jsonc) |
| Qué se publica | Sólo la carpeta [`web/`](../web/) (assets estáticos) |
| Página | [`web/index.html`](../web/index.html): «En construcción · trabajando» |
| 404 | [`web/404.html`](../web/404.html): «Esta parte de la isla aún no existe» |
| Imágenes | `web/img/*.webp` (renders comprimidos) y `web/img/og.jpg` (vista previa al compartir, 1200×630) |
| Repo | https://github.com/ricardolopezreyero/isla |

## Publicar un cambio

Desde la raíz del repo:

```bash
cd ~/Code/isla && git add -A && git commit -m "Web: …" && git push && npx wrangler deploy
```

No hay despliegue automático: después de cada cambio en `web/` hay que correr `npx wrangler deploy`. Si la terminal trae un `CLOUDFLARE_API_TOKEN` de otro proyecto y el deploy responde «No access», correrlo así:

```bash
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npx wrangler deploy
```

## Probar en local

```bash
python3 -m http.server 8787 --directory ~/Code/isla/web
```

y abrir http://localhost:8787.

## Qué tiene la página hoy

1. Portada con la panorámica, la etiqueta **«En construcción · trabajando»** y el nombre.
2. Cuatro cifras: 3–4 km · 800 habitaciones · 80 villas · 1,200 de staff.
3. **Cómo vamos**: las 5 etapas (Base → Fase D) con su estado. Se edita en el arreglo `FASES` dentro de `web/index.html`.
4. Galería con 5 renders.
5. Catálogo en cifras: 50 · 70 · 100 · 100 · 120 · 200.
6. Botones **A− / A+** (letra de 90 % a 145 %, se recuerda en el navegador).

## Cómo va a crecer el sitio

La carpeta `web/` está pensada para ir sumando páginas sin rehacer nada:

| Cuándo | Qué se agrega | Dónde |
|---|---|---|
| Fase B | Capturas y video del greybox | `web/avances/` |
| Fase C | Galería de habitación, villa y restaurante terminados | `web/galeria/` |
| Cuando convenga | Catálogos navegables (menú, spa, tiendas, flora y fauna) leyendo `data/*.json` | `web/catalogo/` |
| Fase D | Recorrido en video de la demo jugable | portada |
| Más adelante | Lista de espera / reservas (Worker + D1) y login único de CapitalTorreon | `src/` + `wrangler.jsonc` |
| Más adelante | Pixel Streaming para jugar desde el navegador | subdominio aparte |

Cuando haga falta lógica de servidor (formularios, reservas), se agrega un `src/index.js` y `"main"` en `wrangler.jsonc`; los assets de `web/` siguen igual.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
