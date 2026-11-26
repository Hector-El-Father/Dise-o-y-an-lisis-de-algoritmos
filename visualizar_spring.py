import pygame
from spring import calcular_fuerzas, actualizar_posiciones, calcular_fuerzas_optimizado
import random
from grafos import grafo_malla
import math
import time
import statistics
from generadores_spring import obtener_generadores

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Proyecto 5 - Eades")
reloj = pygame.time.Clock()
N = 100
nombre_modelo = "barabasi_albert"
generadores = obtener_generadores(N)
#random.seed(42)
grafo = generadores[nombre_modelo]()
nodos = list(grafo.nodos.keys())
vecinos = grafo.adyacencias
aristas = []
for arista in grafo.aristas:
    u = arista.nodo1.id
    v = arista.nodo2.id
    aristas.append((u, v))
rng = random.Random(42)
posiciones = {}
for nodo in nodos:
    x = rng.uniform(50, 750)
    y = rng.uniform(50, 550)
    posiciones[nodo] = (x, y)
print("Nodos:", len(nodos))
print("Aristas:", len(aristas))
print("Posiciones:", len(posiciones))
c1 = 2
c2 = 50
c3 = 1
c4 = 0.2
ejecutando = True
M = 500
iteracion = 0
tiempos_ms = []
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    if iteracion < M:
        inicio=time.perf_counter()
        fuerzas = calcular_fuerzas_optimizado(posiciones, vecinos, c1, c2, c3)
        nuevas_posiciones = actualizar_posiciones(posiciones, fuerzas, c4)
        tiempo_ms = (time.perf_counter() - inicio) * 1000
        tiempos_ms.append(tiempo_ms)
        desplazamiento_max = max(math.dist(posiciones[nodo], nuevas_posiciones[nodo]) for nodo in posiciones)
        posiciones = nuevas_posiciones
        iteracion += 1
        if iteracion == M:
            print("\nRESUMEN DEL EXPERIMENTO")
            print(f"Nodos: {len(posiciones)}")
            print(f"Aristas: {len(aristas)}")
            print(f"Iteraciones: {M}")
            print(f"Tiempo promedio: "
            f"{statistics.mean(tiempos_ms):.4f} ms")
            print(
            f"Tiempo mediano: "
            f"{statistics.median(tiempos_ms):.4f} ms")
            print(f"Tiempo total de cálculo: "
            f"{sum(tiempos_ms) / 1000:.4f} s")
            print(
            f"Desplazamiento final: "
            f"{desplazamiento_max:.6f}")
    pantalla.fill((255, 255, 255))
    for u, v in aristas:
        pygame.draw.line(
            pantalla,
            (0, 0, 0),
            posiciones[u],
            posiciones[v],
            2
        )
    for nodo, posicion in posiciones.items():
        pygame.draw.circle(
            pantalla,
            (30, 120, 220),
            (round(posicion[0]), round(posicion[1])),
            15
        )
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()

