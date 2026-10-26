# RLR · Isla La Encantada — Ricardo López Reyero
# Arquitectura hecha en casa. Cada edificio se modela en coordenadas LOCALES:
#   +X = hacia el mar (fachada principal) · Y = a lo largo · Z = arriba · origen al centro, al nivel del piso.
# En Unreal se coloca con yaw = θ (el ángulo de su lugar en la isla), así la fachada siempre ve al mar.
# Ojo: Blender usa y_b = -y de Unreal; Y() lo convierte para piezas asimétricas.
import math

import bmesh
import bpy

from comun import asignar, caja, cilindro, copiar, esfera, mover, suave, unir
import muebles
import naturaleza

_RLR = "Ricardo López Reyero"


def Y(y):
    return -y


def sector(nombre, r_in, r_out, a0, a1, z0, z1, mat, pasos=24):
    """Sector de anillo (para el restaurante en abanico y terrazas curvas). Ángulos en grados desde +X."""
    bm = bmesh.new()
    capas = []
    for z in (z0, z1):
        fila = []
        for i in range(pasos + 1):
            a = math.radians(a0 + (a1 - a0) * i / pasos)
            fila.append((bm.verts.new((r_in * math.cos(a), r_in * math.sin(a), z)),
                         bm.verts.new((r_out * math.cos(a), r_out * math.sin(a), z))))
        capas.append(fila)
    abajo, arriba = capas
    for i in range(pasos):
        bm.faces.new((arriba[i][0], arriba[i][1], arriba[i + 1][1], arriba[i + 1][0]))
        bm.faces.new((abajo[i][0], abajo[i + 1][0], abajo[i + 1][1], abajo[i][1]))
        bm.faces.new((abajo[i][1], abajo[i + 1][1], arriba[i + 1][1], arriba[i][1]))
        if r_in > 0:
            bm.faces.new((abajo[i][0], arriba[i][0], arriba[i + 1][0], abajo[i + 1][0]))
    for j in (0, pasos):
        bm.faces.new((abajo[j][0], abajo[j][1], arriba[j][1], arriba[j][0]))
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.collection.objects.link(o)
    me.validate()
    return asignar(o, mat)


def colocar(o, x, y, z, rot_grados=0.0):
    """Coloca un objeto de biblioteca (Y en convención Unreal)."""
    return mover(o, x, Y(y), z, math.radians(-rot_grados))


def alberca(nombre, x, y, z, largo_x, ancho_y, borde=0.4):
    """Alberca: espejo de agua turquesa con borde de piedra (la superficie queda en z)."""
    return [caja(nombre + "_agua", x, Y(y), z - 0.05, largo_x, ancho_y, 0.1, "AguaAlberca"),
            caja(nombre + "_fondo", x, Y(y), z - 0.8, largo_x, ancho_y, 0.1, "Mosaico"),
            caja(nombre + "_b1", x + largo_x / 2 + borde / 2, Y(y), z - 0.35, borde, ancho_y + 2 * borde, 0.8, "Piedra"),
            caja(nombre + "_b2", x - largo_x / 2 - borde / 2, Y(y), z - 0.35, borde, ancho_y + 2 * borde, 0.8, "Piedra"),
            caja(nombre + "_b3", x, Y(y + ancho_y / 2 + borde / 2), z - 0.35, largo_x, borde, 0.8, "Piedra"),
            caja(nombre + "_b4", x, Y(y - ancho_y / 2 - borde / 2), z - 0.35, largo_x, borde, 0.8, "Piedra")]


