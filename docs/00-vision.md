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
| Habitaciones estándar | 800 · máx. 3 huéspedes · king + sofá cama o doble queen · 100 USD/noche | Prompt maestro §3 |
| Villas ultra lujo | 80 · 2–4 recámaras · 4–6 huéspedes (promedio 5) · 10,000 USD/noche | Prompt maestro §3 |
| Huéspedes simultáneos | ≈ 2,800 (2,400 + 400) | Prompt maestro §3 |
| Staff | 1,200 NPC con rutinas, turnos, descansos y rutas internas | Prompt maestro §3 |

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
| 1 | **Duración del ciclo** | El prompt maestro dice «ciclo de 24 horas: 18 de día y 8 de noche», que suman **26 h**. Amanecer + día + atardecer = 17–19 h. | ¿Día de 16 h + noche de 8 h (24 h), o día de 18 h + noche de 6 h? ¿El ciclo virtual dura 24 h reales o se acelera? |
| 2 | **Capacidad vs. usuarios** | La isla admite ≈ 2,800 huéspedes simultáneos sin sobreventa; el modelo financiero llega a **100,000 usuarios activos diarios**. | ¿Varias copias de la isla (instancias), turnos de estancia, o visitantes sin habitación? |
| 3 | **Villas** | El prompt habla de 80 villas de 2–4 recámaras (≈ 5 huéspedes); la Villa Horizonte 50 es para 50 personas. | ¿Horizonte 50 es una villa especial aparte de las 80, y cuántas hay? |
| 4 | **Precios** | Habitación 100 USD/noche y villa 10,000 USD/noche (prompt) vs. 35 USD por usuario al día por habitación (modelo). | Una sola lista de precios y moneda virtual. |
| 5 | **Catálogo de masajes** | El PDF dice «100 tipos» y contiene **120**. | Se quedan los 120 (ya están en datos). |
| 6 | **Nombre** | «Isla La Encantada», «IslaEncantada.com», «Isla Virtual de Lujo». | Nombre público definitivo y dominio propio, si se quiere además de isla.capitaltorreon.com. |
| 7 | **Plataforma inicial** | Plan MVP: Unreal Engine 5; alternativa barata: Fortnite UEFN o Roblox. | Se va con Unreal (ya se está descargando). |

<!-- RLR · Ricardo López Reyero · rev 181218 -->
