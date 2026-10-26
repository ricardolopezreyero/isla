# RLR · Isla La Encantada — Ricardo López Reyero
# Utilidades comunes de la fábrica de objetos en Blender (todo hecho en casa, sin assets comprados).
# Convención: se modela en METROS con Z hacia arriba. Al exportar a FBX, Unreal convierte a cm.
# Para que una coordenada del plano (x norte, y este) caiga igual en Unreal, en Blender se usa y_b = -y.
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

# Paleta de la casa (lineal, 0–1) + aspereza. Los nombres son los slots de material que llegan a Unreal.
PALETA = {
    "Arena": ((0.86, 0.78, 0.60), 0.9), "ArenaMojada": ((0.62, 0.52, 0.38), 0.6),
    "Pasto": ((0.16, 0.38, 0.12), 0.9), "PastoSeco": ((0.26, 0.38, 0.13), 0.9),
    "Selva": ((0.07, 0.24, 0.07), 0.9), "Volcan": ((0.15, 0.26, 0.10), 0.9),
    "Roca": ((0.30, 0.27, 0.24), 0.95), "RocaVolcanica": ((0.12, 0.10, 0.09), 0.95),
    "Tronco": ((0.36, 0.27, 0.18), 0.9), "TroncoClaro": ((0.55, 0.45, 0.34), 0.9),
    "Hoja": ((0.10, 0.36, 0.08), 0.6), "HojaClara": ((0.24, 0.50, 0.12), 0.6),
    "Coco": ((0.35, 0.25, 0.08), 0.6), "Flor": ((0.80, 0.05, 0.35), 0.6), "FlorRoja": ((0.85, 0.08, 0.05), 0.6),
    "FlorBlanca": ((0.95, 0.93, 0.88), 0.6), "Estuco": ((0.93, 0.91, 0.86), 0.7), "EstucoArena": ((0.86, 0.80, 0.70), 0.8),
    "Madera": ((0.45, 0.30, 0.18), 0.6), "MaderaClara": ((0.70, 0.55, 0.38), 0.6), "MaderaOscura": ((0.20, 0.13, 0.08), 0.5),
    "Piedra": ((0.78, 0.74, 0.66), 0.8), "PiedraOscura": ((0.35, 0.33, 0.30), 0.8), "Marmol": ((0.92, 0.91, 0.89), 0.2),
    "Vidrio": ((0.10, 0.20, 0.24), 0.05), "Metal": ((0.55, 0.55, 0.56), 0.3), "Laton": ((0.75, 0.58, 0.30), 0.3),
    "MetalOscuro": ((0.08, 0.08, 0.09), 0.4), "Tela": ((0.96, 0.95, 0.92), 0.95), "TelaArena": ((0.80, 0.72, 0.58), 0.95),
    "TelaAzul": ((0.07, 0.17, 0.32), 0.95), "TelaTerracota": ((0.65, 0.30, 0.18), 0.95), "Paja": ((0.66, 0.53, 0.30), 0.95),
    "Agua": ((0.04, 0.55, 0.65), 0.05), "AguaAlberca": ((0.10, 0.70, 0.80), 0.05), "Mosaico": ((0.15, 0.55, 0.65), 0.3),
    "Asfalto": ((0.12, 0.12, 0.13), 0.85), "Pintura": ((0.95, 0.95, 0.95), 0.6), "Casco": ((0.97, 0.97, 0.97), 0.25),
    "Ceramica": ((0.97, 0.97, 0.96), 0.15), "Cromo": ((0.80, 0.80, 0.82), 0.1), "Luz": ((1.0, 0.85, 0.55), 0.5),
    "Concreto": ((0.60, 0.58, 0.55), 0.85), "Abismo": ((0.004, 0.045, 0.085), 0.9),
}


def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(nombre):
    if nombre in bpy.data.materials:
        return bpy.data.materials[nombre]
    color, rough = PALETA.get(nombre, ((0.8, 0.8, 0.8), 0.7))
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1)
        bsdf.inputs["Roughness"].default_value = rough
        if nombre in ("Metal", "Laton", "Cromo", "MetalOscuro"):
            bsdf.inputs["Metallic"].default_value = 1.0
    m.diffuse_color = (*color, 1)
    return m


def asignar(obj, nombre):
    obj.data.materials.clear()
    obj.data.materials.append(material(nombre))
    return obj


def _activo(obj):
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)


def caja(nombre, cx, cy, cz, sx, sy, sz, mat, rot_z=0.0, bisel=0.0):
    """Caja con CENTRO en (cx, cy, cz) y tamaño (sx, sy, sz) en metros."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz), rotation=(0, 0, rot_z))
    o = bpy.context.active_object
    o.name = nombre
    o.scale = (sx, sy, sz)
    aplicar(o)
    if bisel > 0:
        m = o.modifiers.new("bisel", "BEVEL")
        m.width = bisel
        m.segments = 2
        m.limit_method = "ANGLE"
        aplicar_mods(o)
    return asignar(o, mat)


def cilindro(nombre, cx, cy, cz, radio, alto, mat, lados=24, radio_arriba=None, rot=(0, 0, 0)):
    if radio_arriba is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=lados, radius=radio, depth=alto, location=(cx, cy, cz), rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=radio, radius2=radio_arriba, depth=alto,
                                        location=(cx, cy, cz), rotation=rot)
    o = bpy.context.active_object
    o.name = nombre
    return asignar(o, mat)


def esfera(nombre, cx, cy, cz, rx, ry, rz, mat, sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1, location=(cx, cy, cz))
    o = bpy.context.active_object
    o.name = nombre
    o.scale = (rx, ry, rz)
    aplicar(o)
    return asignar(o, mat)


def aplicar(o):
    _activo(o)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def aplicar_mods(o):
    _activo(o)
    for m in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


def unir(objs, nombre):
    """Junta varios objetos en uno (conserva los slots de material)."""
    objs = [o for o in objs if o is not None]
    for o in bpy.context.selected_objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.active_object
    o.name = nombre
    return o


def suave(o):
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def mover(o, dx, dy, dz, rot_z=0.0, escala=1.0):
    o.matrix_world = Matrix.Translation((dx, dy, dz)) @ Matrix.Rotation(rot_z, 4, "Z") @ Matrix.Scale(escala, 4) @ o.matrix_world
    return o


def copiar(o):
    c = o.copy()
    c.data = o.data.copy()
    bpy.context.collection.objects.link(c)
    return c


def origen_al_piso(o):
    """Pivote al centro abajo (así se apoya en el suelo en Unreal)."""
    xs = [v.co.x for v in o.data.vertices]
    ys = [v.co.y for v in o.data.vertices]
    zs = [v.co.z for v in o.data.vertices]
    c = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(zs)))
    o.data.transform(Matrix.Translation(-c))
    o.location = (0, 0, 0)
    return o


def exportar(o, ruta):
    for x in bpy.context.selected_objects:
        x.select_set(False)
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    # Blender trabaja en metros; el FBX declara metros y Unreal convierte a centímetros solo
    bpy.ops.export_scene.fbx(filepath=str(ruta), use_selection=True, apply_unit_scale=False, global_scale=1.0,
                             apply_scale_options="FBX_SCALE_NONE", object_types={"MESH"},
                             mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False,
                             bake_anim=False, axis_forward="-Z", axis_up="Y")


def sembrar(semilla):
    random.seed(semilla)
    return random
