from generadores_spring import obtener_generadores
from spring import calcular_fuerzas_optimizado, actualizar_posiciones
import random
import time
import math
import statistics
N = 500
M = 500
def ejecutar_experimento(grafo, M=500):
    c1 = 2
    c2 = 50
    c3 = 1
    c4 = 0.2
    rng = random.Random(42)
    posiciones = {}
    for nodo in grafo.nodos:
        x = rng.uniform(50, 750)
        y = rng.uniform(50, 550)
        posiciones[nodo] = (x, y)
    vecinos = grafo.adyacencias
    tiempos = []
    desplazamiento_max = 0.0
    for i in range(M):
        inicio = time.perf_counter()
        fuerzas = calcular_fuerzas_optimizado(posiciones, vecinos, c1, c2, c3)
        nuevas_posiciones = actualizar_posiciones(posiciones, fuerzas, c4)
        tiempo_ms = (time.perf_counter() - inicio) * 1000
        tiempos.append(tiempo_ms)
        desplazamiento_max = max(math.dist(posiciones[nodo], nuevas_posiciones[nodo])for nodo in posiciones)
        posiciones = nuevas_posiciones
    return {
        "nodos": grafo.obtener_numero_vertices(),
        "aristas": grafo.obtener_numero_aristas(),
        "iteraciones": M,
        "tiempo_promedio_ms": statistics.mean(tiempos),
        "tiempo_total_s": sum(tiempos) / 1000,
        "desplazamiento_final": desplazamiento_max
    }
generadores = obtener_generadores(N)
for nombre, generador in generadores.items():
    random.seed(42)
    grafo = generador()
    resultado = ejecutar_experimento(grafo, M=500)
    print(
        f"{nombre:22} | "
        f"Nodos: {resultado['nodos']:3} | "
        f"Tiempo: {resultado['tiempo_promedio_ms']:.4f} ms | "
        f"Desplazamiento: {resultado['desplazamiento_final']:.6f}"
    )
