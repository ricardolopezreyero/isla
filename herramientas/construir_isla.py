# RLR · Isla La Encantada — Ricardo López Reyero
# Construye data/plano_isla.json (salida de herramientas/plano_isla.py) dentro de Unreal, nivel L_Isla,
# por el servidor MCP del editor. Borra la carpeta «Isla» del esquematizador y levanta todo de nuevo.
# Requisitos: Unreal abierto con L_Isla y la biblioteca importada (herramientas/importar_unreal.py).
# Uso: python3 herramientas/construir_isla.py            → toda la isla
#      python3 herramientas/construir_isla.py Vegetacion → sólo una zona
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from greybox_unreal import AJUSTES, BORRAR, COMUN, MALLAS, conectar, guion   # noqa: E402

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218

RAIZ = Path(__file__).resolve().parent.parent
LOTE = 80
MATS = "/Game/Isla/Materiales/Paleta/MI_{0}.MI_{0}"

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
        elif p["forma"] == "Malla":
            a = X(S + "add_to_scene_from_asset", {"asset_path": p["asset"], "name": p["nombre"],
                  "xform": {"location": loc, "rotation": rot, "scale": {"x": p["sx"], "y": p["sy"], "z": p["sz"]}}})["returnValue"]
        else:
            a = X(S + "add_to_scene_from_asset", {"asset_path": MALLAS[p["forma"]], "name": p["nombre"],
                  "xform": {"location": loc, "rotation": rot, "scale": {"x": p["sx"], "y": p["sy"], "z": p["sz"]}}})["returnValue"]
            c = X(A + "get_components", {"actor": a, "component_type": {"refPath": "/Script/Engine.StaticMeshComponent"}})["returnValue"][0]
            X(O + "set_properties", {"instance": c, "values": json.dumps({"overrideMaterials": [{"refPath": MATS.format(p["mat"])}]})})
        X(S + "set_actor_folder", {"actor": a, "folder_path": "Isla/" + p["zona"]})
        hechos += 1
    return {"hechos": hechos}
'''


def main():
    plano = json.loads((RAIZ / "data" / "plano_isla.json").read_text(encoding="utf-8"))
    zona = sys.argv[1] if len(sys.argv) > 1 else None
    piezas = [p for p in plano["piezas"] if not zona or p["zona"] == zona]
    conectar()
    print("borrar:", guion(BORRAR % json.dumps("Isla" + ("/" + zona if zona else ""))), flush=True)
    for i in range(0, len(piezas), LOTE):
        r = guion(CONSTRUIR % (json.dumps(json.dumps(piezas[i:i + LOTE], ensure_ascii=False)), json.dumps(MALLAS), json.dumps(MATS)))
        print(f"lote {i // LOTE + 1}/{(len(piezas) + LOTE - 1) // LOTE}: {r}", flush=True)
    if not zona:
        print("ajustes:", guion(AJUSTES % json.dumps(json.dumps(plano))), flush=True)
    if True:
        print("guardar:", guion(COMUN + '''
def run():
    return X("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": ["/Game/Isla/Mapas/L_Isla"]})
'''), flush=True)


if __name__ == "__main__":
    main()
