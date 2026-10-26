# 11 · Greybox de la isla (Fase B)

[← Volver al README](../README.md)

> **Actualización (26-oct-2026, noche):** el greybox de bloques ya se reemplazó por la **isla v2** con objetos reales hechos en casa: ver [12 · La fábrica en casa](12-fabrica-en-casa.md). Este documento queda como registro de la primera versión.

> **26-oct-2026.** La isla completa en bloques y a escala real dentro de Unreal: nivel **`/Game/Isla/Mapas/L_Isla`** del proyecto `unreal/IslaLaEncantada`. La construyó Claude por el servidor MCP del editor ([04 §9](04-unreal.md#9-claude-dentro-del-editor-unreal-mcp)).

## Cómo se hace y se rehace

| Paso | Archivo | Qué hace |
|---|---|---|
| 1. El plano | [`herramientas/greybox_isla.py`](../herramientas/greybox_isla.py) | Calcula cada bloque en metros (posición, tamaño, giro, color y zona) y lo escribe en [`data/greybox_isla.json`](../data/greybox_isla.json) |
| 2. La obra | [`herramientas/greybox_unreal.py`](../herramientas/greybox_unreal.py) | Con Unreal abierto, borra la carpeta «Isla» del esquematizador y vuelve a levantar todo; también coloca al jugador y el sol |

```bash
cd ~/Code/isla && python3 herramientas/greybox_isla.py && python3 herramientas/greybox_unreal.py
```

Para rehacer sólo una zona (por ejemplo, después de mover las villas):

```bash
cd ~/Code/isla && python3 herramientas/greybox_isla.py && python3 herramientas/greybox_unreal.py Villas
```

Cambiar la isla = cambiar el plano y volver a correr. Nada se acomoda a mano, así el greybox siempre es igual al documento.

## Convenciones

- **1 unidad de Unreal = 1 cm**; el plano trabaja en metros y convierte al final.
- **Norte = +X, este = +Y.** Los ángulos se miden desde el norte hacia el este.
- La isla está a **6 m sobre el mar**. El mar es un plano de 16 × 16 km.
- Cada zona vive en su carpeta del esquematizador: `Isla/Terreno`, `Isla/Hotel`, `Isla/Villas`, `Isla/Horizonte`, `Isla/Restaurante`, `Isla/Marina`, `Isla/Pista`, `Isla/Spa`, `Isla/Staff` e `Isla/Caminos`.
- Colores del greybox en `/Game/Isla/Greybox/Materiales` (18 materiales: mar, arena, pasto, volcán, cráter, roca, hotel, villa, Horizonte, alberca, camino, muelle, pista, restaurante, spa, staff, tiendas y lobby).

## Lo que hay (354 piezas)

| Zona | Dónde | Qué | Medidas |
|---|---|---|---|
| Terreno | Centro | Isla de **3.5 km** de diámetro, playa perimetral de 100 m, mar de 16 km | Tierra a 6 m sobre el mar |
| Volcán | Centro, un poco al noreste | Cono de **1.3 km de base y 420 m de alto**, con la cumbre oscura del cráter | |
| Acantilados | Costa norte y noreste | 28 rocas de 18–33 m de alto | Deja libre el cuello de Horizonte |
| Hotel | Playa sur | **8 edificios de 100 habitaciones** (5 pisos × 20), lobby, 3 tiendas, alberca principal de 50 m y playa principal | Edificio de 45 × 20 × 17.5 m |
| Villas | Laderas este y oeste | **80 villas** (40 por lado, en dos filas) con su alberca hacia el mar | Villa de 26 × 18 × 7 m |
| Villa Horizonte | Península norte | Cuello de 260 m, península con playa privada, villa en **3 niveles escalonados**, alberca infinita de 40 m, jacuzzi para 20 y muelle privado | Vista de 270° (docs/10) |
| Restaurante principal | Península oeste-suroeste | Salón de doble altura (9 m), 3 terrazas escalonadas al mar y muelle privado | Todas las mesas al atardecer |
| Marina | Bahía sureste | Rompeolas en arco, 4 muelles y 8 yates | |
| Pista aérea | Sobre el mar, al este | **2 km × 120 m**, calzada desde la isla y hangar | |
| Spa | Suroeste, junto al hotel | Spa principal y 8 cabinas | |
| Staff | Detrás del volcán, noreste | 6 edificios fuera de la vista de los huéspedes | |
| Caminos | Anillo a 1.6 km del centro | 72 tramos + 7 ramales a lobby, spa, restaurante, marina, pista, staff y Horizonte | 8 m de ancho |

El jugador aparece junto a la alberca principal, mirando al norte. El sol está bajo, al oeste-suroeste, para ver la isla al atardecer.

## Qué sigue en la Fase B

- [ ] Recorrerla con el personaje en primera persona y medir: cuánto se tarda en cruzar la isla y llegar a Horizonte, al restaurante y a la marina
- [ ] Revisar con Ricardo la distribución (qué se mueve, qué falta)
- [ ] Cambiar el cilindro de tierra por un **Landscape** con laderas reales hacia el volcán y bahías
- [ ] Agua con el plugin **Water** (olas y orilla) en lugar del plano
- [ ] Prueba de multitud: 50 NPC caminando en la playa principal, midiendo cuadros por segundo

<!-- RLR · Ricardo López Reyero · rev 181218 -->
