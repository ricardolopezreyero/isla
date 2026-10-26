# RLR · Isla La Encantada — Ricardo López Reyero
# Naturaleza hecha en casa: palmas, árboles, arbustos con flor y rocas volcánicas.
# Flora de referencia: catalogo/flora.md (cocotera, palma real, almendro, buganvilia, hibisco…).
import math

import bmesh
import bpy
from mathutils import Vector, noise

from comun import aplicar_mods, asignar, esfera, sembrar, suave, unir

_RLR = "Ricardo López Reyero"


def tubo(nombre, puntos, radios, mat, lados=10):
    """Tubo a lo largo de una polilínea (troncos, ramas, nervaduras)."""
    bm = bmesh.new()
    anillos = []
    for i, (p, r) in enumerate(zip(puntos, radios)):
        p = Vector(p)
        d = (Vector(puntos[min(i + 1, len(puntos) - 1)]) - Vector(puntos[max(i - 1, 0)])).normalized()
        a = d.orthogonal().normalized()
        b = d.cross(a).normalized()
        anillo = [bm.verts.new(p + (a * math.cos(2 * math.pi * k / lados) + b * math.sin(2 * math.pi * k / lados)) * r)
                  for k in range(lados)]
        anillos.append(anillo)
    for i in range(len(anillos) - 1):
        for k in range(lados):
            bm.faces.new((anillos[i][k], anillos[i][(k + 1) % lados], anillos[i + 1][(k + 1) % lados], anillos[i + 1][k]))
    bm.faces.new(list(reversed(anillos[0])))
    bm.faces.new(anillos[-1])
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.collection.objects.link(o)
    return asignar(o, mat)


def hoja_palma(nombre, base, direccion, largo, caida, mat, foliolos=30, subida=0.35):
    """Fronda: nervadura arqueada con foliolos largos que cuelgan en V a ambos lados."""
    d = Vector(direccion).normalized()
    lado = Vector((-d.y, d.x, 0)).normalized()
    pts = []
    for i in range(foliolos + 1):
        t = i / foliolos
        pts.append(Vector(base) + d * (largo * t * (1 - 0.15 * t)) + Vector((0, 0, largo * (subida * t - caida * t * t))))
    bm = bmesh.new()
    for i in range(1, foliolos):
        p0, p1 = pts[i], pts[i + 1]
        t = i / foliolos
        lf = 1.15 * math.sin(math.pi * min(1, t * 1.1)) + 0.12          # largo del foliolo
        tang = (p1 - p0).normalized()
        for s in (-1, 1):
            punta = p0 + lado * s * lf * 0.8 + Vector((0, 0, -0.55 * lf)) + tang * 0.45 * lf
            v = [bm.verts.new(p0), bm.verts.new(p0 + tang * 0.16), bm.verts.new(punta)]
            bm.faces.new(v if s > 0 else list(reversed(v)))
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.collection.objects.link(o)
    asignar(o, mat)
    sol = o.modifiers.new("grosor", "SOLIDIFY")
    sol.thickness = 0.012
    aplicar_mods(o)
    nerv = tubo(nombre + "_nerv", [tuple(p) for p in pts], [0.055 * (1 - i / (len(pts) + 2)) + 0.012 for i in range(len(pts))], "TroncoClaro", 5)
    return [o, nerv]


def palma_cocotera(semilla=1, alto=14.0, inclinacion=2.5):
    """Palma cocotera (Cocos nucifera): tronco curvo con anillos, 14 frondas y racimo de cocos."""
    rng = sembrar(semilla)
    seg = 18
    ang = rng.uniform(0, 2 * math.pi)
    dx, dy = math.cos(ang), math.sin(ang)
    pts, rad = [], []
    for i in range(seg + 1):
        t = i / seg
        off = inclinacion * t * t
        pts.append((dx * off, dy * off, alto * t))
        rad.append((0.22 - 0.07 * t + 0.16 * max(0.0, 0.12 - t) / 0.12) * (1.06 if i % 2 else 1.0))
    partes = [tubo("tronco", pts, rad, "Tronco", 12)]
    copa = Vector(pts[-1])
    partes.append(esfera("copa", copa.x, copa.y, copa.z + 0.1, 0.35, 0.35, 0.45, "Tronco", 1))
    n = 18
    for k in range(n):
        a = 2 * math.pi * k / n + rng.uniform(-0.12, 0.12)
        joven = k % 3 == 0
        partes += hoja_palma(f"hoja{k}", copa + Vector((0, 0, 0.25)), (math.cos(a), math.sin(a), 0),
                             rng.uniform(3.6, 4.4) if joven else rng.uniform(4.6, 5.6),
                             rng.uniform(0.25, 0.45) if joven else rng.uniform(0.7, 1.05),
                             "HojaClara" if joven else "Hoja", subida=0.55 if joven else 0.3)
    for k in range(6):
        a = 2 * math.pi * k / 6
        partes.append(esfera(f"coco{k}", copa.x + 0.3 * math.cos(a), copa.y + 0.3 * math.sin(a), copa.z - 0.35,
                             0.16, 0.16, 0.19, "Coco", 1))
    return suave(unir(partes, f"SM_PalmaCocotera_{semilla}"))


