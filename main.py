from pathlib import Path
from grafos import (
    grafo_malla,
    grafo_erdos_renyi,
    grafo_gilbert,
    grafo_geografico,
    grafo_barabasi_albert,
    grafo_dorogovtsev_mendes,
)
CARPETA_RESULTADOS = Path("resultados")
def guardar(grafo, modelo, nombre):
    carpeta = CARPETA_RESULTADOS / modelo
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{nombre}.gv"
    grafo.guardar_gv(ruta)
    print(
        f"{nombre}: "
        f"{grafo.obtener_numero_vertices()} nodos, "
        f"{grafo.obtener_numero_aristas()} aristas"
    )
def generar_mallas():
    dimensiones = {
        50: (5, 10),
        200: (20, 10),
        500: (25, 20),
    }
    for cantidad, (m, n) in dimensiones.items():
        grafo = grafo_malla(m, n)
        guardar(grafo, "malla", f"malla_{cantidad}")
def generar_modelos_aleatorios():
    tamanos = [50, 200, 500]
    for n in tamanos:
        m = 2 * n
        guardar(
            grafo_erdos_renyi(n, m),
            "erdos_renyi",
            f"erdos_renyi_{n}",
        )
        guardar(
            grafo_gilbert(n, 0.1),
            "gilbert",
            f"gilbert_{n}",
        )
        guardar(
            grafo_geografico(n, 0.1),
            "geografico",
            f"geografico_{n}",
        )
        guardar(
            grafo_barabasi_albert(n, 3),
            "barabasi_albert",
            f"barabasi_albert_{n}",
        )
        guardar(
            grafo_dorogovtsev_mendes(n),
            "dorogovtsev_mendes",
            f"dorogovtsev_mendes_{n}",
        )
def main():
    generar_mallas()
    generar_modelos_aleatorios()
    print("Generación terminada.")
if __name__ == "__main__":
    main()