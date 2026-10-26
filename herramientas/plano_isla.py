# RLR · Isla La Encantada — Ricardo López Reyero
# Plano v2 de la isla (Fase B → C): cada edificio, árbol, camastro y farol con su posición, giro y escala,
# apoyado a la altura exacta del terreno (herramientas/isla_geo.py). Escribe data/plano_isla.json.
# Lo construye en Unreal herramientas/construir_isla.py. Todo determinista: misma semilla, misma isla.
# Uso: python3 herramientas/plano_isla.py
import json
import math
import random
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isla_geo import HX, RX, RY, SUELO, TH_R, VOLCAN, altura, costa, peso_acantilado, pol

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent
OBJ = "/Game/Isla/Objetos/{0}.{0}"
rng = random.Random(181218)
piezas = []
ocupado = []                       # (x, y, radio) de edificios: la vegetación no se siembra encima


def suelo(x, y):
    return altura(x, y)[0]


def malla(zona, nombre, asset, x, y, z=None, yaw=0.0, escala=1.0, radio=0.0):
    z = suelo(x, y) if z is None else z
    piezas.append({"zona": zona, "nombre": nombre, "forma": "Malla", "asset": OBJ.format(asset),
                   "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "yaw": round(yaw, 1),
                   "sx": escala, "sy": escala, "sz": escala})
    if radio:
        ocupado.append((x, y, radio))


def bloque(zona, nombre, forma, x, y, z, sx, sy, sz, mat, yaw=0.0):
    """Figura básica de Unreal (cubo, cilindro, plano) con un material de la paleta. z = centro."""
    piezas.append({"zona": zona, "nombre": nombre, "forma": forma, "x": round(x, 2), "y": round(y, 2), "z": round(z, 2),
                   "sx": round(sx, 3), "sy": round(sy, 3), "sz": round(sz, 3), "yaw": round(yaw, 1), "mat": mat})


LETREROS = False      # los letreros flotantes ayudan a ubicarse en el editor pero estorban la vista; por omisión no van


