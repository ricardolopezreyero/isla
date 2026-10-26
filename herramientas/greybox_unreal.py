# RLR · Isla La Encantada — Ricardo López Reyero
# Construye data/greybox_isla.json dentro de Unreal (nivel L_Isla) usando el servidor MCP del editor
# (plugin Unreal MCP, http://localhost:8000/mcp; ver docs/04-unreal.md §9). Unreal debe estar abierto.
#
# Es idempotente: antes de construir borra todo lo que esté en la carpeta «Isla» del esquematizador.
# Uso: python3 herramientas/greybox_unreal.py            → borra y construye todo
#      python3 herramientas/greybox_unreal.py Villas     → sólo reconstruye una zona
import json
import sys
import urllib.request
from pathlib import Path

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent
URL = "http://localhost:8000/mcp"
LOTE = 60
MALLAS = {"Cubo": "/Engine/BasicShapes/Cube.Cube", "Cilindro": "/Engine/BasicShapes/Cylinder.Cylinder",
          "Cono": "/Engine/BasicShapes/Cone.Cone", "Esfera": "/Engine/BasicShapes/Sphere.Sphere",
          "Plano": "/Engine/BasicShapes/Plane.Plane"}
MATS = "/Game/Isla/Greybox/Materiales/MI_{0}.MI_{0}"
SESION = None


def mcp(metodo, params=None, id_=1):
    global SESION
    cuerpo = {"jsonrpc": "2.0", "method": metodo}
    if id_ is not None:
        cuerpo["id"] = id_
    if params is not None:
        cuerpo["params"] = params
    req = urllib.request.Request(URL, data=json.dumps(cuerpo).encode(), method="POST", headers={
        "content-type": "application/json", "accept": "application/json, text/event-stream",
        **({"Mcp-Session-Id": SESION} if SESION else {})})
    with urllib.request.urlopen(req, timeout=900) as r:
        SESION = r.headers.get("Mcp-Session-Id") or SESION
        texto = r.read().decode()
    return json.loads(texto) if texto.strip() else None


def conectar():
    mcp("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "greybox_isla", "version": "1"}})
    mcp("notifications/initialized", id_=None)


def guion(script):
    """Corre un guion en el sandbox de Unreal (execute_tool_script) y devuelve lo que regresa run()."""
    r = mcp("tools/call", {"name": "call_tool", "arguments": {
        "toolset_name": "editor_toolset.toolsets.programmatic.ProgrammaticToolset",
        "tool_name": "execute_tool_script", "arguments": {"script": script}}})
    texto = r["result"]["content"][0]["text"]
    try:
        valor = json.loads(texto)["returnValue"]
        return json.loads(valor) if isinstance(valor, str) else valor
    except (ValueError, KeyError):
        raise RuntimeError(texto[:2000])


COMUN = '''
import json
def X(n, a): return execute_tool(n, json.dumps(a))
S = "editor_toolset.toolsets.scene.SceneTools."
A = "editor_toolset.toolsets.actor.ActorTools."
O = "editor_toolset.toolsets.object.ObjectTools."
'''

BORRAR = COMUN + '''
CARPETA = %s
def run():
    n = 0
    if CARPETA not in [str(f) for f in X(S + "get_folders", {})["returnValue"]]:
        return {"borrados": 0}
    for a in X(S + "get_actors_in_folder", {"folder_path": CARPETA, "recursive": True})["returnValue"]:
        X(S + "remove_from_scene", {"actor": a}); n += 1
    return {"borrados": n}
'''

CONSTRUIR = COMUN + '''
PIEZAS = json.loads(%s)
MALLAS = %s
MATS = %s
def run():
    hechos = 0
    for p in PIEZAS:
        loc = {"x": p["x"] * 100, "y": p["y"] * 100, "z": p["z"] * 100}
        rot = {"pitch": 0, "yaw": p.get("yaw", 0), "roll": 0}
        if p["forma"] == "Texto":
            a = X(S + "add_to_scene_from_class", {"actor_type": {"refPath": "/Script/Engine.TextRenderActor"},
                  "name": p["nombre"], "xform": {"location": loc, "rotation": rot}})["returnValue"]
            c = X(A + "get_components", {"actor": a, "component_type": {"refPath": "/Script/Engine.TextRenderComponent"}})["returnValue"][0]
            X(O + "set_properties", {"instance": c, "values": json.dumps({"text": p["texto"], "worldSize": p["tam"] * 100,
                  "horizontalAlignment": "EHTA_Center", "verticalAlignment": "EVRTA_TextCenter"})})
        else:
            a = X(S + "add_to_scene_from_asset", {"asset_path": MALLAS[p["forma"]], "name": p["nombre"],
                  "xform": {"location": loc, "rotation": rot, "scale": {"x": p["sx"], "y": p["sy"], "z": p["sz"]}}})["returnValue"]
            c = X(A + "get_components", {"actor": a, "component_type": {"refPath": "/Script/Engine.StaticMeshComponent"}})["returnValue"][0]
            X(O + "set_properties", {"instance": c, "values": json.dumps({"overrideMaterials": [{"refPath": MATS.format(p["mat"])}]})})
        X(A + "set_label", {"actor": a, "label": p["nombre"]})
        X(S + "set_actor_folder", {"actor": a, "folder_path": "Isla/" + p["zona"]})
        hechos += 1
    return {"hechos": hechos}
'''

AJUSTES = COMUN + '''
J = json.loads(%s)
def run():
    out = {}
    for a in X(S + "find_actors", {"name": "", "tag": "", "collision_channels": []})["returnValue"]:
        nombre = a["refPath"].split(".")[-1]
        if nombre.startswith("PlayerStart"):
            X(A + "set_actor_transform", {"actor": a, "worldspace": True, "xform": {
                "location": {"x": J["jugador"]["x"] * 100, "y": J["jugador"]["y"] * 100, "z": J["jugador"]["z"] * 100 + 100},
                "rotation": {"pitch": 0, "yaw": J["jugador"]["yaw"], "roll": 0}}})
            out["jugador"] = True
        elif nombre.startswith("DirectionalLight"):
            X(A + "set_actor_transform", {"actor": a, "worldspace": True, "xform": {
                "rotation": {"pitch": J["sol"]["pitch"], "yaw": J["sol"]["yaw"], "roll": 0}}})
            out["sol"] = True
        elif nombre.startswith("Floor"):
            X(S + "remove_from_scene", {"actor": a})
            out["piso_plantilla"] = "quitado"
    return out
'''


def main():
    plano = json.loads((RAIZ / "data" / "greybox_isla.json").read_text(encoding="utf-8"))
    zona = sys.argv[1] if len(sys.argv) > 1 else None
    piezas = [p for p in plano["piezas"] if not zona or p["zona"] == zona]
    conectar()
    print("borrar:", guion(BORRAR % json.dumps("Isla" + ("/" + zona if zona else ""))))
    for i in range(0, len(piezas), LOTE):
        lote = piezas[i:i + LOTE]
        r = guion(CONSTRUIR % (json.dumps(json.dumps(lote, ensure_ascii=False)), json.dumps(MALLAS), json.dumps(MATS)))
        print(f"lote {i // LOTE + 1}: {r}")
    if not zona:
        print("ajustes:", guion(AJUSTES % json.dumps(json.dumps(plano))))


if __name__ == "__main__":
    main()
