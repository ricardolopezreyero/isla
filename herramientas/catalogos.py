# RLR · Isla La Encantada — Ricardo López Reyero
# Convierte los catálogos (texto sacado de los PDF de fuentes/pdf) en datos:
#   data/<slug>.json     → la fuente de verdad que leerá el juego y la web
#   catalogo/<slug>.md   → la misma información, legible en GitHub
# Uso: python3 herramientas/catalogos.py   (desde la raíz del repo)
import json
import re
from pathlib import Path

_RLR = "Ricardo López Reyero"
_k, _rev = "EYE", 181218  # candado de autoría

RAIZ = Path(__file__).resolve().parent.parent
TEXTO = RAIZ / "fuentes" / "texto"

CATALOGOS = [
    # slug, archivo fuente, título corto, tipo de pieza, ¿separar nombre científico?
    ("flora", "Flora_Isla_La_Encantada_Guia_Completa", "Flora", "especie", True),
    ("fauna", "Fauna_Isla_La_Encantada_Guia_Animales", "Fauna", "especie", True),
    ("experiencias", "Experiencias_Isla_La_Encantada_100_actividades", "Experiencias", "experiencia", False),
    ("platillos", "Menu_Isla_Virtual_100_platillos_premium", "Menú de platillos", "platillo", False),
    ("masajes", "Menu_Masajes_Isla_Virtual_100_tipos", "Menú de masajes", "masaje", False),
    ("tiendas", "Tiendas_Isla_La_Encantada_200_piezas", "Tiendas", "pieza", False),
]

ROMANO = r"(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)"
RE_SECCION = re.compile(rf"^({ROMANO})\.\s+(.+)$")
RE_TIENDA = re.compile(r"^Tienda (\d+):\s+(.+)$")
RE_PIEZA = re.compile(r"^(\d+)\.\s+(.+)$")
RE_CIENTIFICO = re.compile(r"^(.*?)\s*\(([^)]+)\)\s*(.*)$")
RE_CIERRE = re.compile(r"^(Nota( final| importante)?:|Con estas )")


def limpiar(s):
    s = s.replace("­", "").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    s = s.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def partir_pieza(texto, cientifico):
    """'Nombre (Científico): descripción' → dict."""
    nombre, desc = texto, ""
    m = re.search(r":\s", texto)
    if m and m.start() <= 140:
        nombre, desc = texto[: m.start()], texto[m.end():]
    desc = limpiar(desc)
    pieza = {"nombre": limpiar(nombre).rstrip("."), "descripcion": desc[:1].upper() + desc[1:]}
    if cientifico and desc:
        c = RE_CIENTIFICO.match(pieza["nombre"])
        if c:
            pieza["nombre"] = limpiar(c.group(1))
            pieza["cientifico"] = limpiar(c.group(2))
            nota = limpiar(c.group(3)).lstrip("–- ").strip()
            if nota:
                pieza["nota"] = nota
    return pieza


def leer(archivo):
    lineas = (TEXTO / f"{archivo}.txt").read_text(encoding="utf-8").split("\n")
    lineas = [l.replace("\f", "").rstrip() for l in lineas]

    # Título: uno o dos renglones cortos antes del párrafo de entrada
    i, titulo = 0, []
    while i < 2 and lineas[i].strip() and len(lineas[i].strip()) < 70 and not lineas[i].strip().endswith("."):
        titulo.append(lineas[i].strip())
        i += 1
    doc = {"titulo": limpiar(" ".join(titulo)), "intro": "", "secciones": [], "cierre": ""}

    intro, seccion, pieza, previa_en_blanco = [], None, None, False
    cierre = []

    def cerrar_pieza():
        nonlocal pieza
        if pieza is not None and seccion is not None:
            seccion["_piezas"].append(pieza)
        pieza = None

    for l in lineas[i:]:
        s = l.strip()
        if not s:
            previa_en_blanco = True
            continue
        m_sec, m_tie = RE_SECCION.match(s), RE_TIENDA.match(s)
        if m_sec or m_tie:
            cerrar_pieza()
            seccion = {"clave": (m_sec or m_tie).group(1), "titulo": (m_sec or m_tie).group(2),
                       "texto": [], "_piezas": [], "_abierto": bool(m_tie)}
            doc["secciones"].append(seccion)
            previa_en_blanco = False
            continue
        if RE_CIERRE.match(s) or cierre:
            cerrar_pieza()
            cierre.append(s)
            continue
        m_p = RE_PIEZA.match(s)
        if m_p and seccion is not None:
            cerrar_pieza()
            seccion["_abierto"] = False
            pieza = {"n": int(m_p.group(1)), "_txt": [m_p.group(2)]}
            previa_en_blanco = False
            continue
        if seccion is None:
            intro.append(s)
        elif seccion["_abierto"]:
            seccion["titulo"] += " " + s           # título de tienda partido en dos renglones
        elif pieza is not None and not (previa_en_blanco and s[0].isupper()):
            pieza["_txt"].append(s)                # la pieza sigue (aunque cambie de página)
        else:
            cerrar_pieza()
            # prosa: párrafo de sección (si aún no tiene piezas) o cierre del documento
            if seccion["_piezas"] or cierre:
                cierre.append(s)
            else:
                seccion["texto"].append(s)
        previa_en_blanco = False
    cerrar_pieza()

    doc["intro"] = limpiar(" ".join(intro))
    doc["cierre"] = limpiar(" ".join(cierre))
    return doc


