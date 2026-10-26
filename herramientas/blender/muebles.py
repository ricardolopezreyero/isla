# RLR · Isla La Encantada — Ricardo López Reyero
# Muebles y objetos de playa hechos en casa, con las medidas de la biblia
# (docs/biblia/01-prompt-maestro-v2.md §4–5 y §8; restaurante §5; Suite Retorno 100).
import math

from comun import caja, cilindro, esfera, suave, unir

_RLR = "Ricardo López Reyero"


# ── Playa y alberca ──────────────────────────────────────────────────────────────────────────
def camastro():
    """Camastro de madera con colchoneta: 2.0 × 0.72 m, asiento a 0.38 m, respaldo reclinado."""
    p = []
    for s in (-1, 1):
        p.append(caja("larguero", 0, s * 0.33, 0.25, 2.0, 0.06, 0.08, "Madera"))
        for x in (-0.9, 0.9):
            p.append(caja("pata", x, s * 0.33, 0.12, 0.07, 0.07, 0.24, "Madera"))
    for i in range(12):
        p.append(caja("tabla", -0.95 + i * 0.12, 0, 0.29, 0.09, 0.66, 0.025, "MaderaClara"))
    p.append(caja("colchon", 0.15, 0, 0.35, 1.3, 0.68, 0.08, "Tela", bisel=0.03))
    resp = caja("respaldo", -0.72, 0, 0.55, 0.62, 0.68, 0.08, "Tela", rot_z=0, bisel=0.03)
    resp.rotation_euler = (0, math.radians(-38), 0)
    p.append(resp)
    return unir(p, "SM_Camastro")


def sombrilla_palma():
    """Sombrilla de palma (paja) de 3 m de diámetro."""
    p = [cilindro("poste", 0, 0, 1.3, 0.06, 2.6, "Madera", 10),
         cilindro("techo", 0, 0, 2.65, 1.55, 0.7, "Paja", 16, radio_arriba=0.05),
         cilindro("fleco", 0, 0, 2.32, 1.58, 0.08, "Paja", 16)]
    return suave(unir(p, "SM_SombrillaPalma"))


def sombrilla_tela():
    """Sombrilla de tela blanca, 2.8 m, para alberca."""
    p = [cilindro("base", 0, 0, 0.04, 0.3, 0.08, "MetalOscuro", 16),
         cilindro("poste", 0, 0, 1.2, 0.03, 2.4, "Metal", 8),
         cilindro("tela", 0, 0, 2.35, 1.45, 0.45, "Tela", 8, radio_arriba=0.04)]
    return unir(p, "SM_SombrillaTela")


def palapa():
    """Palapa de playa 5 × 5 m con techo de palma a cuatro aguas."""
    p = [caja("piso", 0, 0, 0.1, 5.2, 5.2, 0.2, "MaderaClara")]
    for x in (-2.3, 2.3):
        for y in (-2.3, 2.3):
            p.append(cilindro("poste", x, y, 1.45, 0.12, 2.7, "Tronco", 10))
    techo = cilindro("techo", 0, 0, 3.6, 4.4, 2.0, "Paja", 4, radio_arriba=0.1)
    techo.rotation_euler = (0, 0, math.radians(45))
    p.append(techo)
    p.append(camastro_doble(0, 0, 0.2))
    return unir(p, "SM_Palapa")


def camastro_doble(x, y, z):
    p = [caja("base", x, y, z + 0.2, 2.0, 1.6, 0.4, "Madera", bisel=0.03),
         caja("colchon", x, y, z + 0.47, 1.95, 1.55, 0.14, "Tela", bisel=0.05)]
    for k in range(4):
        p.append(caja("cojin", x - 0.8, y - 0.55 + k * 0.37, z + 0.68, 0.18, 0.34, 0.3, "TelaArena" if k % 2 else "TelaAzul", bisel=0.05))
    return unir(p, "camastro_doble")


def farol():
    """Farol de camino: 3.2 m, luz cálida 2700–3000 K (biblia §2)."""
    p = [cilindro("base", 0, 0, 0.15, 0.18, 0.3, "MetalOscuro", 12),
         cilindro("poste", 0, 0, 1.65, 0.05, 3.0, "MetalOscuro", 10),
         caja("lampara", 0, 0, 3.0, 0.3, 0.3, 0.42, "Luz"),
         caja("tapa", 0, 0, 3.25, 0.38, 0.38, 0.06, "MetalOscuro")]
    return unir(p, "SM_Farol")


def luz_piso():
    """Luz al ras de piso para senderos (restaurante §2)."""
    return unir([cilindro("b", 0, 0, 0.2, 0.08, 0.4, "MetalOscuro", 10), cilindro("l", 0, 0, 0.36, 0.07, 0.06, "Luz", 10)], "SM_LuzPiso")


