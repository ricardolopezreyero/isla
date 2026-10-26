# 09 · Revisión del razonamiento y de los números

[← Volver al README](../README.md)

> Pedido (26-oct-2026): «ayúdame a encontrar fallas en el razonamiento… revisa ya los números».
> Los números de esta página salen de `node herramientas/proyecciones.mjs`, con el mismo modelo que usa la página privada [/proyecciones](https://isla.capitaltorreon.com/proyecciones).

## 1. Los cuatro escenarios lado a lado

| Escenario | Ingresos 60 meses | Utilidad 60 meses | Capital necesario | Primer mes con utilidad | Islas al mes 60 | Personas reales en el pico, por isla |
|---|---:|---:|---:|---:|---:|---:|
| Excel v3 (tal cual) | $8,142 M | $7,524 M | $0 | 1 | — | — |
| v4 · **Lanzamiento** (habitación 1 · villa 100 · Horizonte 1,000 USD) | $55.2 M | $18.6 M | $914 mil | 22 | 12 | 499 |
| v4 · Primera subida (todo al doble) | $112.4 M | $63.8 M | $368 mil | 13 | 12 | 499 |
| v4 · Meta (5 veces el lanzamiento) | $275.8 M | $192.9 M | $225 mil | 7 | 12 | 499 |

*26-oct-2026: Ricardo bajó los precios para empezar abajo y subir con experimentos. Los escenarios anteriores (Biblia 100 / 10,000, Prudente 15 / 450, Conservador 6 / 150) se retiraron.*

*Desde el 26-oct-2026 incluye la Villa Horizonte: una por isla, 10 veces el precio de una villa, 30 % de noches vendidas.*

**Lectura:** con precios de lanzamiento la caja baja hasta ~914 mil USD y la primera utilidad llega en el mes 22; si cada subida funciona, el capital necesario baja a 225 mil. **El precio que la gente de verdad paga es el dato que más vale averiguar**, y hoy nadie lo sabe. Antes de construir de más, conviene medirlo (sección 3).

## 2. Las fallas, de la más grave a la menos

| # | Falla | Por qué importa | Qué se hizo / qué se propone |
|---|---|---|---|
| 1 | **Vendida no es llena.** Con 2 h al día dentro, en la hora pico hay ~500 personas reales por isla aunque esté vendida al 100 % | El objetivo «siempre llena» no se cumple sólo con reservas | NPC huéspedes de la misma belleza que ceden su lugar; eventos a hora fija; juntar a la gente donde se ve ([07](07-islas-y-capacidad.md)) |
| 2 | **El ingreso por persona es de techo.** El Excel supone 55 USD por usuario activo al día; Roblox anda cerca de 0.14 USD | Es 390 veces más. Todo el negocio cuelga de este número | Escenarios v4 con precio por noche y por llave; validar con preventa antes de la Fase C |
| 3 | **Calidad AAA con 2 freelancers.** El equipo del modelo cuesta 25–31 mil USD al mes | Sirve para el MVP 0.1, no para 640 piezas de catálogo, MetaHumans, multijugador y operación de varias islas | v4 suma equipo por isla (35 mil USD/mes) y construcción; falta un plan de equipo para pasar de MVP a producto (15–40 personas) |
| 4 | **Un servidor de Unreal no aguanta una isla.** ~100 jugadores por servidor dedicado | 500 personas en el pico ya son 5 servidores por isla | Partir cada isla por zonas; probarlo en la Fase D con 2 zonas y 20 jugadores ([07 §5](07-islas-y-capacidad.md#5-servidores-lo-técnico-que-cambia-todo)) |
| 5 | **Isla por país.** Países muy desparejos y gente del mismo idioma separada | Islas medio vacías en países chicos | Una isla por **región horaria e idioma**; el sol sigue la hora real ([07 §2](07-islas-y-capacidad.md#2-una-isla-por-región-no-por-país)) |
| 6 | **El ciclo de luz suma 26 h** (18 de día + 8 de noche) | No cabe en un día | **Decidido:** como un hotel real; estancia de 12:00 a 12:00 y el sol en la hora real de la región |
| 7 | **Abrir islas diluye.** Abrir otra en cuanto se llena reparte a la gente | Dos islas medio vacías se ven peor que una llena | Abrir con habitaciones al 85 % durante 4 semanas **y** lista de espera |
| 8 | **Servicios chicos para una isla llena.** Un restaurante de 120–150 lugares para 2,685 huéspedes | Filas y frustración | 6–8 restaurantes, 30–40 cabinas de spa, varias playas y albercas ([07 §4](07-islas-y-capacidad.md#4-lo-que-una-isla-tiene-que-poder-atender)) |
| 9 | **Staff corto.** 1,200 NPC para 880 llaves | La biblia pide servicio de 7 estrellas | 2 por llave + 60 de Horizonte = 1,820 por isla |
| 10 | **Costos que el Excel no traía:** construcción antes de lanzar, comisión de pagos (~4 %), 30 % si se vende dentro de App Store o Google Play, 5 % de regalía de Unreal arriba de 1 millón de ingresos | Bajan el margen y cambian el capital necesario | Todos están en v4; la comisión de tiendas es un control en la página |
| 11 | **El marketing del Excel sigue creciendo cuando los usuarios ya toparon** | Gasto sin efecto | v4 lo liga a los ingresos (12 %) más una base |
| 12 | **Ocupación del 15 % el día uno** (120 habitaciones por noche) | Supone audiencia antes de abrir | Lista de espera y preventa desde la Fase B; si no llega, el escenario Conservador muestra el golpe (capital de ~1 millón) |
| 13 | **Sexy y mayores de 18.** La estética pedida, la economía con dinero y los encuentros entre personas | Clasificación de edad, tiendas de apps y moderación | **Decidido (26-oct-2026): plataforma sólo para mayores de 18 años**; avatares siempre adultos, sin desnudos, invitaciones y burbuja personal ([06 §5](06-personajes.md#5-sexy-sin-vulgaridad-las-reglas)) |
| 14 | **Registrar todo** de cada usuario | Datos personales: ley mexicana (LFPDPPP) y, con usuarios europeos, GDPR | Bitácora privada, exportable y borrable; aviso de privacidad antes de abrir ([08 §4](08-bitacora.md#4-privacidad-para-que-dé-gusto-no-miedo)) |
| 15 | **Repositorio público.** El modelo y los supuestos se ven en GitHub | La página de proyecciones es privada, pero los valores por omisión están en el código | Decisión de Ricardo: el repo se queda público. Los escenarios que guardes en la página viven en la base privada, no en el repo |

## 3. Cómo averiguar el precio real, barato y antes de construir de más

**Regla de Ricardo (26-oct-2026): empezar abajo y subir.** Es más fácil subir un precio que bajarlo. Los experimentos, en orden:

1. **Primera noche gratis** para quien llega por primera vez; las siguientes, a precio de lanzamiento.
2. **Subidas pequeñas** (al doble) cuando una isla pasa del 85 % de ocupación por 4 semanas.
3. Cada experimento se guarda como escenario en /proyecciones con lo que de verdad pasó.

Además:

1. **Lista de espera** en isla.capitaltorreon.com con una pregunta: «¿Cuánto pagarías por una noche en una villa para tu grupo?».
2. **Preventa simbólica:** 50–100 «llaves fundadoras» (por ejemplo, 7 noches de habitación) con precio real, cobradas con Stripe y reembolsables.
3. Con lo que se venda, se ajustan `precio_habitacion`, `precio_villa` y `ocupacion_inicial` en /proyecciones y se guarda como escenario «Medido».

## 4. Lo que sí está bien pensado

- **MVP chico y bien hecho** (una habitación, una villa, un restaurante) antes que la isla entera.
- **Exclusividad por escasez:** capacidad física sin sobreventa más lista de espera es una idea fuerte.
- **La biblia al centímetro** da a los freelancers medidas para no inventar.
- **Varias islas con su propio nombre** es una forma de crecer que no rompe la sensación de exclusividad.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