def palma_real(semilla=1, alto=18.0):
    """Palma real (Roystonea regia): tronco recto y liso, capitel verde y copa amplia."""
    rng = sembrar(semilla + 50)
    pts = [(0, 0, alto * i / 10) for i in range(11)]
    rad = [0.32 - 0.1 * (i / 10) + (0.06 if i == 4 else 0) for i in range(11)]
    partes = [tubo("tronco", pts, rad, "Piedra", 14)]
    partes.append(tubo("capitel", [(0, 0, alto), (0, 0, alto + 2.2)], [0.24, 0.2], "HojaClara", 12))
    for k in range(12):
        a = 2 * math.pi * k / 12 + rng.uniform(-0.1, 0.1)
        partes += hoja_palma(f"hoja{k}", (0, 0, alto + 2.2), (math.cos(a), math.sin(a), 0), rng.uniform(3.8, 4.6),
                             rng.uniform(0.4, 0.8), "Hoja")
    return suave(unir(partes, f"SM_PalmaReal_{semilla}"))


def copa_frondosa(nombre, centro, ancho, alto, mat, bolas=9, semilla=1):
    rng = sembrar(semilla)
    partes = []
    for k in range(bolas):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, ancho * 0.35)
        partes.append(esfera(f"{nombre}{k}", centro[0] + r * math.cos(a), centro[1] + r * math.sin(a),
                             centro[2] + rng.uniform(-alto * 0.2, alto * 0.25), ancho * rng.uniform(0.28, 0.4),
                             ancho * rng.uniform(0.28, 0.4), alto * rng.uniform(0.35, 0.5), mat, 3))
    return partes


def almendro(semilla=1):
    """Almendro de playa (Terminalia catappa): ramas horizontales en pisos y copa amplia."""
    rng = sembrar(semilla + 100)
    partes = [tubo("tronco", [(0, 0, 0), (0.2, 0, 3), (0.1, 0.1, 6), (0, 0, 8)], [0.45, 0.35, 0.28, 0.2], "Tronco", 12)]
    for piso, z in enumerate((3.5, 5.5, 7.5)):
        for k in range(4):
            a = 2 * math.pi * k / 4 + piso * 0.6
            L = 5.0 - piso * 1.2
            partes.append(tubo(f"rama{piso}{k}", [(0, 0, z), (L * 0.6 * math.cos(a), L * 0.6 * math.sin(a), z + 0.4),
                                                  (L * math.cos(a), L * math.sin(a), z + 0.6)], [0.16, 0.1, 0.05], "Tronco", 6))
            partes += copa_frondosa(f"c{piso}{k}", (L * math.cos(a), L * math.sin(a), z + 0.9), 4.0 - piso * 0.6, 1.6,
                                    "Hoja" if k % 2 else "HojaClara", 3, semilla * 10 + piso * 4 + k)
    return suave(unir(partes, f"SM_Almendro_{semilla}"))


def ceiba(semilla=1):
    """Ceiba monumental: tronco con contrafuertes y copa enorme."""
    partes = [tubo("tronco", [(0, 0, 0), (0, 0, 8), (0, 0, 16), (0, 0, 20)], [1.3, 0.9, 0.7, 0.5], "TroncoClaro", 16)]
    for k in range(5):
        a = 2 * math.pi * k / 5
        partes.append(tubo(f"raiz{k}", [(3 * math.cos(a), 3 * math.sin(a), 0), (1.2 * math.cos(a), 1.2 * math.sin(a), 2.5),
                                         (0.4 * math.cos(a), 0.4 * math.sin(a), 5)], [0.35, 0.3, 0.15], "TroncoClaro", 6))
    partes += copa_frondosa("copa", (0, 0, 22), 22, 6, "Hoja", 12, semilla + 300)
    return suave(unir(partes, f"SM_Ceiba_{semilla}"))


def arbusto_flor(semilla=1, flor="Flor", ancho=2.2, alto=1.6):
    """Buganvilia / hibisco: masa verde con flores encima."""
    rng = sembrar(semilla + 200)
    partes = copa_frondosa("masa", (0, 0, alto * 0.5), ancho, alto, "Hoja", 6, semilla + 7)
    for k in range(28):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.2, ancho * 0.48)
        partes.append(esfera(f"flor{k}", r * math.cos(a), r * math.sin(a), alto * rng.uniform(0.55, 1.0),
                             0.12, 0.12, 0.08, flor, 1))
    return suave(unir(partes, f"SM_Arbusto{flor}_{semilla}"))


