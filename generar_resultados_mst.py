import subprocess
from pathlib import Path
from grafos import asignar_pesos
from validando_MST import (obtener_generadores,generar_conexo)
import csv
import matplotlib.pyplot as plt

RUTA_BASE = Path(__file__).resolve().parent / "resultados_4"



def generar_imagen(archivo_gv, motor="sfdp", formato="png", n=30):
    archivo_gv = Path(archivo_gv)
    if not archivo_gv.is_file():
        raise FileNotFoundError(archivo_gv)
    archivo_salida = archivo_gv.with_suffix(f".{formato}")
    comando = [motor,f"-T{formato}"]
    if formato == "png":
        if n >= 100:
            tamano = "24,16!"
            dpi = 400
        else:
            tamano = "14,10!"
            dpi = 400
        comando.extend([
            f"-Gsize={tamano}",
            f"-Gdpi={dpi}"
        ])
    if n >= 100:
        comando.extend([
            "-Nshape=point",
            "-Nwidth=0.10",
            "-Nlabel=",
            "-Efontsize=8"
        ])
    else:
        comando.extend([
            "-Nshape=circle",
            "-Nfontsize=10",
            "-Granksep=0.3",
            "-Gnodesep=0.2"
        ])
    if motor == "dot":
        comando.extend([
            "-Grankdir=TB",
            "-Granksep=1.1",
            "-Gnodesep=0.35",
            "-Gsplines=polyline",
            "-Goutputorder=edgesfirst"])    
    comando.extend([str(archivo_gv),"-o",str(archivo_salida)])
    subprocess.run(comando, check=True)
    return archivo_salida


def guardar_resumen_mst(ruta, nombre, n, semilla, intentos, datos):
    filas = [
        [algoritmo, peso, mst.obtener_numero_aristas()]
        for algoritmo, mst, peso in datos
    ]
    archivo_csv = ruta / "resumen_mst.csv"
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow([
            "Algoritmo", "Peso MST", "Aristas",
            "Nodos", "Semilla", "Intentos"
        ])
        for algoritmo, peso, aristas in filas:
            escritor.writerow([
                algoritmo, peso, aristas,
                n, semilla, intentos
            ])
    fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
    ax.axis("off")
    fig.suptitle(
        f"Árbol de expansión mínima — {nombre}",
        fontsize=12,
        fontweight="bold",
        y=0.95
    )
    ax.set_title(
        f"Nodos: {n} | Semilla: {semilla} | Intentos: {intentos}",
        fontsize=8,
        pad=15
    )
    tabla = ax.table(
        cellText=filas,
        colLabels=["Algoritmo", "Peso total MST", "Aristas"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.46, 0.30, 0.24]
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1, 2.2)
    pesos = [peso for _, _, peso in datos]
    mensaje = (
        "Los tres algoritmos coinciden"
        if len(set(pesos)) == 1
        else "ADVERTENCIA: Los pesos no coinciden"
    )
    ax.text(
        0.5, 0.10, mensaje,
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        fontweight="bold"
    )
    archivo_png = ruta / "resumen_mst.png"
    fig.savefig(
        archivo_png,
        dpi=200,
        bbox_inches="tight"
    )
    plt.close(fig)
    print(f"Resumen generado: {archivo_png}")

def guardar_resultados_mst(grafo, nombre, n, semilla, intentos):
    ruta = RUTA_BASE / nombre / f"{n}_nodos"
    ruta.mkdir(parents=True, exist_ok=True)
    s = next(iter(grafo.nodos))
    mst_kruskal, peso_k = grafo.Kruskal()
    mst_inverso, peso_i = grafo.Kruskal_Inverso()
    mst_prim, peso_p = grafo.Prim(s)
    # Comprobamos que coincidan los pesos 
    assert peso_k == peso_i == peso_p
    # Guardamos los grafos
    resultados = {
        "original": grafo,
        "kruskal": mst_kruskal,
        "kruskal_inverso": mst_inverso,
        "prim": mst_prim
    }
    for algoritmo, resultado in resultados.items():
        archivo_gv = ruta / f"{algoritmo}.gv"
        resultado.guardar_gv(archivo_gv)
        motor = "sfdp" if algoritmo == "original" else "dot"
        generar_imagen(archivo_gv,motor=motor,formato="png",n=n)
        if n >= 100 and algoritmo != "original":
            generar_imagen(archivo_gv,motor=motor,formato="svg",n=n)
        print(f"Archivos generados: {algoritmo}")
        print(f"Peso total del MST: {peso_k}")
    datos_mst = [
        ("Kruskal directo", mst_kruskal, peso_k),
        ("Kruskal inverso", mst_inverso, peso_i),
        ("Prim", mst_prim, peso_p)
    ]
    guardar_resumen_mst(ruta,nombre,n,semilla,intentos,datos_mst)
    print(f"Peso total del MST: {peso_k}")


def generar_todos_los_resultados():
    TAMAÑOS = [30, 500]
    SEMILLA = 42
    for n in TAMAÑOS:
        generadores = obtener_generadores(n)
        for nombre, generador in generadores.items():
            grafo, semilla, intentos = generar_conexo(generador,semilla_base=SEMILLA,max_intentos=100)
            # Asignamos pesos reproducibles
            grafo = asignar_pesos(grafo,peso_min=1,peso_max=10,semilla=SEMILLA)
            # Ejecutamos los MST y generamos archivos
            guardar_resultados_mst(grafo,nombre,n,semilla,intentos)
            print(
                f"\nModelo: {nombre} | "
                f"Nodos: {n} | "
                f"Semilla: {semilla} | "
                f"Intentos: {intentos}"
            )
    print("\nGeneración terminada correctamente.")
if __name__ == "__main__":
    generar_todos_los_resultados()
