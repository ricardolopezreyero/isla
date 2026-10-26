# 00 · Visión del proyecto

[← Volver al README](../README.md)

## En una frase

Un mundo virtual 3D persistente, calidad AAA, en una isla volcánica privada convertida en mega-resort de lujo para familias y parejas, donde **todo tiene tamaño, altura y distancia de un resort real**, pero con lo mejor de un mundo virtual: sin desgaste, sin fallas, sin clima incómodo.

## El criterio que manda sobre todo lo demás

> Que la persona sienta que **alguien pensó en absolutamente todos los detalles**: proporciones reales, ergonomía perfecta, límites de capacidad física y una experiencia visual, táctil (imaginaria) y sonora exquisita.

De ahí salen cinco principios de trabajo para cualquier decisión de diseño o de código:

1. **Semi realista, al centímetro.** Camas, lavabos, mesas, sillas, pasillos y regaderas se modelan con las medidas de la biblia (por ejemplo: colchón a 55–60 cm del piso, cubierta de lavabo a 85–90 cm, mesa a 75 cm, silla a 45 cm). Si una medida no está en la biblia, se toma la de un hotel 5–7 estrellas real y se anota.
2. **Cada vista es un momento fotografiable.** Miradores, playas, terrazas y restaurantes se componen como encuadres: luz adecuada, palmeras, fuego, agua, cielo.
3. **El sonido acompaña cada escena.** Pájaros en jardines, olas y viento en playa, murmullo suave en restaurantes, música ambiente que no invade.
4. **Nada genérico, nada fuera de lugar.** La fauna no se atraviesa en zonas de tránsito; los platillos varían un poco para no verse clonados; los muebles invitan a sentarse.
5. **Como hotel real: no hay sobreventa.** La capacidad física manda sobre las reservas.

## La isla

| Dato | Valor | Fuente |
|---|---|---|
| Tipo | Volcánica, con gran cráter central, laderas verdes, acantilados, playas curvas de arena blanca y bahías tranquilas | [Prompt maestro §2](biblia/01-prompt-maestro-v2.md) |
| Tamaño | 3–4 km de diámetro | Prompt maestro §2 |
| Habitaciones | 800 · **hasta 4 personas** (la biblia decía 3) · **1 USD/noche** de lanzamiento | Regla del 26-oct-2026 · [07](07-islas-y-capacidad.md) |
| Villas ultra lujo | 80 · **hasta 10–12 personas** (la biblia decía 4–6) · **100 USD/noche** de lanzamiento | Regla del 26-oct-2026 |
| Villa Horizonte | **1 por isla** · 25 suites · hasta 60 personas · 10 veces el precio de una villa (**1,000 USD/noche** de lanzamiento) | [10](10-villa-horizonte.md) |
| Huéspedes por isla | **4,220 máximo**, 2,685 en promedio (la biblia decía ≈ 2,800) | [07](07-islas-y-capacidad.md) |
| Staff | **1,820 por isla** (2 por llave + 60 de Horizonte; la biblia decía 1,200 NPC) | [07](07-islas-y-capacidad.md) |
| Estancia | **Cada noche va de 12:00 a 12:00**, como un hotel | Decisión del 26-oct-2026 |
| Islas | Una por región horaria e idioma; La Encantada primero | [07](07-islas-y-capacidad.md) |
| Personajes | Gente bonita, sensual sin desnudos, al azar y ajustable | [06](06-personajes.md) |

### Zonas

| Zona | Qué hay | Documento que la detalla |
|---|---|---|
| Área hotelera | Lobby, 800 habitaciones, albercas, restaurantes temáticos | [Prompt maestro](biblia/01-prompt-maestro-v2.md) · [Suite Retorno 100](biblia/03-suite-retorno-100.md) |
| Zona de villas | 80 villas de 2–4 recámaras + villas de grupo | [Villa Horizonte 50](biblia/04-villa-horizonte-50.md) |
| Península del restaurante | Restaurante principal, orientado oeste-suroeste, con muelle privado | [Restaurante principal](biblia/02-restaurante-principal.md) |
| Península privada | Villa Horizonte 50, vista de 270° al mar | Villa Horizonte 50 |
| Marina | Yates, lanchas, salidas de navegación y pesca | [Experiencias](../catalogo/experiencias.md) |
| Pista aérea | Sobre el mar (ver render 01); avionetas e hidroaviones | [Render 01](../referencias/renders/01-vista-aerea-pista-y-marina.png) |
| Spa y bienestar | Jardines aromáticos, 120 masajes | [Masajes](../catalogo/masajes.md) |
| Áreas naturales | Selva, cráter, senderos, miradores, arrecifes | [Flora](../catalogo/flora.md) · [Fauna](../catalogo/fauna.md) |
| Tiendas | Orillas del Mar · Joya del Océano · Gabinete de La Encantada | [Tiendas](../catalogo/tiendas.md) |
| Staff village | Oculta: el staff vive y circula sin cruzarse con huéspedes | Prompt maestro §2 |

### Tiempo y luz

| Momento | Duración virtual | Cómo se ve y se oye |
|---|---|---|
| Amanecer | 1.5–2 h | Azul profundo → morado → rosa → naranja → dorado; nubes finas con bordes iluminados; sube el canto de las aves |
| Día | 14–15 h | Cielo azul claro, nubes esponjosas, mar turquesa transparente, gran visibilidad para nadar y bucear |
| Atardecer | 1.5–2 h | Naranja intenso, bandas rosas y violetas; reflejo dorado; caminos y albercas se encienden en 2700–3000 K |
| Noche | 8 h | Vía Láctea, luna con fases, luz respetuosa del cielo; grillos, oleaje y música lejana |

