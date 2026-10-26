// RLR · Isla La Encantada — modelo de proyecciones · Ricardo López Reyero
// Un solo módulo para la página privada /proyecciones y para herramientas/proyecciones.mjs.
//   modeloV3(s) → réplica exacta del Excel v3 (ingreso por usuario activo al día)
//   modeloV4(s) → por isla: llaves, personas por llave, ocupación, islas que se abren al llenarse,
//                 construcción antes de lanzar y los costos que el v3 no traía
// Todo en USD, por mes, 60 meses.
export const _RLR = "Ricardo López Reyero", _k = "EYE", _rev = 181218;

export const DIAS = 30.4;

// ── v3: el Excel tal cual (fuentes/modelo/IslaEncantada_Model_v3.xlsx)
export const V3 = {
  Start_DAU: 1500, Max_DAU: 100000, Organic_growth: 0.06, Improvement_growth: 0.02,
  Marketing_month1: 30000, Marketing_growth: 0.07, Paid_CAC: 18,
  Rev_room: 35, Rev_activities: 15, Rev_shops: 5, Var_cost: 4,
  Salaries: 25000, Other_fixed: 6000, Months: 60,
};

export function modeloV3(s = V3) {
  const arpu = s.Rev_room + s.Rev_activities + s.Rev_shops, meses = [];
  for (let mes = 1; mes <= s.Months; mes++) {
    const prev = meses[mes - 2];
    const mkt = mes === 1 ? s.Marketing_month1 : prev.marketing * (1 + s.Marketing_growth);
    const pagados = s.Paid_CAC > 0 ? mkt / s.Paid_CAC : 0;
    const crec = s.Organic_growth + s.Improvement_growth;
    const dau = mes === 1 ? s.Start_DAU : Math.min(s.Max_DAU, prev.dau * (1 + crec) + pagados);
    const ingresos = dau * arpu * DIAS;
    const costos = dau * s.Var_cost * DIAS + s.Salaries + s.Other_fixed + mkt;
    meses.push({ mes, dau, marketing: mkt, ingresos, costos, utilidad: ingresos - costos, islas: null, huespedes: null });
  }
  return acumular(meses);
}

// ── v4: por isla
// RLR · reglas de Ricardo (26-oct-2026): hasta 4 personas por habitación y hasta 10–12 por villa; cada noche va
//        de 12:00 a 12:00 (como hotel) y el mes tiene 30.4 noches; Villa Horizonte = 10× villa, 5× recámaras;
//        una isla por región, se abre la siguiente cuando la última se llena.
export const V4_BASE = {
  // Capacidad de cada isla
  habitaciones: 800, max_por_habitacion: 4, prom_por_habitacion: 2.5,
  villas: 80, max_por_villa: 12, prom_por_villa: 8,
  // RLR · Villa Horizonte (docs/10): una por isla, 25 suites, hasta 60 personas, 10 veces el precio de una villa
  villa_horizonte: 1, max_por_horizonte: 60, prom_por_horizonte: 45,
  factor_precio_horizonte: 10, ocupacion_horizonte: 0.3, staff_horizonte: 60,
  staff_por_llave: 2,               // personas de staff (NPC + usuarios-staff) por habitación o villa
  // Precios por noche, por llave (no por persona). RLR · 26-oct-2026: Ricardo bajó todo para empezar abajo y subir
  // con experimentos: Horizonte 1,000 USD y lo demás proporcional (villa = 1/10, habitación = 1/100 de la villa)
  precio_habitacion: 1, precio_villa: 100,
  gasto_huesped_dia: 0.2,           // actividades + tiendas + restaurantes, por huésped al día
  // Demanda
  mes_lanzamiento: 7,               // meses 1..6 = construir el MVP y la primera isla
  ocupacion_inicial: 0.15,          // de la primera isla, el mes del lanzamiento
  crecimiento_mensual: 0.12,        // de la demanda de habitaciones
  factor_villas: 0.6,               // ocupación de villas = ocupación de habitaciones × factor
  umbral_nueva_isla: 0.85,          // se abre otra isla cuando la demanda pasa de este % de lo que hay
  max_islas: 12,
  // Uso
  horas_conectado: 2,               // horas al día que cada huésped está dentro
  costo_hora: 0.25,                 // servidores / streaming por hora conectada
  factor_pico: 2.5,                 // en la hora pico entra 2.5 veces el promedio
  presencia_llena: 1500,            // personas visibles para que una isla se sienta llena
  jugadores_por_servidor: 100,      // lo que aguanta un servidor dedicado de Unreal con buena calidad
  // Costos
  comision_pagos: 0.04,             // pasarela de pago
  comision_tiendas: 0,              // 0.30 si se vende dentro de App Store / Google Play
  regalia_unreal: 0.05,             // sobre ingresos brutos acumulados arriba de 1 millón
  construccion_mes: 25000,          // freelancers + herramientas mientras no se lanza
  assets_iniciales: 15000,          // asset packs y licencias, mes 1
  equipo_base: 31000,               // equipo central (los 25 k + 6 k fijos del v3)
  equipo_por_isla: 35000,           // operación, moderación, eventos y soporte de cada isla
  marketing_base: 30000, marketing_pct: 0.12,
  meses: 60,
};

// RLR · empezar abajo y subir: cada escenario es el siguiente experimento de precio
export const ESCENARIOS = {
  lanzamiento: { nombre: "Lanzamiento", nota: "Horizonte 1,000 USD la noche, villa 100 y habitación 1: empezar abajo", s: {} },
  subida:      { nombre: "Primera subida", nota: "Si el lanzamiento se llena: todo al doble",
                 s: { precio_habitacion: 2, precio_villa: 200, gasto_huesped_dia: 0.5 } },
  meta:        { nombre: "Meta", nota: "Después de varias subidas: 5 veces el lanzamiento",
                 s: { precio_habitacion: 5, precio_villa: 500, gasto_huesped_dia: 1 } },
};

