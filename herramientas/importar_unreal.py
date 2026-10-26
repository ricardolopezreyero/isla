# RLR · Isla La Encantada — Ricardo López Reyero
# Importa a Unreal la biblioteca hecha en casa (unreal/fuentes/objetos/*.fbx, salida de herramientas/blender/fabrica.py):
#   1. Un material por color de la paleta (MI_<nombre>, hijo de M_Isla; el agua es hija de M_Agua).
#   2. Cada FBX a /Game/Isla/Objetos con sus slots apuntando a esos materiales y Nanite donde aplica.
# Unreal debe estar abierto (servidor MCP). Uso: python3 herramientas/importar_unreal.py [SM_Nombre ...]
import ast
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from greybox_unreal import conectar, guion   # noqa: E402

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent
FBX = RAIZ / "unreal" / "fuentes" / "objetos"
CARPETA_MI = "/Game/Isla/Materiales/Paleta"
# Lo que se camina: sin Nanite y con colisión exacta (Nanite usaría una malla simplificada para chocar)
CAMINABLES = {"SM_Terreno", "SM_Caminos", "SM_EdificioHotel", "SM_Villa", "SM_VillaHorizonte", "SM_Restaurante", "SM_Lobby",
              "SM_Tienda", "SM_Spa", "SM_CabinaSpa", "SM_SuiteMuestra", "SM_MuelleTramo", "SM_Pista", "SM_Palapa",
              "SM_EdificioStaff", "SM_Hangar"}
AGUAS = {"Agua": (0.02, 0.38, 0.48, 0.62), "AguaAlberca": (0.05, 0.62, 0.72, 0.45)}
# Colores con textura fotográfica (los arma herramientas/materiales_unreal.py texturas): aquí no se tocan
TEXTURIZADOS = ["Arena", "ArenaMojada", "Pasto", "PastoSeco", "Selva", "Volcan", "Roca", "RocaVolcanica", "Madera",
                "MaderaClara", "MaderaOscura", "Estuco", "EstucoArena", "Piedra", "PiedraOscura", "Concreto"]
METAL = {"Metal": 0.9, "Laton": 1.0, "Cromo": 1.0, "MetalOscuro": 0.7, "Vidrio": 0.35}
EMISIVO = {"Luz": 6.0}


def paleta():
    src = (RAIZ / "herramientas" / "blender" / "comun.py").read_text(encoding="utf-8")
    nodo = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "PALETA")
    return ast.literal_eval(nodo.value)


COMUN = '''
import json
def X(n, a): return execute_tool(n, json.dumps(a))
AS = "editor_toolset.toolsets.asset.AssetTools."
MI = "editor_toolset.toolsets.material_instance.MaterialInstanceTools."
SM = "editor_toolset.toolsets.static_mesh.StaticMeshTools."
'''

MATERIALES = COMUN + '''
P = json.loads(%s)
def run():
    X(AS + "create_folder", {"path": "%s"})
    hechos = []
    for nombre, d in P.items():
        path = "%s/MI_" + nombre
        ref = {"refPath": path + ".MI_" + nombre}
        padre = ("/Game/Isla/Materiales/M_Agua.M_Agua" if d["agua"] else
                 "/Game/Isla/Materiales/M_Vidrio.M_Vidrio" if nombre == "Vidrio" else "/Game/Isla/Materiales/M_Isla.M_Isla")
        existe = X(AS + "exists", {"path": path})["returnValue"]
        if existe and d.get("texturizado"):
            continue
        if not existe:
            X(MI + "create", {"folder_path": "%s", "asset_name": "MI_" + nombre, "parent": {"refPath": padre}})
        r, g, b = d["color"]
        if nombre == "Vidrio":
            X(MI + "set_parent", {"instance": ref, "parent": {"refPath": padre}})
            hechos.append(nombre)
            continue
        if not d["agua"]:
            X(MI + "set_vector_parameter", {"instance": ref, "name": "Color", "value": {"r": r, "g": g, "b": b, "a": 1}})
        X(MI + "set_scalar_parameter", {"instance": ref, "name": "Roughness", "value": d["rough"]})
        if d["agua"]:
            pass   # el agua toma color y opacidad de la profundidad (M_Agua)
        else:
            X(MI + "set_scalar_parameter", {"instance": ref, "name": "Metallic", "value": d["metal"]})
            X(MI + "set_scalar_parameter", {"instance": ref, "name": "Emisivo", "value": d["emisivo"]})
        hechos.append(nombre)
    X(AS + "save_assets", {"asset_paths": ["%s/MI_" + n for n in hechos]})
    return {"materiales": len(hechos)}
'''

