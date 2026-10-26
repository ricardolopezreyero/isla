# 04 · Unreal Engine 5: cómo se monta el proyecto

[← Volver al README](../README.md)

Guía para dejar el proyecto de Unreal listo y conectado a este repo en cuanto termine la descarga. El objetivo inmediato es la **Fase B (greybox)** del [roadmap](01-roadmap.md).

## 1. Instalar (una vez por máquina)

1. **Epic Games Launcher** → pestaña *Unreal Engine* → *Library* → instalar la **última versión 5.x estable**. Anotar aquí la versión exacta en cuanto quede: `UE 5.__`.
2. En Mac, instalar **Xcode** desde la App Store (Unreal lo pide para compilar shaders y, si algún día se usa C++, para compilar código).
3. **Git LFS**, para que los archivos pesados de Unreal no inflen el repo:

```bash
brew install git-lfs
```

```bash
git lfs install
```

El repo ya trae [`.gitattributes`](../.gitattributes) con `.uasset`, `.umap`, `.fbx`, `.exr` y `.wav` por LFS, y [`.gitignore`](../.gitignore) con lo que Unreal regenera solo (`Binaries/`, `DerivedDataCache/`, `Intermediate/`, `Saved/`).

## 2. Crear el proyecto

En el launcher: *Launch* → **Games** → plantilla **Third Person** →

| Opción | Valor | Por qué |
|---|---|---|
| Tipo | **Blueprint** | El MVP no necesita C++; si luego hace falta, se agrega sin rehacer el proyecto |
| Target platform | Desktop | |
| Quality preset | Maximum | Lumen + Nanite para el look de lujo |
| Starter content | Sí | Materiales y piezas básicas para el greybox |
| Raytracing | No (por ahora) | Se activa en la Fase C si el equipo lo aguanta |
| Ubicación | `~/Code/isla/unreal/` | **Fuera del Escritorio**: el Escritorio está en iCloud y deja los archivos sólo en la nube |
| Nombre | **`IslaEncantada`** | |

Queda en `unreal/IslaEncantada/IslaEncantada.uproject`.

## 3. El mapa de la isla

La isla mide 3–4 km: se trabaja como mundo abierto.

- *File → New Level → **Open World*** (trae World Partition, cielo y luz). Guardar como `Content/Isla/Mapas/L_Isla`.
- **Landscape** de ≈ 4 km × 4 km a 1 m por pixel con margen de mar alrededor (por ejemplo, 8 km × 8 km de agua con la isla al centro).
- Plugin **Water** para mar, olas y orilla; la isla como *Water Body Island*.
- Cielo: *Sky Atmosphere* + *Volumetric Clouds* + *Directional Light* (sol) controlados por un Blueprint de ciclo día/noche (`BP_CicloDia`) con las duraciones de [00-vision.md](00-vision.md#tiempo-y-luz).
- Escala: **1 unidad de Unreal = 1 cm**. Las medidas de la biblia entran directo (cama a 55–60 cm = 55–60 unidades).

## 4. Carpetas dentro de `Content/`

Todo lo nuestro va bajo `Content/Isla/`; los asset packs comprados se quedan en sus propias carpetas y no se tocan.

```
Content/Isla/
├── Mapas/          L_Isla (persistente) y niveles de prueba
├── Zonas/
│   ├── Hotel/      lobby, habitación estándar, Suite Retorno 100
│   ├── Villas/     villa 2–4 recámaras, Villa Horizonte 50
│   ├── Restaurante/
│   ├── Marina/
│   ├── Pista/
│   ├── Spa/
│   ├── Tiendas/    Orillas del Mar, Joya del Océano, Gabinete
│   └── StaffVillage/
├── Naturaleza/
│   ├── Flora/      una carpeta por especie de data/flora.json (id flora-001…)
│   ├── Fauna/      una por especie de data/fauna.json
│   └── Arrecife/
├── Mobiliario/     camas, lavabos, regaderas, mesas, sillas
├── Comida/         platillos por id de data/platillos.json
├── Personajes/     NPC de staff y huéspedes
├── Blueprints/     BP_CicloDia, BP_Puerta, BP_Luz, BP_Asiento, BP_MenuRestaurante
├── UI/
├── Materiales/
└── Audio/          ambientes: jardín, playa, restaurante, noche, bajo el agua
```

## 5. Nombres

| Prefijo | Tipo | Ejemplo |
|---|---|---|
| `L_` | Nivel / mapa | `L_Isla` |
| `SM_` | Static mesh | `SM_Cama_King_200x200` |
| `SK_` | Skeletal mesh | `SK_Mesero` |
| `M_` / `MI_` | Material / instancia | `MI_Piedra_Caliza_Clara` |
| `T_` | Textura | `T_Arena_Blanca_D` |
| `BP_` | Blueprint | `BP_Puerta_Corrediza` |
| `WBP_` | Widget (UI) | `WBP_MenuRestaurante` |
| `DT_` | Data Table | `DT_Platillos` |
| `A_` / `SC_` | Audio / sound cue | `SC_Olas_Playa` |

Las medidas van en el nombre cuando importan (`SM_Lavabo_Doble_Cubierta_90cm`).

## 6. Conectar los catálogos al juego

Los JSON de [`data/`](../data/) son la fuente de verdad. Para que Unreal los lea:

1. Convertir el catálogo a CSV con columnas planas (`id, nombre, descripcion, seccion`) — se agregará un `herramientas/exportar_unreal.py` cuando arranque la Fase D.
2. En Unreal: crear un *Struct* (`S_Platillo`) y un *Data Table* (`DT_Platillos`) importando ese CSV.
3. `WBP_MenuRestaurante` lee `DT_Platillos` para mostrar el menú interactivo.

Así, si cambia un platillo en el repo, se reimporta y el juego queda al día sin tocar Blueprints.

## 7. Subir avances

```bash
cd ~/Code/isla && git add unreal && git commit -m "Greybox: forma de la isla" && git push
```

- Cerrar Unreal antes de hacer commit (deja de escribir en `Saved/`).
- Capturas de cada entrega en `referencias/avances/AAAA-MM-DD/`.
- GitHub cobra el almacenamiento LFS arriba de la cuota gratuita; cuando el proyecto pese varios GB, revisar el plan o mover los binarios a otro almacenamiento.

## 8. Cómo se va a jugar (decisión posterior)

| Opción | Cómo | A favor | En contra |
|---|---|---|---|
| Descarga | Build para Mac/Windows | Calidad máxima, costo de servidor bajo | Hay que instalar |
| **Pixel Streaming** | El juego corre en GPU en la nube y se ve en isla.capitaltorreon.com | Se juega desde el navegador, cualquier equipo | Costo de GPU por hora por usuario |
| Video/recorridos | Renders y paseos grabados en la web | Barato, sirve para vender la idea | No es jugable |

Para el MVP 0.1 basta un build local. La web empieza mostrando recorridos y capturas.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