def roca(semilla=1, ancho=4.0, alto=2.5, mat="RocaVolcanica"):
    """Roca volcánica con ruido: para costas, acantilados y jardines."""
    o = esfera("roca", 0, 0, 0, ancho / 2, ancho / 2 * 0.8, alto / 2, mat, 3)
    off = Vector((semilla * 3.1, semilla * 7.7, semilla * 1.3))
    for v in o.data.vertices:
        n = noise.noise(v.co * 0.6 + off) * 0.35 + noise.noise(v.co * 1.7 + off) * 0.12
        v.co *= 1 + n
        v.co.z = max(v.co.z, -alto * 0.15)
    o.name = f"SM_Roca_{semilla}"
    return suave(o)


def pasto_playa(semilla=1):
    """Mata de pasto de duna (Ipomoea / pastos resistentes)."""
    rng = sembrar(semilla + 400)
    partes = []
    for k in range(18):
        a = rng.uniform(0, 2 * math.pi)
        h = rng.uniform(0.5, 1.0)
        b = (rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), 0)
        partes.append(tubo(f"brizna{k}", [b, (b[0] + 0.25 * math.cos(a), b[1] + 0.25 * math.sin(a), h * 0.6),
                                          (b[0] + 0.5 * math.cos(a), b[1] + 0.5 * math.sin(a), h)], [0.03, 0.02, 0.005],
                           "PastoSeco" if k % 2 else "HojaClara", 4))
    return suave(unir(partes, f"SM_PastoPlaya_{semilla}"))


def agave(semilla=1):
    """Agave de costa: roseta de pencas gruesas, escultórica (catalogo/flora.md, vegetación costera)."""
    rng = sembrar(semilla + 600)
    partes = []
    for k in range(22):
        a = 2 * math.pi * k / 22 + rng.uniform(-0.1, 0.1)
        incl = rng.uniform(0.35, 1.25)
        L = rng.uniform(0.9, 1.4)
        punta = (L * math.cos(a) * math.sin(incl), L * math.sin(a) * math.sin(incl), L * math.cos(incl) + 0.1)
        partes.append(tubo(f"penca{k}", [(0, 0, 0.1), (punta[0] * 0.5, punta[1] * 0.5, punta[2] * 0.6), punta],
                           [0.11, 0.08, 0.005], "PastoSeco" if k % 4 == 0 else "HojaClara", 5))
    return suave(unir(partes, f"SM_Agave_{semilla}"))


def heliconia(semilla=1):
    """Heliconia: hojas grandes tipo banano y brácteas rojas que atraen colibríes."""
    rng = sembrar(semilla + 700)
    partes = []
    for k in range(7):
        a = rng.uniform(0, 2 * math.pi)
        h = rng.uniform(1.4, 2.2)
        base = (rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.25), 0)
        tope = (base[0] + 0.3 * math.cos(a), base[1] + 0.3 * math.sin(a), h)
        partes.append(tubo(f"tallo{k}", [base, tope], [0.03, 0.02], "HojaClara", 5))
        hoja = esfera(f"hoja{k}", 0, 0, 0, 0.55, 0.16, 0.04, "Hoja", 2)
        hoja.rotation_euler = (0, math.radians(25), a)
        hoja.location = (tope[0] + 0.35 * math.cos(a), tope[1] + 0.35 * math.sin(a), tope[2] - 0.2)
        partes.append(hoja)
        if k % 2 == 0:
            for j in range(4):
                partes.append(esfera(f"bractea{k}{j}", tope[0] + (0.08 if j % 2 else -0.08), tope[1], tope[2] + 0.12 - j * 0.12,
                                     0.12, 0.05, 0.05, "FlorRoja", 1))
    return suave(unir(partes, f"SM_Heliconia_{semilla}"))


def helecho(semilla=1):
    """Helecho del sotobosque: frondas arqueadas desde el centro."""
    rng = sembrar(semilla + 800)
    partes = []
    for k in range(12):
        a = 2 * math.pi * k / 12 + rng.uniform(-0.15, 0.15)
        partes += hoja_palma(f"fronda{k}", (0, 0, 0.15), (math.cos(a), math.sin(a), 0), rng.uniform(0.9, 1.3),
                             rng.uniform(0.6, 1.0), "HojaClara" if k % 3 else "Hoja", 16, 0.9)
    return suave(unir(partes, f"SM_Helecho_{semilla}"))


def platanera(semilla=1):
    """Platanera ornamental: pseudotallo y hojas enormes, da sombra tropical a los jardines."""
    rng = sembrar(semilla + 900)
    partes = [tubo("tallo", [(0, 0, 0), (0, 0, 2.8)], [0.2, 0.14], "HojaClara", 10)]
    for k in range(8):
        a = 2 * math.pi * k / 8 + rng.uniform(-0.2, 0.2)
        hoja = esfera(f"hoja{k}", 0, 0, 0, 1.3, 0.35, 0.05, "Hoja" if k % 2 else "HojaClara", 2)
        hoja.rotation_euler = (0, math.radians(rng.uniform(15, 40)), a)
        hoja.location = (1.15 * math.cos(a), 1.15 * math.sin(a), 3.0 + rng.uniform(-0.3, 0.5))
        partes.append(hoja)
    return suave(unir(partes, f"SM_Platanera_{semilla}"))
