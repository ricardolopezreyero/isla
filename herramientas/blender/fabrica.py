# RLR · Isla La Encantada — Ricardo López Reyero
# Fábrica de objetos: genera en Blender toda la biblioteca de la isla y la exporta a FBX.
# Todo es código: cambiar una medida = cambiar la función y volver a correr.
# Uso: blender -b --factory-startup -P herramientas/blender/fabrica.py -- [nombre ...]
#      (sin nombres exporta todo; los FBX quedan en unreal/fuentes/objetos/)
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arquitectura as A   # noqa: E402
import muebles as M        # noqa: E402
import naturaleza as N     # noqa: E402
import terreno as T        # noqa: E402
from comun import exportar, limpiar   # noqa: E402

_RLR = "Ricardo López Reyero"
SALIDA = Path(__file__).resolve().parents[2] / "unreal" / "fuentes" / "objetos"

BIBLIOTECA = {
    # Naturaleza (catalogo/flora.md)
    "SM_PalmaCocotera_1": lambda: N.palma_cocotera(1, 14, 2.5),
    "SM_PalmaCocotera_2": lambda: N.palma_cocotera(2, 11, 4.0),
    "SM_PalmaCocotera_3": lambda: N.palma_cocotera(3, 17, 3.0),
    "SM_PalmaCocotera_4": lambda: N.palma_cocotera(4, 9, 1.0),
    "SM_PalmaReal_1": lambda: N.palma_real(1, 18),
    "SM_PalmaReal_2": lambda: N.palma_real(2, 14),
    "SM_Almendro_1": lambda: N.almendro(1),
    "SM_Ceiba_1": lambda: N.ceiba(1),
    "SM_Buganvilia": lambda: N.arbusto_flor(1, "Flor"),
    "SM_Hibisco": lambda: N.arbusto_flor(2, "FlorRoja"),
    "SM_Plumeria": lambda: N.arbusto_flor(3, "FlorBlanca", 2.8, 2.4),
    "SM_Roca_1": lambda: N.roca(1, 4.0, 2.5),
    "SM_Roca_2": lambda: N.roca(2, 7.0, 4.0),
    "SM_Roca_3": lambda: N.roca(3, 12.0, 9.0, "Roca"),
    "SM_PastoPlaya": lambda: N.pasto_playa(1),
    "SM_Agave": lambda: N.agave(1), "SM_Heliconia": lambda: N.heliconia(1),
    "SM_Helecho": lambda: N.helecho(1), "SM_Platanera": lambda: N.platanera(1),
    # Playa, alberca y muebles (biblia §4–8)
    "SM_Camastro": M.camastro, "SM_SombrillaPalma": M.sombrilla_palma, "SM_SombrillaTela": M.sombrilla_tela,
    "SM_Palapa": M.palapa, "SM_Farol": M.farol, "SM_LuzPiso": M.luz_piso, "SM_Banca": M.banca, "SM_Kayak": M.kayak,
    "SM_CamaKing": M.cama_king, "SM_Sofa3": M.sofa3, "SM_MesaComedor4": lambda: M.mesa_comedor(4),
    "SM_DobleLavabo": M.doble_lavabo, "SM_Regadera": M.regadera, "SM_WCWashlet": M.wc_washlet, "SM_Tina": M.tina,
    "SM_MesaRestaurante": M.mesa_restaurante, "SM_Barra": M.barra_bar,
    # Arquitectura y mar
    "SM_EdificioHotel": A.edificio_hotel, "SM_Villa": A.villa, "SM_VillaHorizonte": A.villa_horizonte,
    "SM_Restaurante": A.restaurante, "SM_Lobby": A.lobby, "SM_Tienda": A.tienda, "SM_CabinaSpa": A.cabina_spa,
    "SM_Spa": A.spa, "SM_EdificioStaff": A.edificio_staff, "SM_SuiteMuestra": A.suite_muestra,
    "SM_MuelleTramo": A.muelle_tramo, "SM_Yate": A.yate, "SM_Hidroavion": A.hidroavion, "SM_Pista": A.pista,
    "SM_Hangar": A.hangar, "SM_BarPlaya": A.bar_playa, "SM_MiradorCrater": A.mirador_crater,
    "SM_ClubNautico": A.club_nautico, "SM_AlbercaPrincipal": A.alberca_principal,
    # Terreno de 4.8 × 4.8 km con celdas de 8 m
    "SM_Terreno": lambda: T.terreno(4800.0, 600),
    # Red de caminos del plano (correr antes: python3 herramientas/plano_isla.py)
    "SM_Caminos": lambda: T.caminos(str(Path(__file__).resolve().parents[2] / "data" / "plano_isla.json")),
}

if __name__ == "__main__":
    pedidos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, fn in BIBLIOTECA.items():
        if pedidos and nombre not in pedidos:
            continue
        t = time.time()
        limpiar()
        o = fn()
        o.name = nombre
        exportar(o, SALIDA / f"{nombre}.fbx")
        mats = sorted({m.name for m in o.data.materials})
        print(f"FABRICADO {nombre} · {len(o.data.polygons)} caras · {len(mats)} materiales · {time.time() - t:.1f} s · {','.join(mats)}")
