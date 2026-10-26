# 07 · Islas, capacidad y «siempre llena»

[← Volver al README](../README.md)

## 1. La regla de ocupación (26-oct-2026)

| Llave | Cuántas por isla | Personas máximo | Promedio para proyectar |
|---|---:|---:|---:|
| Habitación | 800 | **hasta 4** | 2.5 |
| Villa | 80 | **hasta 12** (10–12) | 8 |
| **Total por isla** | **880 llaves** | **4,160 huéspedes** | **2,640** |

Esto reemplaza a la cifra de la biblia (máximo 3 por habitación y ~5 por villa, ≈ 2,800 huéspedes). La Villa Horizonte 50 queda como **villa especial de grupo**, aparte de las 80.

**Staff: 2 personas por llave → 1,760 por isla** (la biblia decía 1,200 NPC). En hoteles de ultra lujo la proporción real va de 1.5 a 3 empleados por cuarto. El staff mezcla NPC y, más adelante, usuarios que trabajan en la isla ([00-vision.md](00-vision.md#la-economía-del-mundo-también-se-puede-trabajar-en-la-isla)).

## 2. Una isla por región, no por país

La idea: empezar con una isla y abrir la siguiente cuando la última se llena, para que todas estén siempre llenas y la exclusividad se sienta.

**Ajuste al razonamiento:** dividir por **país** deja islas muy desparejas (México y Estados Unidos frente a países chicos) y separa a gente que habla el mismo idioma y vive a la misma hora. Lo que importa es **la hora**: si todos los de una isla viven en el mismo huso horario, se conectan a la misma hora y la isla se llena en la noche de todos. Por eso se propone **una isla por región horaria e idioma**:

| Orden | Isla | Región | Hora |
|---|---|---|---|
| 1 | **La Encantada** | México, Centroamérica | UTC−6 |
| 2 | *(por nombrar)* | Estados Unidos y Canadá, costa este | UTC−5 |
| 3 | *(por nombrar)* | Sudamérica | UTC−3 |
| 4 | *(por nombrar)* | España y Europa | UTC+1 |
| 5+ | … | Se abre la siguiente donde haya lista de espera | |

Cada isla puede tener su propio nombre (por eso el logotipo es **ISLA** arriba y el nombre abajo). Se puede visitar otra isla como invitado; la reserva vive en la tuya.

**Bono:** con una isla por región, **el sol sigue la hora real de esa región**. Eso resuelve la [decisión abierta 1](00-vision.md#decisiones-abiertas) (el ciclo «18 h de día + 8 h de noche» suma 26 h). Propuesta: ciclo de 24 h real, con amanecer de 6:00 a 7:30, día hasta las 20:00, atardecer de 20:00 a 21:30 y noche de 22:00 a 6:00 (8 h). El atardecer cae cuando más gente está conectada.

## 3. La falla más importante: vendida ≠ llena

Una habitación vendida no significa una persona caminando por la isla. Si cada huésped entra **2 horas al día**, en promedio sólo está dentro **1 de cada 12**.

| Isla al 100 % de ocupación | Personas |
|---|---:|
| Huéspedes con reserva (promedio) | 2,640 |
| Dentro al mismo tiempo, en promedio (2 h de 24) | ≈ 220 |
| Dentro en la hora pico (× 2.5) | ≈ 550 |
| Para **sentirse llena** en una isla de 3–4 km | ≈ 1,500 |
| **Faltan en la hora pico → NPC huéspedes** | **≈ 950** |

Consecuencias de diseño:

1. **Los NPC huéspedes no son relleno barato: son parte del producto.** Usan el mismo generador de belleza que los jugadores ([06-personajes.md](06-personajes.md)) y ceden su lugar a los jugadores reales.
2. **La gente real se concentra donde se ve.** Hay que juntar a los jugadores donde la isla tiene que verse viva (playa principal al atardecer, restaurante, bar, alberca), no regarlos en 3–4 km.
3. **Eventos a hora fija** (atardecer, cena de gala, fiesta en la playa) suben el pico real.
4. **Abrir otra isla diluye la presencia.** La regla para abrir la siguiente no debe ser sólo «habitaciones al 85 %», sino **habitaciones al 85 % durante 4 semanas y lista de espera**. Mientras tanto, la lista de espera es parte de la exclusividad.

## 4. Lo que una isla tiene que poder atender

Con 2,640 huéspedes en promedio, la biblia se queda corta en algunos lugares:

| Servicio | Lo que hay en la biblia | Lo que pide una isla llena | Ajuste |
|---|---|---|---|
| Cenas | Restaurante principal de 120–150 comensales | Si 1 de cada 3 cena en restaurante en la hora pico virtual: ~880 cubiertos | 6–8 restaurantes de 120–150 + bares; el principal se reserva con anticipación (exclusividad) |
| Spa | 120 tipos de masaje | Cabinas suficientes para ~5 % de huéspedes al día | 30–40 cabinas, más en villas |
| Playa y albercas | 1 playa + 1 alberca en el MVP | Camastros para ~25 % de huéspedes a la vez en el pico | Varias playas y albercas por zona |
| Staff | 1,200 NPC | 1,760 (2 por llave) | Actualizado arriba |

## 5. Servidores (lo técnico que cambia todo)

- Un servidor dedicado de Unreal aguanta del orden de **100 jugadores** con calidad alta. Una isla con 550 personas reales en el pico necesita **varios servidores por isla**, partida por zonas: playa, hotel, villas, restaurante, marina. Pasar de zona a zona es como cruzar una puerta.
- El staff y los huéspedes NPC corren del lado del servidor de su zona. Los muy lejanos son sólo «decorado» de bajo costo.
- Esto se prueba en la Fase D con 2 zonas y 20 jugadores reales antes de prometer números.

## 6. Cómo entra al modelo

Todo lo de arriba está en el **modelo v4** ([`web/proyecciones/modelo.js`](../web/proyecciones/modelo.js)): llaves, personas por llave, staff por llave, umbral para abrir isla, horas conectado, factor pico, presencia para sentirse llena y jugadores por servidor. Se ve y se mueve en la página privada [isla.capitaltorreon.com/proyecciones](https://isla.capitaltorreon.com/proyecciones).

<!-- RLR · Ricardo López Reyero · rev 181218 -->
