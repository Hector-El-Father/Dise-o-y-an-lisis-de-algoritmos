import math
from grafos import (grafo_malla,grafo_erdos_renyi,grafo_gilbert,grafo_geografico,grafo_barabasi_albert,grafo_dorogovtsev_mendes)

def obtener_generadores(n):
    dimensiones = {
        30: (5, 6),
        100: (10, 10),
        500: (20, 25)
    }
    if n not in dimensiones:
        raise ValueError("Usar 30, 100 o 500 nodos")
    columnas, filas = dimensiones[n]
    m = 2 * n
    p = 4 / (n - 1)
    r = math.sqrt(4 / (math.pi * (n - 1)))
    generadores = {
        "malla": lambda: grafo_malla(columnas, filas),
        "erdos_renyi": lambda: grafo_erdos_renyi(n, m),
        "gilbert": lambda: grafo_gilbert(n, p),
        "geografico": lambda: grafo_geografico(n, r),
        "barabasi_albert": lambda: grafo_barabasi_albert(n, 2),
        "dorogovtsev_mendes": lambda: grafo_dorogovtsev_mendes(n)
    }
    return generadores
if __name__ == "__main__":
    import random
    generadores = obtener_generadores(30)
    for nombre, generador in generadores.items():
        random.seed(42)
        grafo = generador()
        print(
            f"{nombre:22} | "
            f"Nodos: {grafo.obtener_numero_vertices():3} | "
            f"Aristas: {grafo.obtener_numero_aristas():4}"
        )