// RLR · Isla La Encantada · Worker — Ricardo López Reyero
// Sirve web/ tal cual. Sólo pasan por aquí /proyecciones (página privada) y /api/*.
// /proyecciones es pública como cascarón (no trae números): los datos sólo salen de /api/proyecciones/*
// con un pase del Login de CapitalTorreon cuyo correo esté en PERMITIDOS. Cada visita queda en la bitácora.
import { verificarPase } from "./verificar.js";

const _RLR = "Ricardo López Reyero", _k = "EYE", _rev = 181218;
const AUD = ["isla.capitaltorreon.com", "localhost"];
const BASES = ["biblia", "prudente", "conservador"];
// RLR · Ricardo entra con contacto@ingenieriadigital.mx pero se muestra su correo de trabajo
const CORREO_DE_TRABAJO = { "contacto@ingenieriadigital.mx": "ricardo@superleads.mx" };

const PRIVADO = {
  "cache-control": "no-store, no-transform",
  "x-robots-tag": "noindex, nofollow",
  "referrer-policy": "no-referrer",
  "x-frame-options": "DENY",
  "x-content-type-options": "nosniff",
};
const json = (datos, status = 200) => new Response(JSON.stringify(datos), { status, headers: { "content-type": "application/json; charset=utf-8", ...PRIVADO } });

async function quien(req, env, cuerpo) {
  const c = await verificarPase(cuerpo?.pase, AUD, env.JWKS_PRUEBA);
  if (!c?.email) return { error: json({ ok: false, motivo: "sin-sesion" }, 401) };
  const permitidos = String(env.PERMITIDOS || "").split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);
  const correo = String(c.email).toLowerCase();
  if (!permitidos.includes(correo)) return { error: json({ ok: false, motivo: "privada" }, 403) };
  return { sub: c.sub, correo: CORREO_DE_TRABAJO[correo] || correo, nombre: c.name || "" };
}

const anotar = (env, q, tipo, ref, detalle) =>
  env.DB.prepare("INSERT INTO bitacora (quien, tipo, ref, detalle) VALUES (?, ?, ?, ?)")
    .bind(q.sub, tipo, ref ?? null, JSON.stringify({ correo: q.correo, ...(detalle || {}) })).run();

async function api(req, env, url) {
  if (req.method !== "POST") return json({ ok: false }, 405);
  const origen = req.headers.get("origin");
  // RLR · en local (JWKS_PRUEBA sólo existe en .dev.vars) wrangler reescribe el Origin al dominio en http, y el navegador
  //       de pruebas del escritorio manda "null": esos dos casos sólo se aceptan ahí
  const origenOk = !origen || /^https:\/\/isla\.capitaltorreon\.com$|^http:\/\/localhost(:\d+)?$/.test(origen)
    || (env.JWKS_PRUEBA && (origen === "null" || origen === "http://isla.capitaltorreon.com"));
  if (!origenOk) return json({ ok: false, motivo: "origen", ...(env.JWKS_PRUEBA ? { origen } : {}) }, 403);
  let cuerpo = {}; try { cuerpo = await req.json(); } catch {}
  const q = await quien(req, env, cuerpo); if (q.error) return q.error;
  const ruta = url.pathname.replace(/^\/api\/proyecciones\/?/, "");

  if (ruta === "datos") {
    if (!cuerpo.silencio) await anotar(env, q, "entro", "proyecciones");
    const [esc, bit] = await Promise.all([
      env.DB.prepare("SELECT id, nombre, base, supuestos, actualizado FROM escenarios WHERE quien = ? ORDER BY actualizado DESC LIMIT 50").bind(q.sub).all(),
      env.DB.prepare("SELECT tipo, ref, detalle, creado FROM bitacora WHERE quien = ? ORDER BY id DESC LIMIT 30").bind(q.sub).all(),
    ]);
    return json({
      ok: true, quien: { correo: q.correo, nombre: q.nombre },
      escenarios: esc.results.map((e) => ({ ...e, supuestos: JSON.parse(e.supuestos) })),
      bitacora: bit.results.map((b) => ({ ...b, detalle: b.detalle ? JSON.parse(b.detalle) : null })),
    });
  }
  if (ruta === "guardar") {
    const nombre = String(cuerpo.nombre || "").trim().slice(0, 80);
    const base = BASES.includes(cuerpo.base) ? cuerpo.base : null;
    const sup = cuerpo.supuestos && typeof cuerpo.supuestos === "object" ? cuerpo.supuestos : null;
    if (!nombre || !base || !sup) return json({ ok: false, motivo: "faltan-datos" }, 400);
    const limpio = Object.fromEntries(Object.entries(sup).filter(([k, v]) => /^[a-z_]{1,40}$/.test(k) && Number.isFinite(v)).slice(0, 60));
    const r = await env.DB.prepare("INSERT INTO escenarios (quien, correo, nombre, base, supuestos) VALUES (?, ?, ?, ?, ?) RETURNING id")
      .bind(q.sub, q.correo, nombre, base, JSON.stringify(limpio)).first();
    await anotar(env, q, "guardo-escenario", String(r.id), { nombre, base });
    return json({ ok: true, id: r.id });
  }
  if (ruta === "borrar") {
    const id = Number(cuerpo.id);
    const fila = await env.DB.prepare("SELECT nombre FROM escenarios WHERE id = ? AND quien = ?").bind(id, q.sub).first();
    if (!fila) return json({ ok: false }, 404);
    await env.DB.prepare("DELETE FROM escenarios WHERE id = ? AND quien = ?").bind(id, q.sub).run();
    await anotar(env, q, "borro-escenario", String(id), { nombre: fila.nombre });
    return json({ ok: true });
  }
  return json({ ok: false }, 404);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/proyecciones")) return api(req, env, url);
    if (url.pathname.startsWith("/api/")) return json({ ok: false }, 404);
    if (url.pathname === "/proyecciones" || url.pathname === "/proyecciones/" || url.pathname === "/proyecciones/index.html") {
      const r = await env.ASSETS.fetch(new Request(new URL("/proyecciones/", url), req));
      const h = new Headers(r.headers); for (const [k, v] of Object.entries(PRIVADO)) h.set(k, v);
      return new Response(r.body, { status: r.status, headers: h });
    }
    return env.ASSETS.fetch(req);
  },
};
// RLR · fin
