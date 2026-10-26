# 05 · Web y dominio: isla.capitaltorreon.com

[← Volver al README](../README.md)

## Cómo está conectado

| Pieza | Valor |
|---|---|
| Dominio | **https://isla.capitaltorreon.com** (dominio propio del Worker; Cloudflare crea DNS y certificado solo) |
| Worker | `isla` · cuenta SuperLeads de Cloudflare |
| Configuración | [`wrangler.jsonc`](../wrangler.jsonc) |
| Qué se publica | La carpeta [`web/`](../web/) (assets estáticos) + el Worker [`src/index.js`](../src/index.js), que sólo atiende `/proyecciones` y `/api/*` |
| Login | [Login de CapitalTorreon](https://login.capitaltorreon.com): el widget arriba a la derecha en todas las páginas; el servidor verifica el pase con [`src/verificar.js`](../src/verificar.js) |
| Base de datos | D1 `isla` (`33c4e9bc-e84e-4cea-ac80-8979bb9b4e20`): tablas `escenarios` y `bitacora` ([`migraciones/`](../migraciones/)) |
| Página privada | **/proyecciones**: sólo abre con los correos de `PERMITIDOS` en `wrangler.jsonc` (los de Ricardo; entra como contacto@ingenieriadigital.mx y se muestra ricardo@superleads.mx) |
| Página | [`web/index.html`](../web/index.html): «En construcción · trabajando» |
| 404 | [`web/404.html`](../web/404.html): «Esta parte de la isla aún no existe» |
| Imágenes | `web/img/*.webp` (renders comprimidos) y `web/img/og.jpg` (vista previa al compartir, 1200×630) |
| Repo | https://github.com/ricardolopezreyero/isla |

## La página privada /proyecciones

- El HTML es un cascarón sin números. Los datos salen de `POST /api/proyecciones/{datos|guardar|borrar}` con el pase del login, y sólo si el correo está en `PERMITIDOS`. Otro correo ve «Esta página es privada».
- Respuestas con `no-store`, `noindex`, `X-Frame-Options: DENY` y `Referrer-Policy: no-referrer`; se rechazan POST de otros orígenes.
- Cada vez que entras, guardas o borras un escenario queda un renglón en la `bitacora` (el principio de la [bitácora de cada huésped](08-bitacora.md)).
- Para dar acceso a alguien más: agregar su correo a `PERMITIDOS` y desplegar.

## Publicar un cambio

Desde la raíz del repo (la terminal trae un token de otro proyecto; por eso el `env -u`):

```bash
cd ~/Code/isla && git add -A && git commit -m "Web: …" && git push && env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npx -y wrangler@latest deploy
```

Si se agrega una migración nueva en `migraciones/`, antes del deploy:

```bash
cd ~/Code/isla && env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npx -y wrangler@latest d1 migrations apply isla --remote
```

## Probar en local

```bash
cd ~/Code/isla && env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npx -y wrangler@latest dev --port 8787
```

y abrir http://localhost:8787. Para probar /proyecciones sin la llave real del login, `.dev.vars` (no se sube) trae `JWKS_PRUEBA` con una llave pública de prueba; sólo en local se aceptan pases firmados con ella.

## Qué tiene la página hoy

1. Portada con la panorámica, la etiqueta **«En construcción · trabajando»** y el logo **ISLA / La Encantada** (archivo en `web/img/logo.svg`).
2. Cuatro cifras: 3–4 km · 800 habitaciones · 80 villas · 1,820 de staff.
3. **Cómo vamos**: las 5 etapas (Base → Fase D) con su estado. Se edita en el arreglo `FASES` dentro de `web/index.html`.
4. Galería con 5 renders.
5. Catálogo en cifras: 50 · 70 · 100 · 100 · 120 · 200.
6. Botones **A− / A+** (letra de 90 % a 145 %, se recuerda en el navegador y viaja con la cuenta) y el login de la casa.

## Cómo va a crecer el sitio

La carpeta `web/` está pensada para ir sumando páginas sin rehacer nada:

| Cuándo | Qué se agrega | Dónde |
|---|---|---|
| Fase B | Capturas y video del greybox | `web/avances/` |
| Fase C | Galería de habitación, villa y restaurante terminados | `web/galeria/` |
| Cuando convenga | Catálogos navegables (menú, spa, tiendas, flora y fauna) leyendo `data/*.json` | `web/catalogo/` |
| Fase D | Recorrido en video de la demo jugable | portada |
| Fase A | Lista de espera con la pregunta de precio | `src/` + D1 |
| Más adelante | Reservas sin sobreventa y la bitácora de cada huésped | `src/` + D1 |
| Más adelante | Pixel Streaming para jugar desde el navegador | subdominio aparte |

Para una ruta nueva con lógica de servidor: agregarla a `run_worker_first` en `wrangler.jsonc` y atenderla en `src/index.js`; los assets de `web/` siguen igual.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
