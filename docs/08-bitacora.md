# 08 · La bitácora de cada huésped

[← Volver al README](../README.md)

> **Pedido:** cada usuario tiene una bitácora y todo se va registrando, para que ese avatar sea único y especial en este mundo.

## 1. Qué es

Un **diario de estancia** que se escribe solo. Cada cosa que haces en la isla queda como un renglón con fecha y hora. Con eso:

- **La isla te recuerda:** tu mesero sabe qué pediste la última vez, tu terapeuta qué presión prefieres y tu concierge a qué hora te gusta el atardecer.
- **Tú recuerdas:** «Mis recuerdos» junta lo mejor (primer buceo, cenas, fotos, gente que conociste) en un álbum que se puede ver como línea del tiempo.
- **Tu avatar se vuelve único:** insignias, historia y costumbres que nadie más tiene. Cambiar de look no borra nada (ver [06-personajes.md](06-personajes.md)).

## 2. Qué se registra

| Tipo | Ejemplos | Para qué sirve |
|---|---|---|
| `llegada` / `salida` | Entró por la marina a las 21:04 · salió de la villa 12 | Historial de estancias y horarios favoritos |
| `look` | Eligió «Ella · llegada del 26 oct», cambió el pelo, se puso el kimono de olas | Guardarropa y looks guardados |
| `reserva` | Habitación 314 · 3 noches · 4 personas | Estancias y ocupación real |
| `comida` | Taco de camarón al pastor (platillos-001), margarita de tamarindo | «¿Lo de siempre?» del mesero |
| `spa` | Masaje con piedras calientes (masajes-008), presión media | El terapeuta recuerda la presión |
| `experiencia` | Buceo nocturno con linternas (experiencias-003) | Insignias y recomendaciones dentro de la isla |
| `compra` | Toalla «Mar Profundo» (tiendas-001) | Inventario personal |
| `encuentro` | Brindó con Valeria · bailaron en la playa | Amistades (sólo si los dos lo aceptan) |
| `foto` | Foto en el mirador del cráter al atardecer | Álbum |
| `logro` | 10 atardeceres · primera mantarraya | Insignias |
| `ajuste` | Burbuja personal 1.5 m · no aparecer en fotos | Comodidad |

Los `id` de catálogo (`platillos-001`, `masajes-008`…) son los mismos de [`data/`](../data/): la bitácora y los catálogos hablan el mismo idioma.

## 3. Cómo se guarda (técnico)

Una tabla que **sólo crece** (nunca se reescribe la historia) en Cloudflare D1, la misma base `isla` que ya usa la página de proyecciones:

```sql
CREATE TABLE bitacora (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  quien     TEXT NOT NULL,        -- sub del login de CapitalTorreon (no el correo)
  isla      TEXT NOT NULL DEFAULT 'la-encantada',
  tipo      TEXT NOT NULL,        -- llegada, look, comida, spa, experiencia…
  ref       TEXT,                 -- id de catálogo (platillos-001) u otro objeto
  detalle   TEXT,                 -- JSON con lo particular del evento
  creado    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX bitacora_quien ON bitacora (quien, creado);
```

- **Quién:** el `sub` del [Login de CapitalTorreon](05-web-y-dominio.md): la misma persona en la web, en el juego y en cualquier servicio de la casa.
- El juego escribe en lotes (cada 30 s o al salir) a una API del Worker `isla`; la web la lee.
- Cuando el volumen crezca (miles de eventos por segundo), la bitácora pasa a un almacén de eventos y D1 se queda con los resúmenes.

**Ya funciona hoy en pequeño:** la página privada de proyecciones escribe en esta tabla cada vez que entras, guardas o borras un escenario. Es la primera bitácora del proyecto.

## 4. Privacidad (para que dé gusto, no miedo)

- **Tu bitácora es tuya:** sólo tú la ves completa. El staff (NPC) sólo «recuerda» lo necesario para atenderte.
- **Ver, descargar y borrar** desde tu cuenta, como ya existe en la página `/cuenta` del login de la casa.
- Los `encuentro` necesitan que los dos acepten; si alguien te bloquea, desaparece de tu bitácora y tú de la suya.
- Antes de abrir al público: aviso de privacidad conforme a la ley mexicana de protección de datos (LFPDPPP) y, si entran usuarios de Europa, el reglamento europeo (GDPR).

<!-- RLR · Ricardo López Reyero · rev 181218 -->
