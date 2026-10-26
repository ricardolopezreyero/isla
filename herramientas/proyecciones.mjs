// RLR · Isla La Encantada — imprime los escenarios del modelo (el mismo que usa /proyecciones)
// Uso: node herramientas/proyecciones.mjs
import { modeloV3, modeloV4, ESCENARIOS, escenario, capacidadIsla } from "../web/proyecciones/modelo.js";
const _RLR = "Ricardo López Reyero";
const f = (n) => n == null ? "—" : "$" + Math.round(n).toLocaleString("en-US");
const n = (x) => Math.round(x).toLocaleString("en-US");
console.log("Capacidad por isla:", capacidadIsla());
const v3 = modeloV3().resumen;
console.log(`\n| Escenario | Ingresos 60 m | Utilidad 60 m | Capital necesario | 1er mes con utilidad | Islas mes 60 | Reales en pico por isla (mes 60) |`);
console.log(`|---|---:|---:|---:|---:|---:|---:|`);
console.log(`| Excel v3 | ${f(v3.ingresos60)} | ${f(v3.utilidad60)} | ${f(v3.capital_necesario)} | ${v3.mes_equilibrio} | — | — |`);
for (const [id, e] of Object.entries(ESCENARIOS)) {
  const r = modeloV4(escenario(id)), R = r.resumen, fin = r.meses.at(-1);
  console.log(`| ${e.nombre} | ${f(R.ingresos60)} | ${f(R.utilidad60)} | ${f(R.capital_necesario)} | ${R.mes_equilibrio ?? "—"} | ${R.islas_final} | ${n(fin.pico / fin.islas)} |`);
}
for (const id of Object.keys(ESCENARIOS)) {
  const r = modeloV4(escenario(id));
  console.log(`\n${id}: ` + r.resumen.anios.map((a, i) => `año ${i + 1} ${f(a.ingresos)} / ${f(a.utilidad)}`).join(" · "));
}