IMPORTAR = COMUN + '''
NOMBRE, FUENTE, NANITE, CAMINABLE = %s, %s, %s, %s
O = "editor_toolset.toolsets.object.ObjectTools."
def run():
    path = "/Game/Isla/Objetos/" + NOMBRE
    # Si ya existe: sin uso se borra; en uso se aparta como __viejo (luego se reconstruye la zona y se limpia con --limpiar)
    if X(AS + "exists", {"path": path})["returnValue"]:
        if X(AS + "get_referencers", {"asset_path": path})["returnValue"]:
            viejo = path + "__viejo"
            if X(AS + "exists", {"path": viejo})["returnValue"]:
                X(AS + "delete", {"path": viejo})
            X(AS + "move", {"path": path, "new_path": viejo})
            # el nivel cargado ya apunta a __viejo: se guarda y se borra el redirector que dejó la mudanza
            X(AS + "save_assets", {"asset_paths": X(AS + "get_referencers", {"asset_path": path})["returnValue"]})
            X(AS + "delete", {"path": path})
        else:
            X(AS + "delete", {"path": path})
    import time
    for intento in range(8):              # el registro de assets tarda un instante en soltar el nombre borrado
        try:
            X(SM + "import_file", {"folder_path": "/Game/Isla/Objetos", "asset_name": NOMBRE, "source_file": FUENTE,
                                    "import_materials": False, "import_textures": False, "combine_meshes": True})
            break
        except RuntimeError:
            if intento == 7:
                raise
            time.sleep(1.5)
    mesh = {"refPath": path + "." + NOMBRE}
    slots = X(SM + "get_material_slots", {"mesh": mesh})["returnValue"]
    for s in slots:
        base = s.split("_")[0] if s not in %s else s
        X(SM + "set_material", {"mesh": mesh, "slot_name": s, "material": {"refPath": "%s/MI_%%s.MI_%%s" %% (base, base)}})
    transparente = any(s.split("_")[0] in ("Vidrio", "Agua", "AguaAlberca") for s in slots)
    X(SM + "set_nanite_enabled", {"mesh": mesh, "enabled": NANITE and not CAMINABLE and not transparente})
    if CAMINABLE:
        body = json.loads(X(O + "get_properties", {"instance": mesh, "properties": ["bodySetup"]})["returnValue"])["bodySetup"]
        X(O + "set_properties", {"instance": body, "values": json.dumps({"collisionTraceFlag": "CTF_UseComplexAsSimple"})})
    X(AS + "save_assets", {"asset_paths": [path]})
    return {"malla": NOMBRE, "slots": len(slots), "caras": X(SM + "get_triangle_count", {"mesh": mesh, "lod_index": 0})["returnValue"]}
'''


LIMPIAR = COMUN + '''
def run():
    n = []
    todos = X(AS + "find_assets", {"folder_path": "/Game/Isla/Objetos", "name": "", "asset_type": None, "recursive": True, "tags": {}})["returnValue"]
    for a in [t for t in todos if t.endswith("__viejo")]:
        if not X(AS + "get_referencers", {"asset_path": a})["returnValue"]:
            X(AS + "delete", {"path": a}); n.append(a)
    return {"borrados": n}
'''


def main():
    pal = paleta()
    datos = {n: {"color": c, "rough": r, "agua": n in AGUAS, "metal": METAL.get(n, 0.0), "emisivo": EMISIVO.get(n, 0.0),
                 "opacidad": AGUAS.get(n, (0, 0, 0, 1))[3], "texturizado": n in TEXTURIZADOS} for n, (c, r) in pal.items()}
    for n, (r, g, b, _) in AGUAS.items():
        datos[n]["color"] = (r, g, b)
    pedidos = sys.argv[1:]
    solo_materiales = pedidos == ["--materiales"]
    conectar()
    if pedidos == ["--limpiar"]:
        print(guion(LIMPIAR))
        return
    if not pedidos or solo_materiales:
        print("materiales:", guion(MATERIALES % (json.dumps(json.dumps(datos)), CARPETA_MI, CARPETA_MI, CARPETA_MI, CARPETA_MI)))
    if solo_materiales:
        return
    nombres = list(pal.keys())
    for f in sorted(FBX.glob("SM_*.fbx")):
        if pedidos and f.stem not in pedidos:
            continue
        con_agua = f.stem in ("SM_Villa", "SM_VillaHorizonte", "SM_Restaurante", "SM_Lobby", "SM_Spa", "SM_SuiteMuestra")
        r = guion(IMPORTAR % (json.dumps(f.stem), json.dumps(str(f)), repr(not con_agua), repr(f.stem in CAMINABLES), json.dumps(nombres), CARPETA_MI))
        print(r)


if __name__ == "__main__":
    main()
