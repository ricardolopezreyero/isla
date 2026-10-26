# RLR · Isla La Encantada — Ricardo López Reyero
# Terreno de la isla hecho en casa: malla de alturas de 4.8 × 4.8 km con volcán y cráter hundido,
# playas que bajan al mar, acantilados al norte, bahía de la marina y las penínsulas de
# Villa Horizonte (norte) y del restaurante (oeste-suroeste). Mismo plano que greybox_isla.py.
# Coordenadas Unreal en metros (norte = +X, este = +Y); al crear la malla se invierte Y para Blender.
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector, noise

from comun import material

_RLR = "Ricardo López Reyero"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import isla_geo   # noqa: E402  (la misma geometría que usa el plano de colocación)


def _ruido(x, y):
    return noise.noise(Vector((x, y, 0.3)))


def altura(x, y):
    return isla_geo.altura(x, y, _ruido)


MATERIAL_ZONA = {"mar": "ArenaMojada", "arena": "Arena", "pasto": "Pasto", "roca": "Roca",
                 "selva": "Selva", "volcan": "Volcan", "crater": "RocaVolcanica", "pastoseco": "PastoSeco",
                 "orilla": "ArenaMojada", "cumbre": "Roca"}


def terreno(lado_m=4800.0, celdas=600):
    paso = lado_m / celdas
    bm = bmesh.new()
    verts, zonas = [], []
    for j in range(celdas + 1):
        fila = []
        for i in range(celdas + 1):
            x = -lado_m / 2 + i * paso
            y = -lado_m / 2 + j * paso
            h, z = altura(x, y)
            fila.append(bm.verts.new((x, -y, h)))
            zonas.append(z)
        verts.append(fila)
    mats = sorted(set(MATERIAL_ZONA.values()))
    me = bpy.data.meshes.new("SM_Terreno")
    for m in mats:
        me.materials.append(material(m))
    for j in range(celdas):
        for i in range(celdas):
            v = (verts[j][i], verts[j][i + 1], verts[j + 1][i + 1], verts[j + 1][i])
            f = bm.faces.new((v[0], v[3], v[2], v[1]))
            cx = -lado_m / 2 + (i + 0.5) * paso
            cy = -lado_m / 2 + (j + 0.5) * paso
            h, z = altura(cx, cy)
            hs = [vv.co.z for vv in v]
            if z == "pasto" and max(hs) - min(hs) > paso * 0.7:
                z = "roca"
            elif z == "pasto" and noise.noise(Vector((cx * 0.006, cy * 0.006, 1.7))) > 0.42:
                z = "pastoseco"                                   # manchas de pasto seco: la meseta no es de un solo verde
            elif z == "arena" and h < 0.35:
                z = "orilla"                                      # arena mojada donde rompe el agua
            elif z == "volcan" and h > 300:
                z = "cumbre"
            f.material_index = mats.index(MATERIAL_ZONA[z])
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("SM_Terreno", me)
    bpy.context.collection.objects.link(o)
    for p in me.polygons:
        p.use_smooth = True
    return o


def caminos(plano_json):
    """Malla única con todos los caminos del plano, pegada al terreno (cintas de ancho fijo, muestreo cada 4 m)."""
    import json as _json
    datos = _json.loads(open(plano_json, encoding="utf-8").read())["caminos"]
    bm = bmesh.new()
    me = bpy.data.meshes.new("SM_Caminos")
    mats = sorted({c["mat"] for c in datos})
    for m in mats:
        me.materials.append(material(m))
    for c in datos:
        pts = []
        for (ax, ay), (bx, by) in zip(c["puntos"], c["puntos"][1:]):
            n = max(1, int(math.hypot(bx - ax, by - ay) / 4))
            pts += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(n)]
        pts.append(tuple(c["puntos"][-1]))
        izq, der = [], []
        for i, (x, y) in enumerate(pts):
            a = pts[max(i - 1, 0)]
            b = pts[min(i + 1, len(pts) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L * c["ancho"] / 2, dx / L * c["ancho"] / 2
            for lista, (px, py) in ((izq, (x + nx, y + ny)), (der, (x - nx, y - ny))):
                z = max(altura(px, py)[0], altura(x, y)[0]) + 0.15
                z = max(z, c["z_min"] + 0.15)
                lista.append((bm.verts.new((px, -py, z)), bm.verts.new((px, -py, z - 0.5))))
        idx = mats.index(c["mat"])
        for i in range(len(pts) - 1):
            for cara in ((izq[i][0], der[i][0], der[i + 1][0], izq[i + 1][0]),
                         (izq[i][1], izq[i][0], izq[i + 1][0], izq[i + 1][1]),
                         (der[i][0], der[i][1], der[i + 1][1], der[i + 1][0])):
                try:
                    f = bm.faces.new(cara)
                    f.material_index = idx
                except ValueError:
                    pass
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("SM_Caminos", me)
    bpy.context.collection.objects.link(o)
    return o