export const escenario = (id, cambios = {}) => ({ ...V4_BASE, ...(ESCENARIOS[id]?.s || {}), ...cambios });

export function capacidadIsla(s = V4_BASE) {
  const llaves = s.habitaciones + s.villas + s.villa_horizonte;
  return {
    llaves,
    max_personas: s.habitaciones * s.max_por_habitacion + s.villas * s.max_por_villa + s.villa_horizonte * s.max_por_horizonte,
    prom_personas: s.habitaciones * s.prom_por_habitacion + s.villas * s.prom_por_villa + s.villa_horizonte * s.prom_por_horizonte,
    staff: Math.round((s.habitaciones + s.villas) * s.staff_por_llave + s.villa_horizonte * s.staff_horizonte),
  };
}

export function modeloV4(s = V4_BASE) {
  const meses = [];
  let demanda = 0, islas = 0, acumIngresos = 0;
  for (let mes = 1; mes <= s.meses; mes++) {
    const vivo = mes >= s.mes_lanzamiento;
    if (vivo) {
      demanda = mes === s.mes_lanzamiento ? s.ocupacion_inicial * s.habitaciones : demanda * (1 + s.crecimiento_mensual);
      const necesarias = Math.ceil(demanda / (s.habitaciones * s.umbral_nueva_isla));
      islas = Math.min(s.max_islas, Math.max(islas, 1, necesarias));
    }
    const habOcupadas = vivo ? Math.min(demanda, islas * s.habitaciones) : 0;
    const ocupacion = vivo ? habOcupadas / (islas * s.habitaciones) : 0;
    const villasOcupadas = islas * s.villas * Math.min(1, ocupacion * s.factor_villas);
    const horizonteOcupadas = vivo ? islas * s.villa_horizonte * s.ocupacion_horizonte : 0;
    const huespedes = habOcupadas * s.prom_por_habitacion + villasOcupadas * s.prom_por_villa + horizonteOcupadas * s.prom_por_horizonte;

    const ingHab = habOcupadas * s.precio_habitacion * DIAS;
    const ingVillas = villasOcupadas * s.precio_villa * DIAS;
    const ingGasto = huespedes * s.gasto_huesped_dia * DIAS;
    const ingHorizonte = horizonteOcupadas * s.precio_villa * s.factor_precio_horizonte * DIAS;
    const ingresos = ingHab + ingVillas + ingHorizonte + ingGasto;

    const regalia = s.regalia_unreal * Math.max(0, acumIngresos + ingresos - 1e6) - s.regalia_unreal * Math.max(0, acumIngresos - 1e6);
    acumIngresos += ingresos;
    const servidores = huespedes * s.horas_conectado * s.costo_hora * DIAS;
    const comisiones = ingresos * (s.comision_pagos + s.comision_tiendas);
    const equipo = vivo ? s.equipo_base + s.equipo_por_isla * islas : s.construccion_mes;
    const marketing = vivo ? s.marketing_base + s.marketing_pct * ingresos : (mes >= s.mes_lanzamiento - 2 ? s.marketing_base : 0);
    const assets = mes === 1 ? s.assets_iniciales : 0;
    const costos = servidores + comisiones + regalia + equipo + marketing + assets;

    meses.push({
      mes, islas, ocupacion, habOcupadas, villasOcupadas, huespedes,
      conectados: huespedes * s.horas_conectado / 24,           // promedio simultáneo
      pico: huespedes * s.horas_conectado / 24 * s.factor_pico,
      // RLR · lo que falta para verse llena en la hora pico lo ponen NPC huéspedes
      npc_relleno: islas ? Math.max(0, s.presencia_llena - huespedes * s.horas_conectado / 24 * s.factor_pico / islas) * islas : 0,
      servidores_pico: Math.ceil(huespedes * s.horas_conectado / 24 * s.factor_pico / s.jugadores_por_servidor),
      staff: islas * capacidadIsla(s).staff,
      ingresos, ingHab, ingVillas, ingHorizonte, ingGasto, horizonteOcupadas,
      servidores, comisiones, regalia, equipo, marketing, assets, costos,
      utilidad: ingresos - costos,
    });
  }
  return acumular(meses);
}

function acumular(meses) {
  let caja = 0, peor = 0, mesPeor = 0, equilibrio = null;
  for (const m of meses) {
    caja += m.utilidad; m.caja = caja;
    if (caja < peor) { peor = caja; mesPeor = m.mes; }
    if (equilibrio === null && m.utilidad > 0 && m.ingresos > 0) equilibrio = m.mes;
  }
  const anio = (a) => meses.slice((a - 1) * 12, a * 12).reduce((t, m) => ({ ingresos: t.ingresos + m.ingresos, utilidad: t.utilidad + m.utilidad }), { ingresos: 0, utilidad: 0 });
  const recuperacion = meses.find((m) => m.mes > mesPeor && m.caja >= 0)?.mes ?? null;
  return {
    meses,
    resumen: {
      ingresos60: meses.reduce((t, m) => t + m.ingresos, 0),
      utilidad60: caja,
      capital_necesario: peor < 0 ? -peor : 0,   // lo más hondo que baja la caja: lo que hay que poner antes de que se pague sola
      mes_equilibrio: equilibrio,   // primer mes con utilidad
      mes_recuperacion: peor < 0 ? recuperacion : null,
      islas_final: meses.at(-1).islas,
      anios: [1, 2, 3, 4, 5].map(anio),
    },
  };
}
// RLR · fin