# ── Hotel: edificio de 100 habitaciones (5 pisos × 20, 10 por lado), 45 × 20 × 17.5 m ─────────
def edificio_hotel():
    p = []
    PISO, N = 3.5, 5
    for f in range(N + 1):
        z = f * PISO
        p.append(caja(f"losa{f}", 0, 0, z + 0.15, 24.0 if f else 20.0, 45.0, 0.3, "Estuco"))
    for f in range(N):
        z = f * PISO
        p.append(caja(f"vidrio{f}", 0, 0, z + 0.3 + 1.55, 15.6, 44.4, 3.1, "Vidrio"))
        if f == 0:
            continue
        for s in (-1, 1):
            p.append(caja(f"pasamanos{f}{s}", s * 11.95, 0, z + 1.38, 0.08, 45.0, 0.06, "MaderaOscura"))
            p.append(caja(f"zoclo{f}{s}", s * 11.95, 0, z + 0.36, 0.08, 45.0, 0.12, "Metal"))
            for k in range(31):
                p.append(caja(f"balaustre{f}{s}{k}", s * 11.95, -22.5 + k * 1.5, z + 0.85, 0.04, 0.04, 1.0, "Metal"))
            for i in range(10):
                y = -22.5 + 4.5 * i + 2.25
                p.append(muebles_mini(s * 10.2, y, z + 0.3))
    for s in (-1, 1):
        for i in range(11):
            y = -22.5 + 4.5 * i
            p.append(caja(f"aleta{s}{i}", s * 10.0, y, N * PISO / 2 + 0.15, 4.0, 0.25, N * PISO, "Estuco"))
    for s in (-1, 1):
        p.append(caja(f"testero{s}", 0, s * 22.7, N * PISO / 2, 20.0, 0.6, N * PISO + 0.3, "EstucoArena"))
    # Planta baja: columnas y lobby de vidrio, techo verde y pérgola en la azotea
    for i in range(6):
        p.append(cilindro(f"col{i}", 9.6, -20 + 8 * i, PISO / 2, 0.3, PISO, "Estuco", 12))
    p.append(caja("azotea_jardin", -4, 0, N * PISO + 0.45, 10, 40, 0.3, "Pasto"))
    for i in range(9):
        p.append(caja(f"pergola{i}", 4, -20 + 5 * i, N * PISO + 3.0, 10, 0.2, 0.3, "Madera"))
    for x in (-0.5, 8.5):
        for y in (-20, 0, 20):
            p.append(cilindro("poste", x, y, N * PISO + 1.6, 0.12, 2.8, "Madera", 8))
    for s in (-1, 1):
        p.append(caja(f"pretil_x{s}", s * 12.0, 0, N * PISO + 0.6, 0.25, 45.0, 0.6, "Estuco"))
    return unir(p, "SM_EdificioHotel")


def muebles_mini(x, y, z):
    """Mesita y dos sillas de balcón (se ven desde fuera, dan vida a la fachada)."""
    return unir([cilindro("mesa", x, y, z + 0.37, 0.3, 0.04, "Madera", 12),
                 caja("s1", x, y - 0.6, z + 0.25, 0.5, 0.5, 0.5, "TelaArena", bisel=0.05),
                 caja("s2", x, y + 0.6, z + 0.25, 0.5, 0.5, 0.5, "TelaArena", bisel=0.05)], "balcon")


