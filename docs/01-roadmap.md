# 01 · Roadmap: del documento a la isla jugable

[← Volver al README](../README.md)

Basado en el [Plan de acción MVP](biblia/05-plan-de-accion-mvp.md). La regla del plan: **no construir toda la isla desde el inicio**. Pocas zonas, muy bien hechas, con Unreal Engine 5 + asset packs + 1–2 freelancers; después se crece por iteraciones.

## Dónde estamos

| Etapa | Duración estimada | Estado |
|---|---|---|
| Base · proyecto y dominio | — | ✅ Listo (25-oct-2026) |
| Fase A · Plan rápido | ≈ 1 semana | 🟡 En curso |
| Fase B · Greybox en Unreal | ≈ 2–3 semanas | ⚪ Sigue |
| Fase C · Detalle visual con asset packs | ≈ 4–6 semanas | ⚪ Sigue |
| Fase D · Interactividad mínima | ≈ 2–4 semanas | ⚪ Sigue |
| **MVP 0.1 jugable** | **≈ 9–14 semanas** desde la Fase A | |

Cuando cambie el estado, actualizar esta tabla **y** el arreglo `FASES` de [`web/index.html`](../web/index.html) (la sección «Cómo vamos» de la página), y desplegar.

## Qué entra en el MVP 0.1 (y qué no)

| Entra | Se deja para después |
|---|---|
| 1 zona de hotel con 1–2 tipos de habitación | El resto de las 800 habitaciones |
| 2–3 villas representativas | Las demás villas y Villa Horizonte 50 completa |
| 1 playa principal + 1 alberca principal | Otras playas, marina operando, pista aérea |
| 1 restaurante principal con platillos estrella | Los demás restaurantes temáticos |
| Ciclo día/noche sencillo | Cielo, clima y fases de luna completos |
| Pocos NPC (staff y huéspedes con interacción mínima) | 1,200 NPC con rutinas, fauna, actividades, transporte interno |
| | Economía interna, gestión avanzada, usuarios-staff |

---

## Base · Proyecto y dominio ✅

- [x] Repo con biblia de diseño transcrita (6 documentos)
- [x] 640 piezas de catálogo en Markdown y JSON
- [x] Modelo financiero v3 replicado en código (`herramientas/modelo.py`)
- [x] Concept art ordenado en `referencias/renders/`
- [x] isla.capitaltorreon.com publicada «en construcción» (Worker `isla`)
- [ ] Unreal Engine 5 instalado (en descarga) → seguir [04-unreal.md](04-unreal.md)

## Fase A · Plan rápido (≈ 1 semana) 🟡

Tomar el documento maestro y aterrizarlo en un mapa y en una lista cerrada.

- [ ] Mapa esquemático de la isla con zonas marcadas: hotel, villas, marina, pista, restaurante, spa, áreas naturales, staff village → guardar en `referencias/mapa/`
- [ ] Ubicar en el mapa la península oeste-suroeste del restaurante y la península de 270° de Villa Horizonte
- [ ] Lista exacta de features del MVP 0.1 (tabla de arriba, cerrada y firmada)
- [ ] 3–5 imágenes de referencia con IA: vista aérea, habitación estándar, villa con alberca privada, restaurante (ya hay 6 en `referencias/renders/`; faltan restaurante y baño)
- [ ] Cerrar las [decisiones abiertas](00-vision.md#decisiones-abiertas) 1 y 2 (ciclo y capacidad)
- [ ] Elegir y comprar asset packs: *Tropical Island / Resort / Marina / Luxury Villas* y *Modern Hotel Interior / Luxury Room / Spa*
- [ ] Contactar a los freelancers con el mensaje de [02-equipo.md](02-equipo.md)

**Entregables:** mapa de zonas · lista del MVP 0.1 · carpeta de concept art.

## Fase B · Greybox en Unreal (≈ 2–3 semanas)

El environment artist arma la isla en bloques, sin detalle.

- [ ] Forma de la isla: topografía sencilla, cráter, rocas, playas
- [ ] Caminos y edificios como bloques grises
- [ ] Escala real: alturas, distancias caminables, tamaño de habitación (Suite Retorno = 100 m² + terraza) y villas
- [ ] Recorrido a pie de punta a punta cronometrado (¿cuánto se tarda una persona en cruzar 3–4 km?)

**Entregables:** versión jugable muy básica donde ya se camina · layout aprobado (forma, distancias, zonas).

## Fase C · Detalle visual (≈ 4–6 semanas)

- [ ] Sustituir bloques por modelos de hotel, villas, marina y restaurante (asset packs)
- [ ] **1 habitación completa**: cama (colchón 32–38 cm + topper 5–8 cm, altura 55–60 cm), baño con regadera de lluvia 25–35 cm en espacio de 100×140 cm, WC tipo washlet en recinto propio, doble lavabo con 70–80 cm entre ellos, luz 2700 K con dimmer
- [ ] **1 villa de lujo** con alberca privada y vista al mar
- [ ] **Restaurante principal (hero area):** mesas, barra semicircular, cocina visible opcional, platillos del menú en 3D sencillo o en UI con imágenes
- [ ] Iluminación: día soleado, atardecer y noche; luces cálidas en zonas de lujo
- [ ] Flora del MVP: palmeras, almendros, buganvilias, hibiscos, plumerias (de [flora.json](../data/flora.json))

**Entregables:** isla atractiva en las zonas del MVP · habitación y villa funcionales y decoradas · restaurante presentable.

## Fase D · Interactividad mínima (≈ 2–4 semanas)

- [ ] Movimiento libre del jugador y cámara
- [ ] Entrar y salir de habitación y villa
- [ ] Abrir puertas, prender/apagar luces, sentarse, acostarse
- [ ] Entrar al restaurante, ver el menú interactivo (leído de [platillos.json](../data/platillos.json)) y sentarse a la mesa
- [ ] NPC: recepcionista en el lobby, mesero en el restaurante, 2–4 huéspedes
- [ ] UI simple: menú del restaurante y cambiar la hora del día

**Entregables:** demo jugable para recorrer la isla, explorar habitación y villa, visitar el restaurante y ver la vida básica del resort.

---

## Después del MVP 0.1 (versiones 0.2 en adelante)

En orden sugerido, cada una se puede publicar y mostrar por separado:

1. **Mar:** arrecifes, buceo y snorkel (efectos de luz, color por profundidad, sonido amortiguado), tortugas, mantarrayas, delfines → [fauna marina](../catalogo/fauna.md)
2. **Vida:** fauna terrestre y aves en zonas de observación; más NPC con turnos y rutas
3. **Gastronomía completa:** más restaurantes y bares, cristalería por bebida, menú de vinos
4. **Spa:** los 120 masajes como servicio reservable
5. **Tiendas:** las 3 tiendas con inventario de 200 piezas
6. **Experiencias:** sistema de reservas para las 100 actividades
7. **Multijugador:** llegar con la «familia», compartir habitación o villa, reservar juntos
8. **Economía:** reservas sin sobreventa, moneda virtual, usuarios-staff con comisiones y propinas
9. **Publicación:** jugar desde el navegador en isla.capitaltorreon.com (Pixel Streaming) o descarga

## Plan B más barato

Si el realismo no fuera prioridad: probar el flujo de experiencia en **Fortnite UEFN** o **Roblox** con assets prehechos y dejar la versión hiperrealista para Unreal. Hoy no se toma: ya se va con Unreal Engine 5.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
