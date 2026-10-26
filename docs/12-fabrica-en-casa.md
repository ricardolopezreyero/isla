# 12 · La fábrica en casa: todos los objetos hechos aquí

[← Volver al README](../README.md)

> **Regla de Ricardo (26-oct-2026):** «No vamos a comprar absolutamente nada. Todo va a ser hecho aquí en casa». Van a hacer falta miles de objetos, así que todo sale de código que se puede repetir, variar y mejorar.
>
> **Costo hasta hoy: $0.** Blender 5.2 (gratis, código abierto) + Unreal Engine 5.8 (gratis hasta el primer millón de dólares de ingresos) + los scripts de este repo.

## Cómo funciona

```
herramientas/blender/*.py  ──(Blender, sin abrir la ventana)──▶  unreal/fuentes/objetos/*.fbx
        │                                                                 │
        │                                         herramientas/importar_unreal.py
        ▼                                                                 ▼
herramientas/plano_isla.py ──▶ data/plano_isla.json ──▶ herramientas/construir_isla.py ──▶ Unreal (L_Isla)
```

| Paso | Comando | Qué hace | Tiempo |
|---|---|---|---|
| 1. Plano | `python3 herramientas/plano_isla.py` | Dónde va cada edificio, árbol, camastro y farol, a la altura exacta del terreno | 1 s |
| 2. Fabricar | `blender -b --factory-startup -P herramientas/blender/fabrica.py` | Modela las 55 piezas de la biblioteca y las exporta a FBX | 20 s |
| 3. Importar | `python3 herramientas/importar_unreal.py` | Crea los 44 materiales de la paleta y mete cada pieza a `/Game/Isla/Objetos`. Si una pieza ya existe la aparta como `__viejo`; se borra con `--limpiar` después de reconstruir | 8 min |
| 3b. Materiales | `python3 herramientas/materiales_unreal.py` | Agua por profundidad con reflejo del cielo, vidrio translúcido, texturas fotográficas proyectadas en el mundo, neblina, sol y posproceso | 1 min |
| 4. Construir | `python3 herramientas/construir_isla.py` | Borra la carpeta «Isla» del nivel y coloca las 1,459 piezas | ~20 min |

Pasos 3 y 4 con Unreal abierto en `L_Isla`. Cada paso acepta nombres para rehacer sólo una parte:

```bash
cd ~/Code/isla && blender -b --factory-startup -P herramientas/blender/fabrica.py -- SM_Villa && python3 herramientas/importar_unreal.py SM_Villa
```

```bash
cd ~/Code/isla && python3 herramientas/plano_isla.py && python3 herramientas/construir_isla.py Vegetacion
```

## Archivos

| Archivo | Qué contiene |
|---|---|
| [`herramientas/blender/comun.py`](../herramientas/blender/comun.py) | Paleta de 43 colores (nombre → color y aspereza), figuras básicas, unir, exportar |
| [`herramientas/blender/naturaleza.py`](../herramientas/blender/naturaleza.py) | Palmas cocoteras y reales, almendro, ceiba, buganvilia, hibisco, plumeria, rocas, pasto de duna |
| [`herramientas/blender/muebles.py`](../herramientas/blender/muebles.py) | Camastro, sombrillas, palapa, farol, banca, kayak, cama king, sofá, comedor, doble lavabo, regadera, WC washlet, tina, mesa de restaurante, barra |
| [`herramientas/blender/arquitectura.py`](../herramientas/blender/arquitectura.py) | Edificio del hotel, villa, Villa Horizonte, restaurante, lobby, tienda, spa, cabina de spa, staff, suite de muestra, muelle, yate, hidroavión, pista y hangar |
| [`herramientas/blender/terreno.py`](../herramientas/blender/terreno.py) | Terreno de 4.8 × 4.8 km y la red de caminos pegada al terreno |
| [`herramientas/isla_geo.py`](../herramientas/isla_geo.py) | La forma de la isla (costa, volcán, penínsulas, acantilados) que comparten el terreno y el plano |
| [`herramientas/blender/render_prueba.py`](../herramientas/blender/render_prueba.py) | Foto de revisión en Blender sin abrir Unreal |
| [`herramientas/importar_unreal.py`](../herramientas/importar_unreal.py) · [`construir_isla.py`](../herramientas/construir_isla.py) | Puente con Unreal por el servidor MCP del editor |

## La biblioteca (59 piezas)

