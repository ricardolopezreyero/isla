-- RLR · Isla La Encantada · base D1 `isla` — Ricardo López Reyero
-- Escenarios guardados desde /proyecciones y la bitácora (ver docs/08-bitacora.md)
CREATE TABLE IF NOT EXISTS escenarios (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  quien       TEXT NOT NULL,          -- sub del login de CapitalTorreon
  correo      TEXT NOT NULL,
  nombre      TEXT NOT NULL,
  base        TEXT NOT NULL,          -- biblia | prudente | conservador
  supuestos   TEXT NOT NULL,          -- JSON con los cambios sobre la base
  creado      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  actualizado TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS escenarios_quien ON escenarios (quien, actualizado);

CREATE TABLE IF NOT EXISTS bitacora (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  quien     TEXT NOT NULL,
  isla      TEXT NOT NULL DEFAULT 'la-encantada',
  tipo      TEXT NOT NULL,
  ref       TEXT,
  detalle   TEXT,
  creado    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS bitacora_quien ON bitacora (quien, creado);
