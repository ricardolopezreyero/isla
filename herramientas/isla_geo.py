# RLR · Isla La Encantada — Ricardo López Reyero
# Geometría compartida de la isla (Python puro): la usan el terreno en Blender (herramientas/blender/terreno.py)
# y el plano de colocación (herramientas/plano_isla.py), así todo cae exactamente sobre el suelo.
# Metros; norte = +X, este = +Y; θ en grados desde el norte hacia el este.
import math

_RLR = "Ricardo López Reyero"

R_ISLA = 1750.0
VOLCAN = (200.0, 150.0)
SUELO = 6.0
HX = 2120.0                     # centro de la península de Villa Horizonte (norte)
TH_R = math.radians(250)        # dirección del restaurante (oeste-suroeste)
RX, RY = 2000 * math.cos(TH_R), 2000 * math.sin(TH_R)


def pol(theta, r):
    t = math.radians(theta)
    return r * math.cos(t), r * math.sin(t)


def dist_segmento(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def costa(theta):
    """Radio de la costa según el ángulo."""
    t = math.radians(theta)
    r = R_ISLA + 38 * math.sin(3 * t + 1.0) + 22 * math.sin(7 * t + 2.0) + 9 * math.sin(13 * t)
    dm = ((theta - 140 + 180) % 360) - 180                       # bahía de la marina
    return r - 110 * math.exp(-(dm / 11) ** 2)


def peso_acantilado(theta):
    """0 = playa, 1 = acantilado (costa norte y noreste), con transición suave de 12°."""
    th = theta % 360

    def rampa(a, b):
        return max(0.0, min(1.0, (a - b) / 12))
    w = min(rampa(th if th >= 180 else th + 360, 300), rampa(64, th if th < 180 else th - 360))
    cuello = max(0.0, min(1.0, (min(th, 360 - th) - 6) / 8))
    return w * cuello


def altura(x, y, ruido=None):
    """(altura en m, zona). `ruido(x, y)` opcional en [-1, 1] para el relieve fino (sólo el terreno lo usa)."""
    ruido = ruido or (lambda a, b: 0.0)
    r = math.hypot(x, y)
    theta = math.degrees(math.atan2(y, x)) % 360
    d = costa(theta) - r
    dh = min(dist_segmento(x, y, R_ISLA - 80, 0, HX, 0) - 70, math.hypot(x - HX, y) - 190)
    dr = min(dist_segmento(x, y, 1690 * math.cos(TH_R), 1690 * math.sin(TH_R), RX, RY) - 30, math.hypot(x - RX, y - RY) - 100)
    d = max(d, -dh, -dr)
    wa = peso_acantilado(theta) if r < 2100 else 0.0
    if d < 0:
        # Laguna somera de ~300 m (turquesa) y luego cae al azul profundo
        prof = (-d) * (0.035 + 0.06 * wa) + max(0.0, (-d) - 300) * 0.09
        return -min(44.0, prof) - 2.0 * wa, "mar"
    if d < 60:
        hp, zp = d / 60 * 1.8, "arena"
    elif d < 100:
        hp, zp = 1.8 + (d - 60) / 40 * (SUELO - 1.8), "pasto"
    else:
        hp, zp = SUELO, "pasto"
    ha = d * 1.5 if d < 8 else SUELO + 6 * math.exp(-(d - 8) / 40)
    h = hp * (1 - wa) + ha * wa
    zona = ("roca" if d < 30 else "pasto") if wa > 0.5 else zp
    # Penínsulas: rampa suave desde la arena (sin escalón) hasta 14 m (Horizonte) y 12 m (restaurante)
    if -dh > 0:
        tope = 14.0 if math.hypot(x - HX, y) < 260 else 10.0
        hp2 = min(tope, (-dh) * 0.22)
        if hp2 > h:
            h, zona = hp2, ("arena" if hp2 < 1.8 else "pasto")
    if -dr > 0:
        hp2 = min(12.0, (-dr) * 0.24)
        if hp2 > h:
            h, zona = hp2, ("arena" if hp2 < 1.8 else "pasto")
    dv = math.hypot(x - VOLCAN[0], y - VOLCAN[1])
    if dv < 700:
        hv = 414 * ((700 - dv) / 550) ** 1.25 if dv >= 150 else 414 - 84 * (1 - (dv / 150) ** 2)
        hv *= 1 + 0.07 * ruido(x * 0.004, y * 0.004)
        if hv + SUELO > h:
            h = hv + SUELO
            zona = "crater" if dv < 150 else ("volcan" if dv < 330 else "selva")
    if zona == "pasto" and d > 140 and dv > 720:
        h += 0.22 * ruido(x * 0.01, y * 0.01)
    return h, zona