| Grupo | Piezas | Medidas que respetan la biblia |
|---|---|---|
| Naturaleza | 4 palmas cocoteras (9–17 m, curvas, con cocos y 18 frondas en V), 2 palmas reales (14–18 m), almendro, ceiba con contrafuertes, buganvilia, hibisco, plumeria, agave, heliconia, helecho, platanera, 3 rocas volcánicas, pasto de duna | Flora del [catálogo](../catalogo/flora.md) |
| Playa y alberca | Camastro, sombrilla de palma, sombrilla de tela, palapa con camastro doble, kayak | Camastro 2.0 × 0.72 m |
| Habitación | Cama king, sofá de 3 plazas, comedor, doble lavabo, regadera de lluvia, WC washlet, tina | Colchón a 58 cm, lavabos a 88 cm separados 80 cm, regadera de 1.0 × 1.4 m con cabezal de 30 cm, asiento de WC a 43 cm |
| Restaurante | Mesa para 2 con vela, barra con bancos | Mesa a 75 cm, silla a 45 cm |
| Arquitectura | Edificio de 100 habitaciones con balcones, villa de 2 niveles con alberca, Villa Horizonte (3 niveles, alberca infinita, mesa de gala para 60), restaurante en abanico con terrazas, lobby de palma, tienda, spa, cabina, staff, **suite de muestra recorrible** | Hotel de 45 × 20 × 17.5 m, villa de 26 × 18 m, Suite Retorno de 100 m² + terraza |
| Experiencia | Alberca principal de 50 × 25 m con escalones y bar dentro del agua, bar de playa redondo, mirador en el borde del cráter, club náutico | |
| Mar | Tramo de muelle, súper yate de 40 m, hidroavión, pista de 2 km con marcas, hangar | |
| Suelo | Terreno (360 mil caras, 7 materiales por zona), red de caminos | Volcán de 420 m con cráter hundido a 330 m; laguna turquesa de ~300 m y caída al azul profundo |

## Lo que está en la isla (plano v2)

1,459 piezas: terreno y mar translúcido, 8 edificios de hotel, lobby, 3 tiendas, suite de muestra, alberca principal con camastros, spa con 8 cabinas, 80 villas, Villa Horizonte con muelle y yate, restaurante con muelle, marina con rompeolas, 52 tramos de muelle, 8 yates y 2 hidroaviones, pista con hangar, 6 edificios de staff, red de caminos con 60 faroles, ~750 árboles y flores (palmas de costa, palmas reales en el anillo, almendros, ceibas y selva en el volcán), rocas al pie de los acantilados, y la playa principal con camastros, sombrillas, palapas, kayaks y bar de playa; además alberca principal con bar dentro del agua, mirador en el borde del cráter, club náutico y 327 plantas de jardín (pasto de duna, agaves en los acantilados, heliconias, helechos y plataneras junto a villas, lobby y spa).

## Probado

- **Jugar dentro del editor (26-oct-2026):** el personaje en primera persona aparece de pie junto a la alberca principal, sobre el terreno, con los edificios del hotel a los lados y el volcán al frente; 1,504 actores en escena.
- Recorrido de cámaras por la isla, la playa, la alberca, Villa Horizonte, el restaurante, la marina, las villas y el cráter (capturas en la portada de isla.capitaltorreon.com).

## Para crecer a miles de objetos

- **Variantes gratis:** cada función recibe semilla, altura y colores, así una palma da cientos de palmas distintas.
- **Agregar un objeto:** escribir su función en el módulo que corresponda, darlo de alta en `BIBLIOTECA` de `fabrica.py` y colocarlo en `plano_isla.py`.
- **Texturas fotográficas (gratis, CC0):** 8 texturas de [Poly Haven](https://polyhaven.com) en 1K (arena de costa, arena mojada, pasto, roca, roca volcánica, madera de roble, estuco y piedra), con color y relieve, en `unreal/fuentes/texturas/` con sus [créditos](../unreal/fuentes/texturas/CREDITOS.md). Como el terreno y los modelos no tienen coordenadas de textura, el material `M_IslaTex` las proyecta según la posición en el mundo; cada color de la paleta las tiñe (pasto seco, selva, madera clara u oscura, estuco arena…). Más texturas: misma licencia, mismo camino.
- **Personajes:** MetaHuman viene gratis con Unreal ([06](06-personajes.md)).

## ¿Comprar o no?

**Recomendación: no comprar por ahora.** Todo lo de hoy costó $0, y los siguientes saltos de calidad también son gratis:

| Siguiente salto | Costo | Qué da |
|---|---|---|
| Más texturas CC0 (Poly Haven, ambientCG) | $0 | Fachadas, telas, paja, mármol y metal con detalle real |
| Plugin **Water** de Unreal (ya viene con el motor) | $0 | Olas, espuma en la orilla, reflejos y cáusticas; requiere reiniciar el editor |
| **MetaHumans** dentro del editor | $0 | Huéspedes y staff de calidad AAA ([06](06-personajes.md)) |
| **PCG** de Unreal (vegetación procedural) | $0 | Miles de plantas con instancias, sin costo de rendimiento |

Si algún día se quisiera acelerar con paquetes ya hechos de la tienda Fab, los de entornos tropicales o de resort suelen costar entre decenas y un par de cientos de dólares cada uno (cifra orientativa, revisar en la tienda). La diferencia hoy no lo justifica: los objetos propios se pueden variar por miles y son nuestros.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
