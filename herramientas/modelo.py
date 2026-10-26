# RLR · Isla La Encantada — Ricardo López Reyero
# Réplica en código de fuentes/modelo/IslaEncantada_Model_v3.xlsx (hojas Supuestos,
# Proyeccion_60m y Resumen_Exec). Mismas fórmulas, mismos resultados al centavo.
# Uso: python3 herramientas/modelo.py   → escribe data/modelo.json
# Para probar otro escenario: cambiar SUPUESTOS y volver a correr.
import json
from pathlib import Path

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent

SUPUESTOS = {
    # Usuarios y crecimiento
    "Start_DAU": 1500,             # usuarios activos diarios promedio al mes 1
    "Max_DAU": 100000,             # capacidad técnica máxima de usuarios activos diarios
    "Organic_growth": 0.06,        # crecimiento orgánico mensual
    "Improvement_growth": 0.02,    # extra de crecimiento por mejoras (+1 % features)
    "Days_per_month": 30.4,
    # Marketing y CAC
    "Marketing_month1": 30000,     # USD, mes 1
    "Marketing_growth": 0.07,      # crecimiento mensual del presupuesto
    "Paid_CAC": 18,                # USD por usuario nuevo pagado
    # Monetización por usuario activo en 24 h (USD)
    "Rev_room_per_user_per_day": 35,
    "Rev_activities_per_user_per_day": 15,
    "Rev_shops_per_user_per_day": 5,
    # Costos
    "Var_cost_per_user_per_day": 4,  # servidores, soporte, plataforma
    "Founder_salary": 8000,
    "Env_artist_salary": 5000,
    "Tech_dev_salary": 6000,
    "Support_Ops_team_salary": 6000,
    "Other_fixed_costs": 6000,
    "Projection_months": 60,
}


def proyectar(s=SUPUESTOS):
    arpu = s["Rev_room_per_user_per_day"] + s["Rev_activities_per_user_per_day"] + s["Rev_shops_per_user_per_day"]
    sueldos = s["Founder_salary"] + s["Env_artist_salary"] + s["Tech_dev_salary"] + s["Support_Ops_team_salary"]
    dias, meses = s["Days_per_month"], []
    for mes in range(1, s["Projection_months"] + 1):
        if mes == 1:
            mkt = s["Marketing_month1"]
            pagados = mkt / s["Paid_CAC"] if s["Paid_CAC"] > 0 else 0
            dau = s["Start_DAU"]
            nuevos = dau
        else:
            prev = meses[-1]
            mkt = prev["marketing"] * (1 + s["Marketing_growth"])
            pagados = mkt / s["Paid_CAC"] if s["Paid_CAC"] > 0 else 0
            crec = s["Organic_growth"] + s["Improvement_growth"]
            dau = min(s["Max_DAU"], prev["dau"] * (1 + crec) + pagados)
            nuevos = prev["dau"] * crec + pagados
        hab = dau * s["Rev_room_per_user_per_day"] * dias
        act = dau * s["Rev_activities_per_user_per_day"] * dias
        tie = dau * s["Rev_shops_per_user_per_day"] * dias
        ingresos = hab + act + tie
        variables = dau * s["Var_cost_per_user_per_day"] * dias
        costos = variables + sueldos + s["Other_fixed_costs"] + mkt
        utilidad = ingresos - costos
        meses.append({
            "mes": mes, "dau": dau, "nuevos": nuevos, "nuevos_pagados": pagados,
            "nuevos_organicos": max(nuevos - pagados, 0), "arpu_dia": arpu,
            "ingresos": ingresos, "ingresos_habitaciones": hab, "ingresos_actividades": act,
            "ingresos_tiendas": tie, "costos_variables": variables, "sueldos": sueldos,
            "otros_fijos": s["Other_fixed_costs"], "marketing": mkt, "costos": costos,
            "utilidad": utilidad,
            "utilidad_usuario_dia": utilidad / (dau * dias) if dau * dias > 0 else 0,
            "cac_mezclado": mkt / nuevos if nuevos > 0 else 0,
            "margen": utilidad / ingresos if ingresos > 0 else 0,
        })
    return meses


if __name__ == "__main__":
    meses = proyectar()
    # Comprobación contra los valores guardados en el Excel (mes 1 y mes 60)
    assert round(meses[0]["utilidad"], 2) == 2264600.00
    assert round(meses[59]["utilidad"], 2) == 153384333.83
    resumen = {m: meses[m - 1] for m in (1, 12, 36, 60)}
    (RAIZ / "data" / "modelo.json").write_text(json.dumps({
        "fuente": "fuentes/modelo/IslaEncantada_Model_v3.xlsx",
        "escenario": "Agresivo, realista y optimista (tal cual el Excel v3)",
        "supuestos": SUPUESTOS,
        "resumen": {str(k): {c: round(v, 4) for c, v in r.items()} for k, r in resumen.items()},
        "meses": [{c: round(v, 4) for c, v in m.items()} for m in meses],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tope = next(m["mes"] for m in meses if m["dau"] >= SUPUESTOS["Max_DAU"])
    print(f"OK · igual al Excel · tope de {SUPUESTOS['Max_DAU']:,} DAU en el mes {tope}")
    for k, r in resumen.items():
        print(f"mes {k:2}: DAU {r['dau']:>9,.0f} · ingresos ${r['ingresos']:>14,.0f} · "
              f"utilidad ${r['utilidad']:>14,.0f} · margen {r['margen']:.1%} · CAC ${r['cac_mezclado']:.2f}")
    print("acumulado 60 m: ingresos $%s · utilidad $%s" % (
        f"{sum(m['ingresos'] for m in meses):,.0f}", f"{sum(m['utilidad'] for m in meses):,.0f}"))
