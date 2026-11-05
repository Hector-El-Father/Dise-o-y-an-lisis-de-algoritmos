import random
import subprocess
from pathlib import Path

from grafos import (
    grafo_malla,
    grafo_erdos_renyi,
    grafo_gilbert,
    grafo_geografico,
    grafo_barabasi_albert,
    grafo_dorogovtsev_mendes,
    asignar_pesos
)

RUTA_BASE = Path(__file__).resolve().parent / "resultados_3"
TAMANOS = [30,500]
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


def validar_resultados(grafos, distancias, predecesores):
    original = grafos["original"]
    arbol = grafos["dijkstra"]
    if not validar_arbol(arbol):
        raise ValueError("El árbol de Dijkstra no es válido")
    for arista in arbol.aristas:
        u = arista.nodo1.id
        v = arista.nodo2.id
        if v not in original.adyacencias[u]:
            raise ValueError(
                f"Arista inexistente: {u} -- {v}"
            )
        if arista.peso != original.pesos[u][v]:
            raise ValueError(
                f"Peso incorrecto: {u} -- {v}"
            )
    for nodo, anterior in predecesores.items():
        if anterior is None:
            continue
        peso = original.pesos[anterior][nodo]
        if distancias[nodo] != distancias[anterior] + peso:
            raise ValueError(
                f"Distancia inconsistente en {nodo}"
            )
    for arista in original.aristas:
        u = arista.nodo1.id
        v = arista.nodo2.id
        peso = arista.peso
        if distancias[v] > distancias[u] + peso:
            raise ValueError(f"Distancia no óptima hacia {v}")

        if distancias[u] > distancias[v] + peso:
            raise ValueError(f"Distancia no óptima hacia {u}")

    return True
# procesar los grafos
def procesar_grafo(grafo, s, ruta):

    ruta = Path(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    arbol_dijkstra,distancias, predecesores= grafo.Dijkstra(s.id)
    grafos = {
        "original": grafo,
        "dijkstra": arbol_dijkstra
    }
    validar_resultados(grafos,distancias, predecesores)
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
            grafo = asignar_pesos(
                grafo,
                peso_min=1,
                peso_max=10,semilla=SEMILLA)
            s = next(iter(grafo.nodos.values()))
            ruta = RUTA_BASE / nombre / f"{n}_nodos"
            resultados = procesar_grafo(grafo, s, ruta)
            print(f"\n{nombre.upper()} | {n} nodos")
            print(
                "Aristas originales:",
                grafo.obtener_numero_aristas()
            )
            for algoritmo in ["dijkstra"
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