# ── Villa de lujo (5 recámaras, hasta 12 personas): 26 × 18 m, dos niveles, terraza y alberca ────
def villa():
    p = [caja("zocalo", 0, 0, 0.3, 18, 26, 0.6, "Piedra"),
         caja("deck", 15.5, 0, 0.55, 13, 26, 0.1, "MaderaClara")]
    # Nivel 1: caja de vidrio con muros de estuco en los extremos y el fondo
    p.append(caja("vidrio1", 0.5, 0, 2.3, 13, 22, 3.4, "Vidrio"))
    p.append(caja("muro_fondo", -8.6, 0, 2.3, 0.4, 26, 3.4, "Estuco"))
    for s in (-1, 1):
        p.append(caja("muro_lado", -1.5, s * 12.6, 2.3, 14.5, 0.6, 3.4, "Estuco"))
    p.append(caja("techo1", 1.5, 0, 4.15, 21, 27.5, 0.4, "Estuco"))
    p.append(caja("techo1_madera", 1.5, 0, 3.92, 20.6, 27.1, 0.06, "Madera"))
    # Nivel 2: volumen de estuco con frente de vidrio y celosía de madera
    p.append(caja("nivel2", -2.5, Y(4), 5.95, 10, 15, 3.2, "EstucoArena"))
    p.append(caja("vidrio2", 2.55, Y(4), 5.95, 0.1, 13.5, 2.9, "Vidrio"))
    for i in range(16):
        p.append(caja(f"celosia{i}", 3.1, Y(4 - 7 + i * 0.95), 5.95, 0.1, 0.12, 3.0, "Madera"))
    p.append(caja("techo2", -2, Y(4), 7.75, 13, 17, 0.35, "Estuco"))
    # Terraza: alberca 12 × 5, camastros, sombrilla, comedor exterior
    p += alberca("alberca", 15.5, -5, 0.6, 5, 12)
    for k in range(3):
        p.append(colocar(muebles.camastro(), 15.8, 4.5 + k * 1.1, 0.6, 90))
    p.append(colocar(muebles.sombrilla_tela(), 19, 6, 0.6))
    p.append(colocar(muebles.mesa_comedor(4), 11, 8, 0.6, 90))
    # Interior visible a través del vidrio: sala, comedor para 10 y recámara principal arriba
    p.append(caja("piso_int", 0.5, 0, 0.62, 13, 22, 0.04, "MaderaClara"))
    p.append(colocar(muebles.sofa3(), 3.5, -6, 0.64, 180))
    p.append(colocar(muebles.sofa3(), -1.5, -6, 0.64, 0))
    p.append(caja("alfombra", 1, Y(-6), 0.65, 4.5, 5.5, 0.02, "TelaArena"))
    p.append(caja("mesa_centro", 1, Y(-6), 0.95, 1.2, 2.0, 0.06, "MaderaOscura"))
    for k in range(2):
        p.append(colocar(muebles.mesa_comedor(4), 1 + k * 0.0, 3.5 + k * 3.3, 0.64, 90))
    p.append(caja("cocina_isla", -5.5, Y(6), 1.1, 1.2, 4.5, 0.95, "Marmol"))
    p.append(caja("cocina_muro", -7.9, Y(6), 1.6, 0.6, 6.0, 1.9, "MaderaOscura"))
    p.append(colocar(muebles.cama_king(), -2.5, 4, 4.36, 0))
    p.append(colocar(muebles.sofa3(), 0.8, 9.5, 4.36, 180))
    # Jardín: dos palmas y buganvilias
    p.append(colocar(naturaleza.palma_cocotera(semilla=7, alto=11, inclinacion=2.5), 20.5, -11, 0))
    p.append(colocar(naturaleza.palma_cocotera(semilla=8, alto=13, inclinacion=1.5), 21.5, 11.5, 0))
    p.append(colocar(naturaleza.arbusto_flor(semilla=3, flor="Flor"), -9.5, -13, 0))
    p.append(colocar(naturaleza.arbusto_flor(semilla=4, flor="FlorBlanca"), -9.5, 13, 0))
    return unir(p, "SM_Villa")


