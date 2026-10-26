# 03 · Modelo financiero (v3)

[← Volver al README](../README.md)

- **Fuente:** [`fuentes/modelo/IslaEncantada_Model_v3.xlsx`](../fuentes/modelo/IslaEncantada_Model_v3.xlsx) (hojas *Supuestos*, *Proyeccion_60m*, *Resumen_Exec*)
- **En código:** [`herramientas/modelo.py`](../herramientas/modelo.py) replica las mismas fórmulas y comprueba que da igual al Excel al centavo (mes 1 y mes 60).
- **Datos:** [`data/modelo.json`](../data/modelo.json) con supuestos, resumen y los 60 meses.
- **Escenario del Excel:** «Agresivo, realista y optimista». Todo en USD.

Para probar otro escenario: cambiar `SUPUESTOS` en `herramientas/modelo.py` y correr `python3 herramientas/modelo.py`.

## Supuestos

| Grupo | Supuesto | Valor | Qué significa |
|---|---|---:|---|
| Usuarios | `Start_DAU` | 1,500 | Usuarios activos diarios promedio en el mes 1 |
| | `Max_DAU` | 100,000 | Capacidad técnica máxima de usuarios activos diarios |
| | `Organic_growth` | 6 % | Crecimiento orgánico mensual |
| | `Improvement_growth` | 2 % | Crecimiento extra por mejoras al producto |
| | `Days_per_month` | 30.4 | Días promedio por mes |
| Marketing | `Marketing_month1` | 30,000 | Gasto de marketing del mes 1 |
| | `Marketing_growth` | 7 % | Crecimiento mensual del presupuesto |
| | `Paid_CAC` | 18 | Costo por usuario nuevo pagado |
| Ingreso por usuario activo en 24 h | `Rev_room_per_user_per_day` | 35 | «Habitación» virtual |
| | `Rev_activities_per_user_per_day` | 15 | Actividades |
| | `Rev_shops_per_user_per_day` | 5 | Tiendas y regalos |
| | **ARPU diario** | **55** | Suma de los tres |
| Costos | `Var_cost_per_user_per_day` | 4 | Servidores, soporte y plataforma por usuario activo en 24 h |
| | `Founder_salary` | 8,000 | Mensual |
| | `Env_artist_salary` | 5,000 | Mensual |
| | `Tech_dev_salary` | 6,000 | Mensual |
| | `Support_Ops_team_salary` | 6,000 | Mensual |
| | `Other_fixed_costs` | 6,000 | Herramientas, administración, etc. |
| | `Projection_months` | 60 | Horizonte |

## Cómo calcula

- **Mes 1:** DAU = 1,500; nuevos pagados = marketing ÷ CAC.
- **Mes siguiente:** marketing crece 7 %; DAU = mínimo entre 100,000 y DAU anterior × (1 + 6 % + 2 %) + nuevos pagados.
- **Ingresos** = DAU × 55 × 30.4 (repartidos 35 / 15 / 5).
- **Costos** = DAU × 4 × 30.4 + 25,000 de sueldos + 6,000 fijos + marketing.
- **CAC mezclado** = marketing ÷ todos los nuevos (orgánicos + pagados).

## Resultado

| Mes | DAU | Nuevos pagados | Marketing | Ingresos | Costos | Utilidad | Margen | CAC mezclado |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,500 | 1,667 | $30,000 | $2,508,000 | $243,400 | $2,264,600 | 90.3 % | $20.00 |
| 3 | 5,584 | 1,908 | $34,347 | $9,336,058 | $744,333 | $8,591,725 | 92.0 % | $15.75 |
| 6 | 14,112 | 2,338 | $42,077 | $23,596,001 | $1,789,149 | $21,806,851 | 92.4 % | $13.11 |
| 9 | 26,449 | 2,864 | $51,546 | $44,222,863 | $3,298,754 | $40,924,109 | 92.5 % | $11.18 |
| 12 | 43,941 | 3,508 | $63,146 | $73,469,600 | $5,437,389 | $68,032,211 | 92.6 % | $9.71 |
| 18 | 100,000 | 5,265 | $94,764 | $167,200,000 | $12,285,764 | $154,914,236 | 92.7 % | $7.62 |
| 24 | 100,000 | 7,901 | $142,216 | $167,200,000 | $12,333,216 | $154,866,784 | 92.6 % | $8.94 |
| 36 | 100,000 | 17,794 | $320,297 | $167,200,000 | $12,511,297 | $154,688,703 | 92.5 % | $12.42 |
| 48 | 100,000 | 40,076 | $721,371 | $167,200,000 | $12,912,371 | $154,287,629 | 92.3 % | $15.00 |
| 60 | 100,000 | 90,259 | $1,624,666 | $167,200,000 | $13,815,666 | $153,384,334 | 91.7 % | $16.53 |

- Llega al tope de **100,000 DAU en el mes 18**.
- Acumulado a 60 meses: **ingresos ≈ $8,142 millones** y **utilidad ≈ $7,524 millones** de USD.
- Marketing acumulado: ≈ $24.4 millones.

## Lectura crítica (para la siguiente versión del modelo)

El modelo es útil como esqueleto; los números de entrada son de techo y conviene contrastarlos antes de enseñarlo afuera.

1. **El ARPU es el supuesto que lo define todo.** 55 USD por usuario activo cada día equivale a ≈ 1,672 USD al mes por usuario. En juegos y mundos virtuales es común que el ingreso promedio por usuario activo al día se mida en centavos o pocos dólares. Separar en el modelo a quien *visita* (gratis o barato) de quien *se hospeda* (paga habitación) y poner un porcentaje de conversión.
2. **Capacidad física vs. DAU.** La isla admite ≈ 2,800 huéspedes simultáneos sin sobreventa; 100,000 DAU exige decidir instancias o turnos ([decisión abierta 2](00-vision.md#decisiones-abiertas)) y eso cambia el costo de servidores.
3. **Costo variable de 4 USD/día.** Si el mundo se juega por streaming desde la nube (Pixel Streaming), el costo por hora de GPU puede superar eso; si se descarga, baja mucho. Depende de la decisión de distribución.
4. **Sueldos fijos de 25,000 USD/mes** durante 60 meses aun con 100,000 DAU: falta escalar equipo (soporte, contenido, operación del mundo, moderación).
5. **Después del mes 18 el marketing sigue creciendo 7 % al mes, pero el DAU ya topó:** los usuarios pagados ya no suman. Conviene topar también el marketing o modelar la rotación (usuarios que se van).
6. **No hay inversión inicial** (asset packs, freelancers por proyecto, licencias, servidores) ni el 5 % de regalías de Unreal Engine sobre ingresos brutos arriba de 1 millón de USD por producto.
7. **Precios distintos entre documentos:** 100 USD/noche y 10,000 USD/noche en la biblia vs. 35 USD/día por usuario en el modelo ([decisión abierta 4](00-vision.md#decisiones-abiertas)).

<!-- RLR · Ricardo López Reyero · rev 181218 -->