## Lo que ya está definido (y dónde)

| Pieza | Cantidad | Dónde |
|---|---:|---|
| Documentos maestros | 6 | [docs/biblia/](biblia/README.md) |
| Especies de flora | 50 | [catalogo/flora.md](../catalogo/flora.md) |
| Especies de fauna | 70 | [catalogo/fauna.md](../catalogo/fauna.md) |
| Experiencias | 100 | [catalogo/experiencias.md](../catalogo/experiencias.md) |
| Platillos | 100 | [catalogo/platillos.md](../catalogo/platillos.md) |
| Masajes | 120 | [catalogo/masajes.md](../catalogo/masajes.md) |
| Piezas de tienda | 200 | [catalogo/tiendas.md](../catalogo/tiendas.md) |
| Concept art | 6 | [referencias/renders/](../referencias/renders/) |
| Modelo financiero | 60 meses | [03-modelo-financiero.md](03-modelo-financiero.md) |

## La economía del mundo: también se puede trabajar en la isla

El [restaurante principal §9](biblia/02-restaurante-principal.md) abre una idea que va más allá del restaurante: **los usuarios pueden ser staff y ganar dinero**.

- **Cocineros virtuales / usuarios-creadores:** reciben tareas según demanda y ganan una parte del valor del platillo preparado correctamente y a tiempo.
- **Meseros virtuales / usuarios-host:** gestionan mesas y atención; ganan comisión por ticket promedio + propinas voluntarias.
- **Host/hostess:** reservas, asignación de mesas, lista de espera.
- Cada platillo tiene precio de venta, costo base virtual y porcentaje de comisión para quien cocina y quien sirve; hay métricas (tiempo de servicio, rating, propinas) y bonos semanales.

Esto convive con los 1,200 NPC: el NPC cubre el puesto cuando no hay persona. Se modela después del MVP 0.1.

## Decisiones abiertas

Cosas que los documentos dicen de forma distinta o que todavía no se deciden. Ninguna frena la Fase A; conviene cerrarlas antes de la Fase B.

| # | Tema | Lo que dicen las fuentes | Por decidir |
|---|---|---|---|
| 1 | **Duración del ciclo** | El prompt maestro dice «ciclo de 24 horas: 18 de día y 8 de noche», que suman **26 h**. | **Decidido (26-oct-2026):** como un hotel real. La estancia va de 12:00 a 12:00 y el sol sigue la hora real de la región (La Encantada, hora del centro de México): amanecer 6:00, atardecer 20:00–21:30 y noche 22:00–6:00 ([07 §2](07-islas-y-capacidad.md#2-una-isla-por-región-no-por-país)) |
| 2 | **Capacidad vs. usuarios** | Una isla admite 4,220 huéspedes; el Excel llega a 100,000 usuarios diarios. | **Resuelto:** varias islas por región, se abre otra con 85 % durante 4 semanas y lista de espera ([07](07-islas-y-capacidad.md)) |
| 3 | **Villas** | 80 villas de hasta 12 personas; la Villa Horizonte 50 es para 50. | **Decidido (26-oct-2026):** Villa Horizonte es la villa más especial de la isla, aparte de las 80: **una por isla**, 25 suites (5 veces una villa), hasta 60 personas y 10 veces el precio. La paga un anfitrión que invita a sus amigos ([10](10-villa-horizonte.md)) |
| 8 | **Edad** | La estética es sensual y hay dinero y encuentros entre personas. | **Decidido (26-oct-2026, Ricardo):** la plataforma es sólo para mayores de 18 años ([06 §5](06-personajes.md#5-sexy-sin-vulgaridad-las-reglas)) |
| 9 | **Opción neutral en avatares** | El pedido es una mujer y un hombre nuevos por sesión. | ¿Agregar una tercera opción más adelante? ([06 §9](06-personajes.md#9-lo-que-todavía-hay-que-decidir)) |
| 4 | **Precios** | Habitación 100 USD/noche y villa 10,000 USD/noche (prompt) vs. 35 USD por usuario al día por habitación (modelo). | **Decidido (26-oct-2026): empezar abajo y subir.** Lanzamiento: Horizonte 1,000 USD, villa 100 y habitación 1 por noche; luego experimentos de precio (primera noche gratis, subidas al doble) ([09 §3](09-revision-del-razonamiento.md#3-cómo-averiguar-el-precio-real-barato-y-antes-de-construir-de-más)). Antes: una sola lista de precios y moneda virtual. |
| 5 | **Catálogo de masajes** | El PDF dice «100 tipos» y contiene **120**. | Se quedan los 120 (ya están en datos). |
| 6 | **Nombre** | «Isla La Encantada», «IslaEncantada.com», «Isla Virtual de Lujo». | **Resuelto:** la marca es **ISLA** y cada isla lleva su nombre abajo; la primera es **La Encantada** |
| 7 | **Plataforma inicial** | Plan MVP: Unreal Engine 5; alternativa barata: Fortnite UEFN o Roblox. | Se va con Unreal (ya se está descargando). |

<!-- RLR · Ricardo López Reyero · rev 181218 -->