# ── Villa Horizonte: 25 suites, hasta 60 personas, tres niveles escalonados (docs/10) ──────────
def villa_horizonte():
    p = []
    niveles = [(80, 110, 0, "Estuco"), (64, 92, 6, "EstucoArena"), (46, 70, 12, "Estuco")]
    for i, (lx, ly, z, mat) in enumerate(niveles):
        dx = i * 4
        p.append(caja(f"losa{i}", dx, 0, z + 0.2, lx + 6, ly + 6, 0.4, "Piedra" if i == 0 else "Estuco"))
        p.append(caja(f"vidrio{i}", dx, 0, z + 3.2, lx - 2, ly - 2, 5.6, "Vidrio"))
        for s in (-1, 1):
            p.append(caja(f"muro{i}{s}", dx, s * (ly / 2 - 0.5), z + 3.2, lx - 2, 1.0, 5.6, mat))
        n_col = int(ly / 8)
        for k in range(n_col + 1):
            y = -ly / 2 + k * ly / n_col
            p.append(cilindro(f"col{i}{k}", dx + lx / 2 + 1.5, y, z + 3.2, 0.35, 5.6, "Piedra", 12))
        p.append(caja(f"barandal{i}", dx + lx / 2 + 2.9, 0, z + 1.0, 0.06, ly + 5, 1.1, "Vidrio"))
    p.append(caja("techo", 8, 0, 18.4, 52, 76, 0.5, "Estuco"))
    # Lobby monumental de doble altura (8–9 m) al centro del frente
    p.append(caja("lobby_vidrio", 41.5, 0, 6.2, 1.0, 22, 12, "Vidrio"))
    p.append(caja("lobby_marco", 41.6, 0, 12.4, 1.6, 24, 0.6, "Laton"))
    # Rooftop con pérgola, alberca chica y lounge
    for k in range(12):
        p.append(caja(f"pergola{k}", 8, -30 + k * 5.5, 21.6, 30, 0.25, 0.35, "Madera"))
    for x in (-6, 22):
        for y in (-30, 0, 30):
            p.append(cilindro("poste", x, y, 20.0, 0.18, 3.2, "Madera", 10))
    p += alberca("rooftop", 20, 20, 18.7, 6, 14)
    # Alberca infinita de 40 m al oeste, jacuzzi para 20 y bar en la alberca
    p += alberca("infinita", -20, -72, 0.1, 12, 40)
    p.append(cilindro("jacuzzi_agua", 20, Y(-78), 0.05, 5, 0.1, "AguaAlberca", 32))
    p.append(cilindro("jacuzzi_borde", 20, Y(-78), -0.3, 5.5, 0.8, "Piedra", 32))
    p.append(colocar(muebles.barra_bar(8), -10, -88, 0.0, 90))
    for k in range(10):
        p.append(colocar(muebles.camastro(), -12 + (k % 5) * 2.2, -58 - (k // 5) * 4, 0.0, 90))
    for k in range(4):
        p.append(colocar(muebles.sombrilla_tela(), -11 + k * 3, -64, 0.0))
    # Jardín: anillo de palmas reales y almendros alrededor de la villa
    for k in range(16):
        a = 2 * math.pi * k / 16
        x, y = 150 * math.cos(a), 150 * math.sin(a)
        if -0.6 < math.atan2(y, x) < 0.6 and abs(y) < 40:
            continue
        o = naturaleza.palma_real(semilla=k) if k % 2 else naturaleza.palma_cocotera(semilla=20 + k, alto=15)
        p.append(colocar(o, x, y, 0))
    for k, (x, y) in enumerate(((-60, 70), (60, 80), (-70, -110), (90, -40))):
        p.append(colocar(naturaleza.almendro(semilla=k + 1), x, y, 0))
    for k in range(10):
        p.append(colocar(naturaleza.arbusto_flor(semilla=30 + k, flor="Flor" if k % 2 else "FlorRoja"), -48 + k * 10, 62, 0))
    # Mesa de gala para 60 en la punta de la península
    p.append(caja("mesa_gala", 125, 0, 0.74, 3, 40, 0.06, "Tela"))
    for s in (-1, 1):
        for k in range(30):
            p.append(muebles.silla(125 + s * 1.9, Y(-19.5 + k * 1.35), 0 if s < 0 else 180))
    return unir(p, "SM_VillaHorizonte")


# ── Restaurante principal: abanico abierto al atardecer, doble altura, terrazas (biblia 02) ───
def restaurante():
    p = [sector("piso", 0, 34, -80, 80, 0, 0.4, "MaderaClara"),
         caja("muro_fondo", -0.6, 0, 4.7, 1.2, 68, 8.6, "Piedra"),
         sector("vidrio", 33.6, 34, -80, 80, 0.4, 9.0, "Vidrio"),
         sector("techo", 0, 39, -86, 86, 9.0, 9.6, "Madera"),
         sector("techo_borde", 38.5, 39.2, -86, 86, 8.6, 9.6, "MaderaOscura")]
    p.append(caja("cocina", -9, 0, 4.7, 16, 30, 9.0, "Piedra"))
    p.append(caja("cocina_techo", -9, 0, 9.3, 17, 31, 0.4, "Madera"))
    for i, r in enumerate((40, 46, 52)):
        p.append(sector(f"terraza{i}", r - 6, r, -70, 70, -1.2 * (i + 1), -1.2 * (i + 1) + 0.4, "Piedra"))
        n = 8 + i * 2
        for k in range(n):
            a = math.radians(-60 + 120 * k / (n - 1))
            p.append(colocar(muebles.mesa_restaurante(), (r - 3) * math.cos(a), -(r - 3) * math.sin(a), -1.2 * (i + 1) + 0.4))
    for k in range(18):
        a = math.radians(-65 + 130 * k / 17)
        for anillo in (14, 24):
            p.append(colocar(muebles.mesa_restaurante(), anillo * math.cos(a), -anillo * math.sin(a), 0.4))
    p.append(colocar(muebles.barra_bar(10), 4, 0, 0.4))
    p.append(caja("espejo_agua", 28, 0, 0.45, 2, 50, 0.1, "Agua"))
    return unir(p, "SM_Restaurante")


# ── Lobby: gran pabellón abierto con techo de palma a cuatro aguas ──────────────────────────
def lobby():
    p = [caja("plataforma", 0, 0, 0.4, 40, 60, 0.8, "Piedra")]
    for x in (-16, -8, 0, 8, 16):
        for y in (-26, -13, 0, 13, 26):
            p.append(cilindro("col", x, y, 4.8, 0.45, 8.0, "MaderaOscura", 12))
    techo = cilindro("techo", 0, 0, 12.5, 40, 8.0, "Paja", 4, radio_arriba=2.0)
    techo.rotation_euler = (0, 0, math.radians(45))
    techo.scale = (0.85, 1.25, 1)
    p.append(techo)
    p.append(caja("recepcion", -10, 0, 1.35, 2.5, 12, 1.1, "Marmol", bisel=0.05))
    p += alberca("espejo", 14, 0, 0.9, 8, 40, 0.5)
    for y in (-18, 18):
        p.append(colocar(muebles.sofa3(), -2, y, 0.8, 0))
        p.append(colocar(muebles.sofa3(), 2, y, 0.8, 180))
    return unir(p, "SM_Lobby")


def tienda(color="TelaTerracota"):
    p = [caja("base", 0, 0, 0.2, 14, 18, 0.4, "Piedra"),
         caja("vidrio", 0.5, 0, 2.4, 11, 16, 4.0, "Vidrio"),
         caja("fondo", -6.3, 0, 2.4, 1.0, 18, 4.0, "Estuco"),
         caja("techo", 0.6, 0, 4.6, 15.5, 19, 0.4, "Madera")]
    for i in range(8):
        lona = caja(f"toldo{i}", 7.6, -7 + i * 2, 4.1, 2.2, 1.8, 0.05, color if i % 2 else "Tela")
        lona.rotation_euler = (0, math.radians(18), 0)
        p.append(lona)
    return unir(p, "SM_Tienda")


def cabina_spa():
    p = [caja("base", 0, 0, 0.15, 6, 6, 0.3, "MaderaClara"),
         caja("muros", -0.5, 0, 1.75, 4.5, 5.2, 2.9, "EstucoArena"),
         caja("vidrio", 1.8, 0, 1.75, 0.08, 5.0, 2.8, "Vidrio")]
    techo = cilindro("techo", 0, 0, 4.0, 5.0, 1.8, "Paja", 4, radio_arriba=0.1)
    techo.rotation_euler = (0, 0, math.radians(45))
    p.append(techo)
    return unir(p, "SM_CabinaSpa")


def spa():
    p = [caja("plataforma", 0, 0, 0.3, 30, 40, 0.6, "Piedra"),
         caja("volumen", -4, 0, 3.0, 20, 36, 4.8, "EstucoArena"),
         caja("vidrio", 6.1, 0, 3.0, 0.1, 34, 4.6, "Vidrio"),
         caja("techo", 0, 0, 5.6, 32, 42, 0.5, "Madera")]
    p += alberca("tina_termal", 11, 0, 0.6, 6, 18)
    for k in range(6):
        p.append(colocar(naturaleza.arbusto_flor(semilla=50 + k, flor="FlorBlanca"), 13, -16 + k * 6.4, 0.6))
    return unir(p, "SM_Spa")


def edificio_staff():
    p = [caja("cuerpo", 0, 0, 4, 15, 30, 8, "Concreto")]
    for f in range(2):
        for s in (-1, 1):
            p.append(caja(f"ventanas{f}{s}", s * 7.55, 0, 2.2 + f * 3.6, 0.1, 27, 1.4, "Vidrio"))
    p.append(caja("techo", 0, 0, 8.15, 15.6, 30.6, 0.3, "PiedraOscura"))
    return unir(p, "SM_EdificioStaff")


# ── Mar: muelle, yate, hidroavión, pista ────────────────────────────────────────────────────
def muelle_tramo(largo=10.0, ancho=4.0):
    """Tramo de muelle de madera sobre pilotes, a lo largo de X; el piso queda a 1.5 m."""
    p = []
    n = int(largo / 0.3)
    for i in range(n):
        p.append(caja(f"tabla{i}", -largo / 2 + 0.15 + i * 0.3, 0, 1.45, 0.26, ancho, 0.08, "MaderaClara"))
    for x in (-largo / 2 + 0.3, largo / 2 - 0.3):
        for y in (-ancho / 2 + 0.2, ancho / 2 - 0.2):
            p.append(cilindro("pilote", x, y, -0.5, 0.15, 4.0, "Madera", 8))
    for s in (-1, 1):
        p.append(caja("viga", 0, s * (ancho / 2 - 0.2), 1.3, largo, 0.15, 0.2, "Madera"))
    return unir(p, "SM_MuelleTramo")


def yate():
    """Súper yate de 40 m: casco blanco, tres cubiertas y ventanales oscuros."""
    bm = bmesh.new()
    secc = []
    for i in range(13):
        t = i / 12
        x = -20 + 40 * t
        w = 4.2 * (1 - max(0, t - 0.55) ** 1.6 * 2.2) if t > 0.55 else 4.2
        w = max(w, 0.15)
        z0 = -1.8 + 1.2 * max(0, t - 0.7) * 3
        fila = [bm.verts.new((x, -w, 2.2)), bm.verts.new((x, -w * 0.85, z0 + 0.6)), bm.verts.new((x, 0, z0)),
                bm.verts.new((x, w * 0.85, z0 + 0.6)), bm.verts.new((x, w, 2.2))]
        secc.append(fila)
    for i in range(12):
        for k in range(4):
            bm.faces.new((secc[i][k], secc[i + 1][k], secc[i + 1][k + 1], secc[i][k + 1]))
    bm.faces.new([secc[0][k] for k in range(5)])
    bm.faces.new([secc[-1][k] for k in reversed(range(5))])
    tapa = [v for f in secc for v in (f[0], f[4])]
    me = bpy.data.meshes.new("casco")
    bm.to_mesh(me)
    bm.free()
    casco = bpy.data.objects.new("casco", me)
    bpy.context.collection.objects.link(casco)
    asignar(casco, "Casco")
    p = [casco, caja("cubierta", -1, 0, 2.25, 38, 8.2, 0.1, "MaderaClara")]
    for i, (lx, ly, x) in enumerate(((24, 7, -4), (17, 6.2, -5), (9, 5, -6))):
        z = 2.3 + i * 2.6
        p.append(caja(f"piso{i}", x, 0, z + 1.2, lx, ly, 2.4, "Casco", bisel=0.3))
        p.append(caja(f"ventana{i}", x, 0, z + 1.3, lx + 0.05, ly + 0.05, 0.9, "Vidrio"))
    p.append(cilindro("radar", -7, 0, 10.6, 0.15, 2.0, "Metal", 8))
    return unir(p, "SM_Yate")


def hidroavion():
    p = [esfera("fuselaje", 0, 0, 2.6, 6.0, 0.8, 0.9, "Pintura", 3),
         caja("ala", 0.8, 0, 3.5, 1.6, 15, 0.15, "Pintura"),
         caja("timon", -5.4, 0, 3.6, 1.2, 0.1, 1.6, "TelaAzul"),
         caja("estab", -5.5, 0, 2.9, 1.0, 4.0, 0.1, "Pintura"),
         cilindro("helice", 6.1, 0, 2.6, 1.0, 0.05, "MetalOscuro", 3, rot=(0, math.radians(90), 0))]
    for s in (-1, 1):
        p.append(esfera("flotador", 0.5, s * 1.8, 0.4, 4.0, 0.35, 0.35, "Casco", 2))
        p.append(caja("soporte", 0.5, s * 1.2, 1.4, 0.15, 1.2, 1.8, "Metal"))
    return suave(unir(p, "SM_Hidroavion"))


def pista():
    """Pista de 2 km × 45 m sobre plataforma de 120 m, con marcas blancas (largo en X)."""
    p = [caja("plataforma", 0, 0, 2.5, 2000, 120, 5, "Concreto"),
         caja("asfalto", 0, 0, 5.03, 2000, 45, 0.06, "Asfalto")]
    for i in range(40):
        p.append(caja(f"eje{i}", -975 + i * 50, 0, 5.08, 30, 0.9, 0.02, "Pintura"))
    for s in (-1, 1):
        p.append(caja(f"borde{s}", 0, s * 21.5, 5.08, 2000, 0.9, 0.02, "Pintura"))
        for k in range(8):
            p.append(caja(f"umbral{s}{k}", s * 960, -16 + k * 4.6, 5.08, 30, 1.8, 0.02, "Pintura"))
    for i in range(41):
        for s in (-1, 1):
            p.append(caja(f"luz{i}{s}", -1000 + i * 50, s * 24, 5.15, 0.4, 0.4, 0.2, "Luz"))
    return unir(p, "SM_Pista")


def hangar():
    p = [caja("cuerpo", 0, 0, 7.5, 40, 60, 15, "Metal"),
         caja("puerta", 20.05, 0, 6, 0.1, 44, 12, "MetalOscuro")]
    return unir(p, "SM_Hangar")


# ── Suite de muestra (Suite Retorno 100: 100 m² + terraza) — pabellón recorrible para el MVP ──
def suite_muestra():
    """10 × 10 m interiores + terraza de 4 m con daybed y plunge pool. Frente de vidrio hacia +X."""
    p = [caja("piso", 0, 0, 0.1, 10, 10, 0.2, "MaderaClara"),
         caja("terraza", 7, 0, 0.1, 4, 10, 0.2, "Piedra"),
         caja("techo", 1.5, 0, 3.35, 13.5, 10.6, 0.3, "Estuco"),
         caja("muro_fondo", -5.1, 0, 1.7, 0.2, 10.4, 3.2, "EstucoArena")]
    for s in (-1, 1):
        p.append(caja(f"muro{s}", 0, s * 5.1, 1.7, 10.4, 0.2, 3.2, "EstucoArena"))
    p.append(caja("vidrio", 5.05, -2.5, 1.7, 0.06, 5.0, 3.0, "Vidrio"))      # medio frente corredizo abierto
    # Vestíbulo y baño tipo spa (a la izquierda), separado por un muro bajo de piedra
    p.append(caja("muro_bano", -1.5, Y(1.6), 1.25, 7.0, 0.15, 2.3, "Piedra"))
    p.append(colocar(muebles.doble_lavabo(), -4.6, 3.3, 0.2, 0))
    p.append(colocar(muebles.regadera(), -1.2, 4.2, 0.2, 90))
    p.append(colocar(muebles.wc_washlet(), 1.2, 4.6, 0.2, 90))
    p.append(colocar(muebles.tina(), 3.4, 3.2, 0.2, 0))
    # Zona de descanso y de estar
    p.append(colocar(muebles.cama_king(), -2.8, -2.2, 0.2, 0))
    p.append(colocar(muebles.sofa3(), 2.6, -1.2, 0.2, 180))
    p.append(caja("mesa_centro", 1.6, Y(-1.2), 0.55, 0.8, 1.4, 0.06, "MaderaOscura"))
    p.append(caja("alfombra", 0.6, Y(-2.0), 0.21, 4.5, 3.8, 0.02, "TelaArena"))
    p.append(caja("escritorio", 0.6, Y(-4.6), 0.75, 1.5, 0.6, 0.04, "Madera"))
    # Terraza: daybed y plunge pool
    p.append(camastro_doble_suite(7.2, -2.5))
    p += alberca("plunge", 7.6, 2.6, 0.2, 2.2, 3.6, 0.25)
    return unir(p, "SM_SuiteMuestra")


def camastro_doble_suite(x, y):
    return colocar(muebles.camastro_doble(0, 0, 0), x, y, 0.2, 90)


# ── Piezas de experiencia: bar de playa, mirador del cráter, club náutico y alberca principal ──
def bar_playa():
    """Bar de playa: palapa redonda de 12 m con barra circular y bancos (coctelería, biblia §8)."""
    p = [cilindro("piso", 0, 0, 0.15, 7.5, 0.3, "MaderaClara", 24)]
    for k in range(8):
        a = 2 * math.pi * k / 8
        p.append(cilindro(f"poste{k}", 6.6 * math.cos(a), 6.6 * math.sin(a), 2.0, 0.15, 3.7, "Tronco", 8))
    p.append(cilindro("techo", 0, 0, 5.0, 8.4, 2.6, "Paja", 24, radio_arriba=0.3))
    p.append(sector("barra", 2.6, 3.4, 0, 360, 0.3, 1.4, "MaderaOscura", 32))
    p.append(sector("cubierta", 2.5, 3.6, 0, 360, 1.4, 1.48, "Marmol", 32))
    p.append(cilindro("contrabarra", 0, 0, 1.3, 1.4, 2.0, "Madera", 16))
    p.append(cilindro("luz", 0, 0, 3.6, 2.0, 0.08, "Luz", 24))
    for k in range(14):
        a = 2 * math.pi * k / 14
        p.append(cilindro(f"banco{k}", 4.2 * math.cos(a), 4.2 * math.sin(a), 0.65, 0.04, 0.7, "Laton", 6))
        p.append(cilindro(f"asiento{k}", 4.2 * math.cos(a), 4.2 * math.sin(a), 1.02, 0.22, 0.07, "TelaTerracota", 12))
    return suave(unir(p, "SM_BarPlaya"))


def mirador_crater():
    """Mirador en el borde del cráter: plataforma de madera en voladizo, barandal y bancas."""
    p = [caja("deck", 0, 0, 0.0, 14, 9, 0.3, "Madera")]
    for x in (-6.5, 6.5):
        for y in (-4, 4):
            p.append(cilindro("pilote", x, y, -3.0, 0.2, 6.0, "MaderaOscura", 8))
    for s in (-1, 1):
        p.append(caja(f"barandal{s}", 0, s * 4.45, 0.95, 14, 0.08, 0.06, "MaderaOscura"))
    p.append(caja("barandal_frente", 6.95, 0, 0.95, 0.08, 9, 0.06, "MaderaOscura"))
    for k in range(10):
        p.append(caja(f"poste{k}", -7 + k * 1.55, Y(4.45), 0.5, 0.08, 0.08, 0.95, "MaderaOscura"))
        p.append(caja(f"posteb{k}", -7 + k * 1.55, Y(-4.45), 0.5, 0.08, 0.08, 0.95, "MaderaOscura"))
    for y in (-2, 2):
        p.append(colocar(muebles.banca(), -1, y, 0.15, 90))
    p.append(caja("letrero", -6, 0, 1.2, 0.1, 2.4, 1.2, "Madera"))
    return unir(p, "SM_MiradorCrater")


def club_nautico():
    """Club náutico de la marina: pabellón de dos niveles con terraza sobre el agua."""
    p = [caja("base", 0, 0, 0.5, 24, 36, 1.0, "Piedra"),
         caja("pb_vidrio", -1, 0, 2.9, 18, 32, 3.8, "Vidrio"),
         caja("losa", 1, 0, 5.0, 24, 38, 0.4, "Estuco"),
         caja("pa", -3, 0, 7.0, 14, 24, 3.6, "Estuco"),
         caja("pa_vidrio", 4.05, 0, 7.0, 0.1, 22, 3.2, "Vidrio"),
         caja("techo", -2, 0, 9.0, 18, 28, 0.4, "Madera"),
         caja("terraza", 16, 0, 0.9, 10, 30, 0.2, "MaderaClara")]
    for k in range(6):
        p.append(colocar(muebles.mesa_restaurante(), 15, -12 + k * 4.8, 1.0))
    for s in (-1, 1):
        p.append(caja(f"barandal{s}", 21, s * 15, 1.5, 0.06, 0.06, 1.0, "Metal"))
    p.append(caja("pasamanos", 21, 0, 2.0, 0.08, 30, 0.06, "Metal"))
    return unir(p, "SM_ClubNautico")


def alberca_principal():
    """Alberca principal de 50 × 25 m: escalones de playa, bar dentro del agua, deck y camastros."""
    p = alberca("alberca", 0, 0, 0.0, 25, 50, 0.6)
    for k in range(4):
        p.append(caja(f"escalon{k}", -10.5 + k * 0.9, 0, -0.75 + k * 0.18, 0.9, 12, 0.18, "Piedra"))
    p.append(cilindro("isla_bar", 5, Y(-15), -0.2, 3.5, 1.4, "Piedra", 24))
    p.append(cilindro("barra_bar", 5, Y(-15), 0.6, 3.0, 0.2, "Marmol", 24))
    for k in range(8):
        a = 2 * math.pi * k / 8
        p.append(cilindro(f"banco{k}", 5 + 4.1 * math.cos(a), Y(-15 + 4.1 * math.sin(a)), -0.35, 0.25, 0.7, "Piedra", 10))
    p.append(caja("deck", 0, 0, -0.05, 37, 62, 0.08, "Piedra"))
    for s in (-1, 1):
        for k in range(10):
            p.append(colocar(muebles.camastro(), s * 15.5, -22 + k * 4.8, 0.0, 90 + 90 * s))
            if k % 2:
                p.append(colocar(muebles.sombrilla_tela(), s * 17.0, -22 + k * 4.8, 0.0))
    return unir(p, "SM_AlbercaPrincipal")