def letrero(zona, texto, x, y, z, tam=60.0):
    if not LETREROS:
        return
    piezas.append({"zona": zona, "nombre": "Letrero " + texto, "forma": "Texto", "texto": texto,
                   "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "tam": tam, "yaw": 180.0})


def libre(x, y, margen=0.0):
    return all(math.hypot(x - ox, y - oy) > r + margen for ox, oy, r in ocupado)


CAMINOS = []


def camino(zona, nombre, puntos, ancho=6.0, paso=10.0, mat="Piedra", z_min=-99.0):
    """Camino a lo largo de una polilínea. Se vuelve UNA sola malla pegada al terreno (SM_Caminos, en Blender)."""
    CAMINOS.append({"nombre": nombre, "puntos": [[round(x, 2), round(y, 2)] for x, y in puntos],
                    "ancho": ancho, "mat": mat, "z_min": z_min})


# ── Terreno y mar ───────────────────────────────────────────────────────────────────────────
malla("Terreno", "Terreno de la isla", "SM_Terreno", 0, 0, 0)
bloque("Terreno", "Mar", "Plano", 0, 0, 0, 60000, 60000, 1, "Agua")
bloque("Terreno", "Fondo marino profundo", "Plano", 0, 0, -47, 60000, 60000, 1, "Abismo")
letrero("Terreno", "VOLCÁN · CRÁTER", VOLCAN[0], VOLCAN[1], 520, 70)

# ── Hotel: 8 edificios de 100 habitaciones, lobby, tiendas, suite de muestra, alberca y playa ──
for i in range(8):
    th = 150 + i * 60 / 7
    x, y = pol(th, 1250)
    malla("Hotel", f"Edificio {i + 1} · 100 habitaciones", "SM_EdificioHotel", x, y, SUELO, th, radio=30)
letrero("Hotel", "HOTEL · 800 HABITACIONES", *pol(180, 1250), 75, 45)
malla("Hotel", "Lobby y recepción", "SM_Lobby", *pol(180, 1000), SUELO, 180, radio=40)
letrero("Hotel", "LOBBY", *pol(180, 1000), 45, 30)
for th, nombre in ((174, "Orillas del Mar"), (180, "Joya del Océano"), (186, "Gabinete de La Encantada")):
    malla("Hotel", "Tienda " + nombre, "SM_Tienda", *pol(th, 900), SUELO, th, radio=14)
letrero("Hotel", "TIENDAS", *pol(180, 900), 25, 25)
malla("Hotel", "Suite de muestra · Suite Retorno 100", "SM_SuiteMuestra", *pol(166, 1010), SUELO, 166, radio=12)
letrero("Hotel", "SUITE DE MUESTRA", *pol(166, 1010), 20, 18)
ax, ay = pol(180, 1430)
malla("Hotel", "Alberca principal 50 m", "SM_AlbercaPrincipal", ax, ay, SUELO, 180, radio=34)
letrero("Hotel", "ALBERCA PRINCIPAL", ax, ay, 25, 25)

# ── Spa ─────────────────────────────────────────────────────────────────────────────────────
sx, sy = pol(215, 1000)
malla("Spa", "Spa principal", "SM_Spa", sx, sy, SUELO, 215, radio=28)
for i in range(8):
    a = math.radians(i * 45)
    cx, cy = sx + 38 * math.cos(a), sy + 38 * math.sin(a)
    malla("Spa", f"Cabina {i + 1}", "SM_CabinaSpa", cx, cy, SUELO, i * 45 + 180, radio=5)
letrero("Spa", "SPA", sx, sy, 40, 30)

# ── 80 villas (40 este, 40 oeste) ────────────────────────────────────────────────────────────
for lado, (t0, t1) in (("Este", (45, 135)), ("Oeste", (228, 312))):
    n = 0
    for r in (1080, 1420):
        for i in range(20):
            th = t0 + (t1 - t0) * i / 19
            n += 1
            malla("Villas", f"Villa {lado} {n:02d}", "SM_Villa", *pol(th, r), SUELO, th, radio=24)
    letrero("Villas", f"VILLAS {lado.upper()} · 40", *pol((t0 + t1) / 2, 1250), 50, 45)

# ── Villa Horizonte y restaurante principal ─────────────────────────────────────────────────
malla("Horizonte", "Villa Horizonte", "SM_VillaHorizonte", HX, 0, 14.0, 0, radio=190)
for k in range(10):
    malla("Horizonte", f"Muelle privado {k + 1}", "SM_MuelleTramo", HX - 5 + 0.0, 205 + k * 10, 0, 90)
malla("Horizonte", "Yate de Horizonte", "SM_Yate", HX + 25, 300, 0, 0)
letrero("Horizonte", "VILLA HORIZONTE", HX, 0, 95, 45)
malla("Restaurante", "Restaurante principal", "SM_Restaurante", *pol(250, 2015), 12.0, 250, radio=100)
for k in range(8):
    mx, my = pol(250, 2105 + k * 10)
    malla("Restaurante", f"Muelle privado {k + 1}", "SM_MuelleTramo", mx, my, 0, 250)
letrero("Restaurante", "RESTAURANTE PRINCIPAL", RX, RY, 65, 35)

# ── Marina, pista y staff ───────────────────────────────────────────────────────────────────
mx, my = pol(140, 1960)
rng_m = random.Random(140)                           # generador propio: no mueve la vegetación
for i in range(40):                                  # rompeolas continuo en arco
    a = math.radians(50 + i * 6)
    malla("Marina", f"Rompeolas {i + 1}", "SM_Roca_2", mx + 200 * math.cos(a), my + 200 * math.sin(a), -3.0, i * 37, rng_m.uniform(2.0, 2.6))
for i in range(4):
    th = 134 + i * 4
    for k in range(13):
        x, y = pol(th, costa(th) + 5 + k * 10)
        malla("Marina", f"Muelle {i + 1}·{k + 1}", "SM_MuelleTramo", x, y, 0, th)
    for j, e in enumerate((1.0, 0.55)):
        yx, yy = pol(th + 1.6, costa(th) + 50 + j * 55)
        malla("Marina", f"Yate {i * 2 + j + 1}", "SM_Yate", yx, yy, 0, th, e)
for j in range(2):
    hx, hy = pol(150 + j * 5, costa(150) + 140)
    malla("Marina", f"Hidroavión {j + 1}", "SM_Hidroavion", hx, hy, 0, 140)
cx, cy = pol(127, costa(127) - 32)
malla("Marina", "Club náutico", "SM_ClubNautico", cx, cy, None, 127, radio=22)
letrero("Marina", "MARINA", mx, my, 45, 40)
malla("Pista", "Pista 2 km", "SM_Pista", -100, 2260, 0, 0)
camino("Pista", "Calzada a la pista", [pol(92, 1600), (-100, costa(92) + 10), (-100, 2200)], 18, 10, "Concreto", 4.9)
malla("Pista", "Hangar", "SM_Hangar", 700, 2290, 5, 90)
malla("Pista", "Hidroavión en pista", "SM_Hidroavion", 300, 2250, 5, 0)
letrero("Pista", "PISTA AÉREA · 2 KM", -100, 2260, 50, 45)
stx, sty = pol(20, 1350)
for i in range(6):
    malla("Staff", f"Edificio staff {i + 1}", "SM_EdificioStaff", stx + (i % 3 - 1) * 45, sty + (i // 3 - 0.5) * 34, SUELO, 20, radio=18)
letrero("Staff", "STAFF · OCULTO", stx, sty, 40, 30)

# ── Caminos ─────────────────────────────────────────────────────────────────────────────────
camino("Caminos", "Anillo", [pol(i * 5, 1600) for i in range(73)], 8, 12)
for nombre, th, r1, r2 in (("Lobby", 180, 1035, 1600), ("Spa", 215, 1035, 1600), ("Restaurante", 250, 1600, 1950),
                           ("Marina", 140, 1600, 1660), ("Staff", 20, 1385, 1600), ("Horizonte", 0, 1600, 1950)):
    camino("Caminos", "Ramal " + nombre, [pol(th, r1), pol(th, r2)], 6, 10)
mvx, mvy = VOLCAN[0] - 172 * 0.94, VOLCAN[1] - 172 * 0.34
malla("Terreno", "Mirador del cráter", "SM_MiradorCrater", mvx, mvy, suelo(mvx, mvy) + 0.4, 20, radio=9)
letrero("Terreno", "MIRADOR DEL CRÁTER", mvx, mvy, suelo(mvx, mvy) + 30, 12)
camino("Caminos", "Sendero al cráter", [pol(240, 900), (VOLCAN[0] - 380, VOLCAN[1] - 300), (VOLCAN[0] - 160, VOLCAN[1] - 60)], 3, 5, "Roca")
for i in range(0, 360, 6):                           # faroles a lo largo del anillo, luz cálida
    x, y = pol(i + 3, 1606)
    malla("Caminos", f"Farol {i // 6 + 1}", "SM_Farol", x, y, None, i)

malla("Caminos", "Red de caminos", "SM_Caminos", 0, 0, 0)

# ── Vegetación ──────────────────────────────────────────────────────────────────────────────
PALMAS = ["SM_PalmaCocotera_1", "SM_PalmaCocotera_2", "SM_PalmaCocotera_3", "SM_PalmaCocotera_4"]
n = 0
th = 0.0
while th < 360:                                      # palmas de costa sobre la arena
    w = peso_acantilado(th)
    marina = abs(((th - 140 + 180) % 360) - 180) < 12
    if w < 0.4 and not marina:
        r = costa(th) - rng.uniform(22, 55)
        x, y = pol(th, r)
        if libre(x, y, 4):
            n += 1
            malla("Vegetacion", f"Palma costa {n:03d}", rng.choice(PALMAS), x, y, None, rng.uniform(0, 360), rng.uniform(0.85, 1.15))
    th += rng.uniform(0.6, 1.1)
for i in range(0, 360, 4):                           # palmas reales flanqueando el anillo
    for s in (-1, 1):
        x, y = pol(i + (1 if s > 0 else 3), 1600 + s * 12)
        if libre(x, y, 3):
            malla("Vegetacion", f"Palma real anillo {i}{'a' if s > 0 else 'b'}", "SM_PalmaReal_" + ("1" if s > 0 else "2"), x, y, None, rng.uniform(0, 360))
k = 0
while k < 70:                                        # almendros y ceibas tierra adentro
    th, r = rng.uniform(0, 360), rng.uniform(760, 1520)
    x, y = pol(th, r)
    if math.hypot(x - VOLCAN[0], y - VOLCAN[1]) > 720 and libre(x, y, 12):
        k += 1
        asset = "SM_Ceiba_1" if k % 9 == 0 else "SM_Almendro_1"
        malla("Vegetacion", f"Árbol {k:02d}", asset, x, y, None, rng.uniform(0, 360), rng.uniform(0.85, 1.2))
        ocupado.append((x, y, 6))
k = 0
while k < 160:                                       # selva en las faldas del volcán
    a, d = rng.uniform(0, 2 * math.pi), rng.uniform(420, 700)
    x, y = VOLCAN[0] + d * math.cos(a), VOLCAN[1] + d * math.sin(a)
    if libre(x, y, 8):
        k += 1
        asset = rng.choice(["SM_Almendro_1", "SM_PalmaReal_1", "SM_PalmaCocotera_3", "SM_Almendro_1"])
        malla("Vegetacion", f"Selva {k:03d}", asset, x, y, suelo(x, y) - 0.5, rng.uniform(0, 360), rng.uniform(0.9, 1.3))
FLORES = ["SM_Buganvilia", "SM_Hibisco", "SM_Plumeria"]
for i in range(8):                                   # jardines con flor frente a cada edificio del hotel
    th = 150 + i * 60 / 7
    for j in range(5):
        x, y = pol(th - 0.6 + j * 0.3, 1286)
        malla("Vegetacion", f"Flores hotel {i + 1}·{j + 1}", FLORES[(i + j) % 3], x, y, SUELO, rng.uniform(0, 360))
for j in range(14):                                  # flores en el acceso al lobby
    x, y = pol(180 + (j % 2 * 2 - 1) * 1.6, 1040 + (j // 2) * 18)
    malla("Vegetacion", f"Flores lobby {j + 1}", FLORES[j % 3], x, y, SUELO, rng.uniform(0, 360), 1.3)
for i, th in enumerate(range(304, 360, 3)):          # rocas al pie de los acantilados
    x, y = pol(th, costa(th) + 6)
    malla("Terreno", f"Roca acantilado {i + 1}", rng.choice(["SM_Roca_1", "SM_Roca_2", "SM_Roca_3"]), x, y, -1.5, rng.uniform(0, 360), rng.uniform(0.8, 1.6))
for i, th in enumerate(range(9, 64, 3)):
    x, y = pol(th, costa(th) + 6)
    malla("Terreno", f"Roca acantilado este {i + 1}", rng.choice(["SM_Roca_1", "SM_Roca_2", "SM_Roca_3"]), x, y, -1.5, rng.uniform(0, 360), rng.uniform(0.8, 1.6))

# ── Jardines: pasto de duna, agaves en acantilados y plantas tropicales junto a villas, lobby y spa ──
n = 0
th = 0.0
while th < 360:
    w = peso_acantilado(th)
    marina = abs(((th - 140 + 180) % 360) - 180) < 12
    if not marina:
        if w < 0.4:
            x, y = pol(th, costa(th) - rng.uniform(58, 72))
            if libre(x, y, 3):
                n += 1
                malla("Jardines", f"Pasto de duna {n:03d}", "SM_PastoPlaya", x, y, None, rng.uniform(0, 360), rng.uniform(1.0, 1.8))
        elif rng.random() < 0.5:
            x, y = pol(th, costa(th) - rng.uniform(14, 40))
            if libre(x, y, 3):
                n += 1
                malla("Jardines", f"Agave {n:03d}", "SM_Agave", x, y, None, rng.uniform(0, 360), rng.uniform(0.9, 1.6))
    th += rng.uniform(1.6, 2.4)
TROPICALES = ["SM_Heliconia", "SM_Helecho", "SM_Platanera"]
for lado, (t0, t1) in (("Este", (45, 135)), ("Oeste", (228, 312))):
    for r in (1080, 1420):
        for i in range(20):
            th = t0 + (t1 - t0) * i / 19
            for s_ in (-1, 1):
                x, y = pol(th + s_ * 0.95, r - 6)
                malla("Jardines", f"Jardín villa {lado} {r} {i}{'a' if s_ > 0 else 'b'}", TROPICALES[(i + (s_ > 0)) % 3], x, y, SUELO, rng.uniform(0, 360))
for j in range(12):
    a = math.radians(j * 30)
    lx, ly = pol(180, 1000)
    malla("Jardines", f"Jardín lobby {j + 1}", TROPICALES[j % 3], lx + 46 * math.cos(a), ly + 46 * math.sin(a), SUELO, j * 30, 1.2)
    sx2, sy2 = pol(215, 1000)
    malla("Jardines", f"Jardín spa {j + 1}", TROPICALES[(j + 1) % 3], sx2 + 52 * math.cos(a), sy2 + 52 * math.sin(a), SUELO, j * 30)

# ── Playa principal: camastros, sombrillas de palma, palapas y kayaks ───────────────────────
n = 0
for th10 in range(1655, 1950, 18):
    th = th10 / 10
    r = costa(th) - 28
    for s in (-1, 1):
        x, y = pol(th + s * 0.18, r)
        n += 1
        malla("Playa", f"Camastro playa {n:03d}", "SM_Camastro", x, y, None, th + 180)
    x, y = pol(th, r + 2)
    malla("Playa", f"Sombrilla playa {th10}", "SM_SombrillaPalma", x, y, None, rng.uniform(0, 360))
for k, th in enumerate((158, 202, 70, 110, 250 - 12, 290)):
    x, y = pol(th, costa(th) - 30)
    malla("Playa", f"Palapa {k + 1}", "SM_Palapa", x, y, None, th + 180)
for k in range(8):
    x, y = pol(176 + k, costa(176 + k) - 6)
    malla("Playa", f"Kayak {k + 1}", "SM_Kayak", x, y, None, 176 + k + 90)
bx, by = pol(172, costa(172) - 48)
malla("Playa", "Bar de playa", "SM_BarPlaya", bx, by, None, 172, radio=10)
for k, th in enumerate((95, 285)):                    # un bar de playa para cada lado de villas
    bx, by = pol(th, costa(th) - 48)
    malla("Playa", f"Bar de playa villas {k + 1}", "SM_BarPlaya", bx, by, None, th, radio=10)
letrero("Playa", "PLAYA PRINCIPAL", *pol(180, costa(180) - 30), 25, 40)

if __name__ == "__main__":
    salida = {"nivel": "/Game/Isla/Mapas/L_Isla", "version": 2,
              "jugador": {"x": round(pol(180, 1520)[0], 1), "y": 0, "z": SUELO + 1.2, "yaw": 0},
              "sol": {"pitch": -14, "yaw": 70}, "caminos": CAMINOS, "piezas": piezas}
    (RAIZ / "data" / "plano_isla.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(piezas), "piezas ·", dict(Counter(p["zona"] for p in piezas)))