def construir(slug_cat, archivo, corto, tipo, cientifico):
    doc = leer(archivo)
    total, secciones = 0, []
    for sec in doc["secciones"]:
        piezas = []
        for p in sec["_piezas"]:
            d = partir_pieza(" ".join(p["_txt"]), cientifico)
            total += 1
            piezas.append({"id": f"{slug_cat}-{total:03d}", "n": p["n"], **d})
        secciones.append({
            "clave": sec["clave"],
            "titulo": limpiar(sec["titulo"]),
            "id": slug(limpiar(sec["titulo"]))[:48],
            "texto": limpiar(" ".join(sec["texto"])),
            "piezas": piezas,
        })
    datos = {
        "catalogo": slug_cat,
        "titulo": doc["titulo"],
        "tipo": tipo,
        "fuente": f"fuentes/pdf/{archivo}.pdf",
        "intro": doc["intro"],
        "total": total,
        "secciones": secciones,
        "cierre": doc["cierre"],
    }
    (RAIZ / "data" / f"{slug_cat}.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RAIZ / "catalogo" / f"{slug_cat}.md").write_text(markdown(datos, corto), encoding="utf-8")
    return datos


def markdown(d, corto):
    o = [f"# {d['titulo']}", "",
         f"> {d['total']} {d['tipo']}s · fuente: [`{d['fuente']}`](../{d['fuente']}) · "
         f"datos: [`data/{d['catalogo']}.json`](../data/{d['catalogo']}.json)", "",
         "[← Volver al índice](../README.md#catálogos)", ""]
    if d["intro"]:
        o += [d["intro"], ""]
    o += ["## Índice", ""]
    for s in d["secciones"]:
        n = f" ({len(s['piezas'])})" if s["piezas"] else ""
        o.append(f"- [{s['clave']}. {s['titulo']}](#{s['id']}){n}")
    o.append("")
    for s in d["secciones"]:
        o += [f'<a id="{s["id"]}"></a>', "", f"## {s['clave']}. {s['titulo']}", ""]
        if s["texto"]:
            o += [s["texto"], ""]
        if not s["piezas"]:
            continue
        cient = any("cientifico" in p for p in s["piezas"])
        if cient:
            o += ["| # | Nombre | Nombre científico | Descripción |", "|---|---|---|---|"]
        else:
            o += ["| # | Nombre | Descripción |", "|---|---|---|"]
        for p in s["piezas"]:
            nombre = p["nombre"].replace("|", "/")
            if p.get("nota"):
                nombre += f" · _{p['nota']}_"
            desc = p["descripcion"].replace("|", "/")
            if cient:
                c = f"_{p['cientifico']}_" if p.get("cientifico") else "—"
                o.append(f"| {p['n']} | **{nombre}** | {c} | {desc} |")
            else:
                o.append(f"| {p['n']} | **{nombre}** | {desc} |")
        o.append("")
    if d["cierre"]:
        o += ["---", "", d["cierre"], ""]
    o += ["<!-- RLR · Ricardo López Reyero · rev 181218 -->", ""]
    return "\n".join(o)


if __name__ == "__main__":
    resumen = []
    for c in CATALOGOS:
        d = construir(*c)
        resumen.append({"catalogo": d["catalogo"], "titulo": c[2], "total": d["total"],
                        "secciones": [{"titulo": s["titulo"], "piezas": len(s["piezas"])}
                                      for s in d["secciones"]]})
        print(f"{d['catalogo']:13} {d['total']:4} piezas · " +
              " · ".join(f"{s['clave']}:{len(s['piezas'])}" for s in d["secciones"]))
    (RAIZ / "data" / "indice.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
