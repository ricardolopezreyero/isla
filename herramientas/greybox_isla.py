# RLR · Isla La Encantada — Ricardo López Reyero
# Plano del greybox (Fase B): genera data/greybox_isla.json con cada bloque de la isla a escala real.
# Unreal lo construye con herramientas/greybox_unreal.py (por el servidor MCP del editor).
#
# Convenciones (docs/04-unreal.md): 1 unidad de Unreal = 1 cm. Aquí todo va en METROS y se
# convierte al final. Norte = +X, Este = +Y. Ángulo θ en grados desde el norte hacia el este.
# Las figuras básicas de Unreal miden 1 m y tienen el pivote al centro, así que escala = metros.
# Uso: python3 herramientas/greybox_isla.py
import json
import math
from pathlib import Path

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent
SUELO = 6.0          # altura de la isla sobre el mar (m)
R_ISLA = 1750.0      # radio de la tierra: 3.5 km de diámetro (biblia: 3–4 km)
VOLCAN = (200.0, 150.0)

piezas = []


def pol(theta, r):
    t = math.radians(theta)
    return r * math.cos(t), r * math.sin(t)


def pieza(zona, nombre, forma, x, y, z, ancho, largo, alto, mat, yaw=0.0):
    """z = altura del CENTRO. ancho = eje X local, largo = eje Y local (m)."""
    piezas.append({"zona": zona, "nombre": nombre, "forma": forma, "x": round(x, 2), "y": round(y, 2),
                   "z": round(z, 2), "sx": round(ancho, 3), "sy": round(largo, 3), "sz": round(alto, 3),
                   "yaw": round(yaw, 2), "mat": mat})


def sobre(zona, nombre, forma, x, y, base, ancho, largo, alto, mat, yaw=0.0):
    """Igual que pieza() pero apoyada en `base` (m)."""
    pieza(zona, nombre, forma, x, y, base + alto / 2, ancho, largo, alto, mat, yaw)