def banca():
    p = [caja("pata1", -0.7, 0, 0.21, 0.08, 0.45, 0.42, "MetalOscuro"), caja("pata2", 0.7, 0, 0.21, 0.08, 0.45, 0.42, "MetalOscuro")]
    for i in range(5):
        p.append(caja("tabla", 0, -0.2 + i * 0.1, 0.45, 1.6, 0.08, 0.04, "Madera"))
    for i in range(3):
        p.append(caja("resp", 0, 0.26, 0.6 + i * 0.12, 1.6, 0.04, 0.08, "Madera"))
    return unir(p, "SM_Banca")


def kayak():
    o = esfera("kayak", 0, 0, 0.18, 2.0, 0.32, 0.18, "Pintura", 2)
    return unir([o, esfera("asiento", 0, 0, 0.33, 0.35, 0.22, 0.06, "MetalOscuro", 1)], "SM_Kayak")


# ── Habitación (biblia §4) ──────────────────────────────────────────────────────────────────
def cama_king():
    """Cama king 200 × 200: colchón 35 cm + topper 6 cm, altura total 58 cm, cabecera acolchada,
    4 almohadas grandes + 2 decorativas, burós con lámpara a ambos lados."""
    p = [caja("base", 0, 0, 0.1, 2.0, 2.06, 0.2, "MaderaOscura", bisel=0.02),
         caja("colchon", 0, 0, 0.375, 2.0, 2.0, 0.35, "Tela", bisel=0.05),
         caja("topper", 0, 0, 0.55, 1.98, 1.98, 0.06, "Tela", bisel=0.03),
         caja("piecera", 0.55, 0, 0.6, 0.6, 2.04, 0.03, "TelaArena", bisel=0.01),
         caja("cabecera", -1.06, 0, 0.75, 0.12, 2.3, 1.3, "TelaArena", bisel=0.05)]
    for k in range(4):
        p.append(caja("almohada", -0.82 + (k // 2) * 0.12, -0.5 + (k % 2) * 1.0, 0.68 + (k // 2) * 0.12, 0.45, 0.75, 0.18, "Tela", bisel=0.07))
    for k in range(2):
        p.append(caja("cojin", -0.6, -0.25 + k * 0.5, 0.7, 0.2, 0.45, 0.3, "TelaTerracota", bisel=0.06))
    for s in (-1, 1):
        p += [caja("buro", -0.82, s * 1.45, 0.3, 0.45, 0.5, 0.6, "Madera", bisel=0.01),
              cilindro("lamp_b", -0.82, s * 1.45, 0.75, 0.07, 0.3, "Laton", 12),
              cilindro("lamp_p", -0.82, s * 1.45, 1.02, 0.2, 0.28, "Tela", 16, radio_arriba=0.15)]
    return unir(p, "SM_CamaKing")


def sofa3():
    """Sofá de 3 plazas muy profundo, tipo lounge (Suite Retorno 100 §4)."""
    p = [caja("base", 0, 0, 0.2, 1.05, 2.4, 0.3, "TelaArena", bisel=0.04)]
    for k in range(3):
        p.append(caja("asiento", 0.08, -0.78 + k * 0.78, 0.43, 0.85, 0.76, 0.18, "TelaArena", bisel=0.06))
        p.append(caja("resp", -0.42, -0.78 + k * 0.78, 0.72, 0.22, 0.76, 0.5, "TelaArena", bisel=0.07))
    for s in (-1, 1):
        p.append(caja("brazo", 0, s * 1.13, 0.45, 1.05, 0.18, 0.55, "TelaArena", bisel=0.06))
    return unir(p, "SM_Sofa3")


def mesa_comedor(sillas=4):
    """Mesa de 75 cm de alto con sillas de asiento a 45 cm (biblia §8)."""
    p = [caja("cubierta", 0, 0, 0.73, 1.6 if sillas > 2 else 0.8, 0.9, 0.04, "Madera", bisel=0.01)]
    for x in (-0.7, 0.7) if sillas > 2 else (-0.3, 0.3):
        for y in (-0.35, 0.35):
            p.append(caja("pata", x, y, 0.36, 0.06, 0.06, 0.71, "MaderaOscura"))
    pos = [(-0.4, -0.75, 0), (0.4, -0.75, 0), (-0.4, 0.75, 180), (0.4, 0.75, 180)][:sillas] if sillas > 2 else [(0, -0.75, 0), (0, 0.75, 180)]
    for x, y, r in pos:
        p.append(silla(x, y, r))
    return unir(p, f"SM_MesaComedor{sillas}")


def silla(x=0, y=0, rot=0):
    s = 1 if rot == 0 else -1
    p = [caja("asiento", x, y, 0.45, 0.46, 0.46, 0.05, "TelaArena", bisel=0.015),
         caja("resp", x, y - s * 0.21, 0.72, 0.46, 0.05, 0.5, "Madera", bisel=0.01)]
    for dx in (-0.2, 0.2):
        for dy in (-0.2, 0.2):
            p.append(caja("pata", x + dx, y + dy, 0.21, 0.04, 0.04, 0.42, "MaderaOscura"))
    return unir(p, "silla")


def doble_lavabo():
    """Doble lavabo: cubierta a 88 cm, lavabos separados 80 cm, espejo con centro a 1.55 m (biblia §4.2)."""
    p = [caja("mueble", 0, 0, 0.45, 0.55, 1.8, 0.8, "MaderaOscura", bisel=0.01),
         caja("cubierta", 0, 0, 0.87, 0.58, 1.84, 0.04, "Marmol", bisel=0.005),
         caja("espejo", -0.27, 0, 1.55, 0.03, 1.7, 0.95, "Vidrio"),
         caja("luz_espejo", -0.25, 0, 2.06, 0.05, 1.6, 0.04, "Luz")]
    for y in (-0.4, 0.4):
        p.append(esfera("lavabo", 0.03, y, 0.94, 0.2, 0.17, 0.08, "Ceramica", 2))
        p.append(cilindro("llave", -0.18, y, 1.0, 0.015, 0.22, "Cromo", 8))
        p.append(caja("pico", -0.1, y, 1.1, 0.16, 0.03, 0.03, "Cromo"))
    return unir(p, "SM_DobleLavabo")


def regadera():
    """Regadera tipo lluvia: espacio 1.0 × 1.4 m para dos, cabezal de 30 cm, jets laterales y nicho."""
    p = [caja("piso", 0, 0, 0.02, 1.0, 1.4, 0.04, "PiedraOscura"),
         caja("muro", -0.52, 0, 1.15, 0.04, 1.4, 2.3, "Piedra"),
         caja("mampara", 0.5, 0, 1.05, 0.02, 1.4, 2.1, "Vidrio"),
         cilindro("lluvia", 0, 0, 2.25, 0.15, 0.02, "Cromo", 24),
         cilindro("brazo", -0.25, 0, 2.27, 0.012, 0.5, "Cromo", 8, rot=(0, math.radians(90), 0)),
         caja("nicho", -0.5, 0.45, 1.1, 0.06, 0.4, 0.3, "Luz")]
    for z in (1.1, 1.3):
        p.append(cilindro("jet", -0.5, -0.3, z, 0.03, 0.03, "Cromo", 8, rot=(0, math.radians(90), 0)))
    return unir(p, "SM_Regadera")


def wc_washlet():
    """Escusado tipo washlet: asiento a 43 cm, tapa de cierre suave."""
    p = [esfera("taza", 0, 0, 0.25, 0.3, 0.2, 0.25, "Ceramica", 2),
         caja("asiento", 0.02, 0, 0.43, 0.48, 0.38, 0.04, "Ceramica", bisel=0.02),
         caja("tanque", -0.28, 0, 0.55, 0.18, 0.4, 0.3, "Ceramica", bisel=0.03),
         caja("panel", 0.0, 0.26, 0.55, 0.12, 0.03, 0.06, "MetalOscuro")]
    return unir(p, "SM_WCWashlet")


def tina():
    return suave(unir([esfera("tina", 0, 0, 0.28, 0.9, 0.42, 0.3, "Ceramica", 3), cilindro("llave", -0.85, 0, 0.5, 0.02, 0.4, "Cromo", 8)], "SM_Tina"))


def mesa_restaurante():
    """Mesa de restaurante para 2 con mantel y luz cálida de mesa (biblia §8)."""
    p = [cilindro("cubierta", 0, 0, 0.74, 0.45, 0.04, "Tela", 24),
         cilindro("pata", 0, 0, 0.37, 0.05, 0.72, "MetalOscuro", 10),
         cilindro("base", 0, 0, 0.02, 0.25, 0.04, "MetalOscuro", 16),
         cilindro("vela", 0, 0, 0.8, 0.04, 0.09, "Luz", 10)]
    for a in (0, 180):
        x = 0.65 * math.cos(math.radians(a))
        p.append(silla(x, 0, 0) if a == 0 else silla(x, 0, 180))
    return unir(p, "SM_MesaRestaurante")


def barra_bar(largo=6.0):
    p = [caja("frente", 0, 0, 0.55, 0.6, largo, 1.1, "MaderaOscura", bisel=0.02),
         caja("cubierta", 0, 0, 1.12, 0.75, largo + 0.1, 0.05, "Marmol", bisel=0.01),
         caja("contra", -1.3, 0, 1.2, 0.4, largo, 2.4, "Madera"),
         caja("luz", -1.08, 0, 1.6, 0.05, largo - 0.4, 0.05, "Luz")]
    for i in range(int(largo / 0.7)):
        y = -largo / 2 + 0.4 + i * 0.7
        p += [cilindro("banco", 0.7, y, 0.38, 0.03, 0.76, "Laton", 8), cilindro("asiento", 0.7, y, 0.78, 0.2, 0.06, "TelaArena", 16)]
    return unir(p, f"SM_Barra")
