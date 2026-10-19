import random
import subprocess
from pathlib import Path

from grafos import (
    grafo_malla,
    grafo_erdos_renyi,
    grafo_gilbert,
    grafo_geografico,
    grafo_barabasi_albert,
    grafo_dorogovtsev_mendes
)

RUTA_BASE = Path(__file__).resolve().parent / "resultados_2_prueba"
TAMANOS = [30, 100, 500]
SEMILLA = 42


def generar_imagen(archivo_gv, motor="sfdp", formato="png"):
    archivo_gv = Path(archivo_gv)
    if not archivo_gv.is_file():
        raise FileNotFoundError(archivo_gv)
    archivo_salida = archivo_gv.with_suffix(f".{formato}")
    comando = [
        motor,
        f"-T{formato}",
        "-Grankdir=TB",
    ]
    if motor == "sfdp":
        comando.extend([
            "-Nshape=point",
            "-Nwidth=0.10",
            "-Nlabel="
        ])
    else:
        comando.extend([
            "-Granksep=0.3",
            "-Gnodesep=0.2",
            "-Nshape=circle",
            "-Nfontsize=10"
        ])
    comando.extend([
        str(archivo_gv),
        "-o",
        str(archivo_salida)
    ])
    subprocess.run(comando, check=True)
    return archivo_salida
# Validar los arboles
def validar_arbol(arbol):
    V = arbol.obtener_numero_vertices()
    E = arbol.obtener_numero_aristas()
    if V == 0:
        return False
    s = next(iter(arbol.nodos.values()))
    recorrido = arbol.BFS(s)
    es_conexo = recorrido.obtener_numero_vertices() == V
    return es_conexo and E == V - 1


def validar_resultados(grafos):
    original = grafos["original"]
    for nombre in [
        "bfs",
        "dfs_recursivo",
        "dfs_iterativo"
    ]:
        arbol = grafos[nombre]
        if not validar_arbol(arbol):
            raise ValueError(f"Árbol inválido: {nombre}")
        if not arbol.aristas.issubset(original.aristas):
            raise ValueError(
                f"El árbol {nombre} contiene aristas ajenas al original"
            )
    if (
        grafos["dfs_recursivo"].aristas
        != grafos["dfs_iterativo"].aristas
    ):
        raise ValueError(
            "DFS recursivo e iterativo generaron árboles diferentes"
        )

    return True
# procesar los grafos
def procesar_grafo(grafo, s, ruta):

    ruta = Path(ruta)
    ruta.mkdir(parents=True, exist_ok=True)

    grafos = {
        "original": grafo,
        "bfs": grafo.BFS(s),
        "dfs_recursivo": grafo.DFS_R(s),
        "dfs_iterativo": grafo.DFS_I(s)
    }
    validar_resultados(grafos)
    for nombre, resultado in grafos.items():
        archivo_gv = ruta / f"{nombre}.gv"
        resultado.guardar_gv(archivo_gv)
        motor = "sfdp" if nombre == "original" else "dot"
        generar_imagen(
            archivo_gv,
            motor=motor,
            formato="png"
        )
        # SVG adicionales para árboles grandes
        if nombre != "original" and len(grafo.nodos) >= 100:
            generar_imagen(
                archivo_gv,
                motor="dot",
                formato="svg"
            )
    return grafos


# Generar modelos
def generar_todos_los_grafos():
    random.seed(SEMILLA)
    for n in TAMANOS:
        modelos = {
            "erdos_renyi": grafo_erdos_renyi(n, 3 * n),
            "gilbert": grafo_gilbert(n, 6 / (n - 1)),
            "geografico": grafo_geografico(
                n,
                {30: 0.30, 100: 0.18, 500: 0.09}[n]
            ),
            "barabasi_albert": grafo_barabasi_albert(n, 3),
            "dorogovtsev_mendes": grafo_dorogovtsev_mendes(n)
        }
        dimensiones = {
            30: (5, 6),
            100: (10, 10),
            500: (20, 25)
        }
        m, filas = dimensiones[n]
        modelos["malla"] = grafo_malla(m, filas)
        for nombre, grafo in modelos.items():
            if grafo is None:
                raise ValueError(
                    f"No fue posible generar {nombre} con {n} nodos"
                )
            s = next(iter(grafo.nodos.values()))
            ruta = RUTA_BASE / nombre / f"{n}_nodos"
            resultados = procesar_grafo(grafo, s, ruta)
            print(f"\n{nombre.upper()} | {n} nodos")
            print(
                "Aristas originales:",
                grafo.obtener_numero_aristas()
            )
            for algoritmo in [
                "bfs",
                "dfs_recursivo",
                "dfs_iterativo"
            ]:
                arbol = resultados[algoritmo]
                print(
                    f"{algoritmo}: "
                    f"{len(arbol.nodos)} nodos, "
                    f"{len(arbol.aristas)} aristas"
                )
#Ejecución
if __name__ == "__main__":

    generar_todos_los_grafos()

    print("\nGeneración terminada correctamente.")