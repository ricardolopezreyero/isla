# RLR · Isla La Encantada — render de revisión: alinea objetos y saca una foto (para revisar sin Unreal)
# uso: blender -b --factory-startup -P render_prueba.py -- salida.png modulo:funcion[:args] ...
import sys, math
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import bpy
from mathutils import Vector
from comun import limpiar, mover, caja
args = sys.argv[sys.argv.index("--") + 1:]
salida, specs = args[0], args[1:]
limpiar()
x = 0.0
objs = []
for sp in specs:
    mod, fn, *rest = sp.split(":")
    m = __import__(mod)
    kw = eval("dict(" + (rest[0] if rest else "") + ")")
    o = getattr(m, fn)(**kw)
    xs = [v.co.x for v in o.data.vertices]; w = max(xs) - min(xs)
    mover(o, x + w / 2 - (max(xs) + min(xs)) / 2, 0, 0)
    x += w + 1.5
    objs.append(o)
piso = caja("piso", x / 2, 0, -0.05, x + 30, 60, 0.1, "Arena")
alto = max(max(v.co.z for v in o.data.vertices) for o in objs)
scn = bpy.context.scene
scn.render.engine = "BLENDER_EEVEE"
scn.render.resolution_x, scn.render.resolution_y = 1400, 800
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scn.collection.objects.link(cam); scn.camera = cam
d = max(x, alto * 1.6)
cam.location = (x * 0.75, -d * 0.9, alto * 0.6 + d * 0.45)
cam.rotation_euler = (math.radians(62), 0, math.radians(18))
cam.data.lens = 35
sol = bpy.data.objects.new("sol", bpy.data.lights.new("sol", "SUN")); scn.collection.objects.link(sol)
sol.rotation_euler = (math.radians(50), math.radians(10), math.radians(30)); sol.data.energy = 4
w = bpy.data.worlds.new("w"); scn.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.7, 0.9, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.8
scn.view_settings.view_transform = "AgX"
scn.render.filepath = salida
bpy.ops.render.render(write_still=True)
print("RENDER", salida, sum(len(o.data.polygons) for o in objs), "caras")
