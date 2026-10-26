# PLAN DE ACCIÓN PARA CREAR LA ISLA 3D (VERSIÓN RÁPIDA Y DE BAJO COSTO)

> Transcripción fiel de [`fuentes/pdf/Plan_de_Accion_Isla_3D_MVP.pdf`](../../fuentes/pdf/Plan_de_Accion_Isla_3D_MVP.pdf). No editar el sentido: los cambios de diseño van en un documento nuevo con versión.

[← Biblia de diseño](README.md)

## 1. Estrategia general

- **Objetivo:** Tener una demo 3D funcional y visualmente atractiva de la isla (MVP 0.1), sin modelar todo el proyecto completo.
- **Clave:** Usar Unreal Engine + asset packs, enfocarse en pocas áreas muy bien hechas y apoyarse en 1–2 freelancers especializados.

## 2. Definir el MVP 0.1 (qué sí va en la primera versión)

**Incluir:**

- 1 zona de hotel con 1–2 tipos de habitación.
- 2–3 villas representativas.
- 1 playa principal + 1 alberca principal.
- 1 restaurante principal (con algunos platillos “estrella” del menú maestro).
- Ciclo día/noche sencillo.
- Pocos NPC (staff y huéspedes caminando o interactuando mínimamente).

**Dejar para versiones futuras:**

- Todas las demás zonas de la isla (habitaciones extra, villas adicionales, áreas especiales).
- Más NPC, fauna, actividades, transporte interno, etc.
- Simulaciones complejas (economía interna, gestión avanzada, etc.).

## 3. Herramientas principales

- Motor de juego recomendado: Unreal Engine 5 (look realista y de lujo).
- Recursos (asset packs) a comprar/usar:
  - Packs de “Tropical Island / Resort / Marina / Luxury Villas”.
  - Packs de “Modern Hotel Interior / Luxury Room / Spa”.
- IA como apoyo:
  - Generar imágenes de referencia (concept art) para:
    - Vista aérea de la isla.
    - Habitación estándar.
    - Villa de lujo.
    - Restaurante de alta cocina.
  - Opcional: usar IA 3D solo para objetos o piezas icónicas (esculturas, barras especiales, etc.).

## 4. Equipo mínimo recomendado

- Director creativo / Product Owner: tú, usando tus documentos como biblia de diseño.
- 1 Environment Artist (freelance, con experiencia en Unreal):
  - Construye la isla, acomoda assets, crea la vegetación, playas, caminos y edificios.
- 1 Technical Artist o Game Developer (freelance):
  - Programa movimiento del jugador.
  - Interacciones básicas (abrir puertas, prender/apagar luces, sentarse, etc.).
  - Menús y detalles de UI simples.

## 5. Fases del proyecto

### Fase A – Plan rápido (≈ 1 semana)

- Tomar el documento maestro de la isla y marcar en un mapa:
  - Zona hotel, villas, marina, pista, restaurante, spa, etc.
- Definir con claridad qué entra en el MVP 0.1 y qué se pospone.
- Crear 3–5 imágenes de referencia con IA:
  - Vista aérea general.
  - Habitación estándar de hotel.
  - Villa de lujo con alberca privada.
  - Restaurante / área de fine dining.

**Entregables de esta fase:**

- Mapa esquemático de la isla con zonas marcadas.
- Lista exacta de features del MVP 0.1.
- Carpeta con imágenes de referencia (concept art).

### Fase B – Greybox en Unreal (≈ 2–3 semanas)

- El environment artist:
  - Crea la forma básica de la isla (topografía sencilla, rocas, playas).
  - Traza caminos y coloca edificios como “bloques” sin detalle (greybox).
  - Ajusta escala: alturas realistas, distancias caminables, tamaño de habitaciones y villas.

**Entregables de esta fase:**

- Versión jugable muy básica de la isla donde ya se pueda caminar.
- Layout general aprobado (forma, distancias, ubicación de zonas principales).

### Fase C – Detalle visual usando asset packs (≈ 4–6 semanas)

- Sustituir los bloques por:
  - Modelos de hotel, villas, marina y restaurante de los asset packs.
- Detallar interiores clave:
  - 1 tipo de habitación completa (cama, baño sensual, iluminación cuidada).
  - 1 villa de lujo con alberca privada y vista al mar.
- Crear el restaurante principal (“hero area”):
  - Mesas, barra, cocina visible opcional.
  - Mostrar algunos platillos del menú mediante:
    - Modelos 3D simples o
    - UI con imágenes renderizadas.
- Configurar iluminación:
  - Día soleado, atardecer y noche.
  - Luces cálidas para áreas de lujo (habitaciones, villas, restaurante).

**Entregables de esta fase:**

- Isla visualmente atractiva en las zonas del MVP.
- 1 habitación completamente funcional y decorada.
- 1 villa de lujo completamente funcional y decorada.
- Restaurante principal montado y presentable.

### Fase D – Interactividad mínima (≈ 2–4 semanas)

- Implementar mecánicas básicas:
  - Movimiento libre del jugador por la isla.
  - Entrar y salir de la habitación y la villa.
  - Acciones simples: abrir puertas, prender/apagar luces, sentarse o acostarse.
  - Entrar al restaurante, ver el menú interactivo y sentarse a la mesa.
- Añadir algunos NPC:
  - Recepcionista en el lobby.
  - Mesero en el restaurante.
  - 2–4 huéspedes caminando o interactuando con el entorno.

**Entregables de esta fase:**

- Demo jugable donde se pueda:
  - Recorrer la isla en sus zonas principales.
  - Explorar una habitación y una villa de lujo.
  - Visitar el restaurante y ver el menú.
  - Percibir la vida básica del resort mediante NPC.

## 6. Opciones aún más rápidas/baratas (si el realismo no es prioridad)

- Usar Fortnite UEFN o Roblox como plataforma inicial:
  - Construir la isla con herramientas tipo “Lego” y assets preexistentes.
  - Enfocarse en probar el flujo de experiencia y las ideas de diseño.
  - Dejar la versión hiperrealista para una segunda etapa en Unreal.

## 7. Resumen ejecutivo

- No intentes construir toda la isla desde el inicio.
- Usa Unreal Engine + asset packs para acelerar y abaratar el desarrollo.
- Define un MVP muy acotado con pocas zonas pero de alta calidad visual.
- Apóyate en 1–2 freelancers clave (environment y technical artist).
- Añade poco a poco más zonas, NPC y sistemas en iteraciones posteriores.

## SHORT ENGLISH SUMMARY

Goal: Build a beautiful, interactive 3D island as fast and cheap as possible by:

- Focusing on a very small MVP: one hotel zone, a few villas, one beach, one pool and one main restaurant.
- Using Unreal Engine 5 with marketplace asset packs instead of full custom modeling.
- Hiring 1–2 freelancers (environment + technical artist) to assemble everything.
- Adding interactivity step by step (movement, basic interactions, simple NPCs).
- Expanding the island in later versions once the core experience is working.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