def letrero(zona, texto, x, y, z, tam=60.0):
    piezas.append({"zona": zona, "nombre": "Letrero " + texto, "forma": "Texto", "texto": texto,
                   "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "tam": tam, "yaw": 180.0})


def tramo(zona, nombre, ax, ay, bx, by, ancho, base, alto, mat):
    """Bloque recto de A a B (caminos, cuellos de península, muelles)."""
    dx, dy = bx - ax, by - ay
    sobre(zona, nombre, "Cubo", (ax + bx) / 2, (ay + by) / 2, base, math.hypot(dx, dy), ancho, alto, mat,
          math.degrees(math.atan2(dy, dx)))


# ── Terreno ────────────────────────────────────────────────────────────────────────────────────
pieza("Terreno", "Mar", "Plano", 0, 0, 0, 16000, 16000, 1, "Mar")
pieza("Terreno", "Playa perimetral", "Cilindro", 0, 0, 0, 2 * (R_ISLA + 100), 2 * (R_ISLA + 100), 3, "Arena")
pieza("Terreno", "Isla", "Cilindro", 0, 0, 0, 2 * R_ISLA, 2 * R_ISLA, 2 * SUELO, "Pasto")
# Volcán: cono de 1.3 km de base y 420 m de alto; la cumbre oscura marca el cráter
sobre("Terreno", "Volcan", "Cono", *VOLCAN, SUELO, 1300, 1300, 420, "Volcan")
pieza("Terreno", "Crater", "Esfera", *VOLCAN, SUELO + 380, 320, 320, 80, "Crater")
letrero("Terreno", "VOLCÁN · CRÁTER", VOLCAN[0], VOLCAN[1], SUELO + 500, 70)

# Acantilados en la costa norte y noreste (rocas altas), dejando libre el cuello de Horizonte
for i, th in enumerate(list(range(300, 356, 4)) + list(range(8, 64, 4))):
    x, y = pol(th, R_ISLA - 5)
    alto = 18 + (i * 7) % 16
    sobre("Terreno", f"Acantilado {i + 1:02d}", "Cubo", x, y, 0, 38, 70, alto, "Roca", th + (i % 3 - 1) * 12)

# ── Caminos: anillo a 1.6 km del centro + ramales ────────────────────────────────────────────
R_ANILLO, SEG = 1600.0, 72
for i in range(SEG):
    th = i * 360 / SEG
    x, y = pol(th, R_ANILLO)
    sobre("Caminos", f"Anillo {i + 1:02d}", "Cubo", x, y, SUELO, 8, 2 * math.pi * R_ANILLO / SEG + 1, 0.3, "Camino", th)
for nombre, th, r1, r2 in [("Lobby", 180, 1030, 1600), ("Spa", 215, 1030, 1600), ("Restaurante", 250, 1600, 1750),
                           ("Marina", 140, 1600, 1760), ("Pista", 92, 1600, 1760), ("Staff", 20, 1380, 1600),
                           ("Horizonte", 0, 1600, 1720)]:
    tramo("Caminos", "Ramal " + nombre, *pol(th, r1), *pol(th, r2), 6, SUELO, 0.3, "Camino")

# ── Hotel: 800 habitaciones en 8 edificios de 100 (5 pisos × 20) frente a la playa sur ─────────
for i in range(8):
    th = 150 + i * 60 / 7
    x, y = pol(th, 1250)
    sobre("Hotel", f"Edificio {i + 1} · 100 habitaciones", "Cubo", x, y, SUELO, 20, 45, 17.5, "Hotel", th)
letrero("Hotel", "HOTEL · 800 HABITACIONES", *pol(180, 1250), 70, 45)
sobre("Hotel", "Lobby y recepción", "Cubo", *pol(180, 1000), SUELO, 40, 60, 12, "Lobby", 180)
letrero("Hotel", "LOBBY", *pol(180, 1000), 40, 30)
for i, th in enumerate((174, 180, 186)):
    nombres = ("Orillas del Mar", "Joya del Océano", "Gabinete de La Encantada")
    sobre("Hotel", "Tienda " + nombres[i], "Cubo", *pol(th, 900), SUELO, 14, 18, 6, "Tiendas", th)
letrero("Hotel", "TIENDAS", *pol(180, 900), 25, 25)
sobre("Hotel", "Alberca principal 50 m", "Cubo", *pol(180, 1430), SUELO - 0.6, 25, 50, 1.0, "Alberca", 180)
letrero("Hotel", "ALBERCA PRINCIPAL", *pol(180, 1430), 22, 25)
letrero("Hotel", "PLAYA PRINCIPAL", *pol(180, 1820), 12, 40)

# ── Spa & bienestar ──────────────────────────────────────────────────────────────────────────
sx, sy = pol(215, 1000)
sobre("Spa", "Spa principal", "Cubo", sx, sy, SUELO, 30, 40, 6, "Spa", 215)
for i in range(8):
    cx, cy = sx + 32 * math.cos(math.radians(i * 45)), sy + 32 * math.sin(math.radians(i * 45))
    sobre("Spa", f"Cabina {i + 1}", "Cubo", cx, cy, SUELO, 6, 6, 3.5, "Spa", i * 45)
letrero("Spa", "SPA", sx, sy, 40, 30)

# ── 80 villas: 40 al este y 40 al oeste, en dos filas, cada una con su alberca hacia el mar ─────
for lado, (t0, t1) in (("Este", (45, 135)), ("Oeste", (228, 312))):
    n = 0
    for r in (1080, 1420):
        for i in range(20):
            th = t0 + (t1 - t0) * i / 19
            n += 1
            x, y = pol(th, r)
            sobre("Villas", f"Villa {lado} {n:02d}", "Cubo", x, y, SUELO, 18, 26, 7, "Villa", th)
            px, py = pol(th, r + 17)
            sobre("Villas", f"Alberca villa {lado} {n:02d}", "Cubo", px, py, SUELO - 0.6, 5, 12, 1.0, "Alberca", th)
    letrero("Villas", f"VILLAS {lado.upper()} · 40", *pol((t0 + t1) / 2, 1250), 50, 45)

# ── Villa Horizonte: península norte, vista de 270° (docs/10) ────────────────────────────────
HX = 2120.0
tramo("Horizonte", "Cuello de la península", R_ISLA - 60, 0, HX - 150, 0, 140, 0, 10, "Pasto")
pieza("Horizonte", "Playa privada", "Cilindro", HX, 0, 0, 470, 470, 3, "Arena")
pieza("Horizonte", "Península", "Cilindro", HX, 0, 7, 380, 380, 14, "Pasto")
sobre("Horizonte", "Nivel 1 · playa y alberca", "Cubo", HX, 0, 14, 80, 110, 6, "Horizonte")
sobre("Horizonte", "Nivel 2 · sala monumental y comedor", "Cubo", HX + 4, 0, 20, 64, 92, 6, "Horizonte")
sobre("Horizonte", "Nivel 3 · suites y rooftop", "Cubo", HX + 8, 0, 26, 46, 70, 6, "Horizonte")
sobre("Horizonte", "Alberca infinita 40 m", "Cubo", HX - 20, -72, 14 - 0.6, 12, 40, 1.0, "Alberca")
pieza("Horizonte", "Jacuzzi 20 personas", "Cilindro", HX + 20, -78, 14.2, 10, 10, 1.0, "Alberca")
tramo("Horizonte", "Muelle privado", HX, 200, HX, 300, 8, 0, 1.5, "Muelle")
letrero("Horizonte", "VILLA HORIZONTE", HX, 0, 90, 45)

# ── Restaurante principal: península oeste-suroeste, todas las mesas al atardecer ──────────────
TH_R = 250
tramo("Restaurante", "Cuello de la península", *pol(TH_R, R_ISLA - 60), *pol(TH_R, 1920), 60, 0, 10, "Pasto")
rx, ry = pol(TH_R, 2000)
pieza("Restaurante", "Península", "Cilindro", rx, ry, 6, 200, 200, 12, "Pasto")
fx, fy = pol(TH_R, 2015)
pieza("Restaurante", "Restaurante · doble altura", "Cilindro", fx, fy, 12 + 4.5, 70, 70, 9, "Restaurante")
for i in range(3):
    tx, ty = pol(TH_R, 2050 + i * 9)
    sobre("Restaurante", f"Terraza {i + 1}", "Cubo", tx, ty, 12 - i * 2, 8, 60 - i * 8, 1, "Camino", TH_R)
tramo("Restaurante", "Muelle privado", *pol(TH_R, 2100), *pol(TH_R, 2170), 6, 0, 1.5, "Muelle")
letrero("Restaurante", "RESTAURANTE PRINCIPAL", rx, ry, 60, 35)

# ── Marina: bahía sureste con rompeolas y muelles ─────────────────────────────────────────────
mx, my = pol(140, 1960)
for i in range(9):
    a = 60 + i * 30
    bx, by = mx + 190 * math.cos(math.radians(a)), my + 190 * math.sin(math.radians(a))
    sobre("Marina", f"Rompeolas {i + 1}", "Cubo", bx, by, 0, 15, 70, 3, "Roca", a + 90)
for i in range(4):
    ax, ay = pol(140 - 6 + i * 4, 1770)
    bx, by = pol(140 - 6 + i * 4, 1900)
    tramo("Marina", f"Muelle {i + 1}", ax, ay, bx, by, 4, 0, 1.5, "Muelle")
    for j in range(2):
        yx, yy = pol(140 - 4 + i * 4, 1810 + j * 50)
        sobre("Marina", f"Yate {i * 2 + j + 1}", "Cubo", yx, yy, 0, 22, 6, 4, "Lobby", 140)
letrero("Marina", "MARINA", mx, my, 45, 40)

# ── Pista aérea: 2 km sobre el mar, al este ──────────────────────────────────────────────────
sobre("Pista", "Pista 2 km", "Cubo", -100, 2260, 0, 2000, 120, 5, "Pista")
tramo("Pista", "Calzada a la pista", -100, R_ISLA - 20, -100, 2200, 20, 0, 5, "Camino")
sobre("Pista", "Hangar", "Cubo", 700, 2290, 5, 60, 40, 15, "Staff")
letrero("Pista", "PISTA AÉREA · 2 KM", -100, 2260, 50, 45)

# ── Staff village: escondido detrás del volcán ───────────────────────────────────────────────
sx, sy = pol(20, 1350)
for i in range(6):
    sobre("Staff", f"Edificio staff {i + 1}", "Cubo", sx + (i % 3 - 1) * 45, sy + (i // 3 - 0.5) * 30, SUELO, 30, 15, 8, "Staff", 20)
letrero("Staff", "STAFF · OCULTO", sx, sy, 40, 30)

if __name__ == "__main__":
    salida = {
        "nivel": "/Game/Isla/Mapas/L_Isla",
        "unidades": "metros; norte = +X, este = +Y; z = centro de la pieza",
        "jugador": {"x": round(pol(180, 1520)[0], 1), "y": 0, "z": SUELO + 1.2, "yaw": 0},
        "sol": {"pitch": -12, "yaw": 70},
        "piezas": piezas,
    }
    (RAIZ / "data" / "greybox_isla.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    from collections import Counter
    print(len(piezas), "piezas ·", dict(Counter(p["zona"] for p in piezas)))
