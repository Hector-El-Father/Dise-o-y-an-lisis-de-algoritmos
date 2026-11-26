import pygame
from spring import calcular_fuerzas, actualizar_posiciones, calcular_fuerzas_optimizado
import random
from grafos import grafo_malla
import math
import time
import statistics
from generadores_spring import obtener_generadores
from pathlib import Path

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "--modelo",
    default="malla",
    choices=[
        "malla",
        "erdos_renyi",
        "gilbert",
        "geografico",
        "barabasi_albert",
        "dorogovtsev_mendes"
    ]
)
parser.add_argument("--nodos",type=int,choices=[100, 500],default=100)
parser.add_argument("--lote",action="store_true")
args = parser.parse_args()
pygame.init()
fuente = pygame.font.SysFont("Arial", 14)
pantalla = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Proyecto 5 - Eades")
reloj = pygame.time.Clock()
N = args.nodos
nombre_modelo = args.modelo
generadores = obtener_generadores(N)
ruta_capturas = Path("resultados_5/capturas")
ruta_capturas.mkdir(parents=True,exist_ok=True)
ruta_captura = ruta_capturas / f"{nombre_modelo}_{N}.png"
captura_guardada = False
#random.seed(42)
grafo = generadores[nombre_modelo]()
nodos = list(grafo.nodos.keys())
vecinos = grafo.adyacencias
aristas = []
video = None
ultimo_frame_grabado = -1
if args.lote:
    import imageio.v2 as imageio
    ruta_videos = Path("resultados_5/videos")
    ruta_videos.mkdir(parents=True, exist_ok=True)
    ruta_video = ruta_videos / f"{nombre_modelo}_{N}.mp4"
    video = imageio.get_writer(str(ruta_video),fps=30,codec="libx264",macro_block_size=8)
for arista in grafo.aristas:
    u = arista.nodo1.id
    v = arista.nodo2.id
    aristas.append((u, v))
rng = random.Random(42)
posiciones = {}
for nodo in nodos:
    x = rng.uniform(50, 800)
    y = rng.uniform(50, 700)
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
    superficie = pygame.display.get_surface()
    pantalla.fill((255, 255, 255))
    capa_aristas = pygame.Surface(superficie.get_size(),pygame.SRCALPHA)
    for u, v in aristas:
        pygame.draw.line(
            pantalla,
            (0, 0, 0, 35),
            posiciones[u],
            posiciones[v],
            1
        )
    superficie.blit(capa_aristas, (0, 0))
    for nodo, posicion in posiciones.items():
        pygame.draw.circle(
            pantalla,
            (30, 120, 220),
            (round(posicion[0]), round(posicion[1])),
            5
        )
    superficie = pygame.display.get_surface()
    pygame.draw.rect(superficie,(25, 25, 30),(0, 0, superficie.get_width(), 65))
    info_modelo = (
        f"Modelo: {nombre_modelo} | "
        f"Nodos: {len(nodos)} | "
        f"Aristas: {len(aristas)}")
    info_iteracion = f"Iteracion: {iteracion}/{M}"
    texto1 = fuente.render(info_modelo, True, (255, 255, 255))
    texto2 = fuente.render(info_iteracion, True, (255, 255, 255))
    superficie.blit(texto1, (12, 10))
    superficie.blit(texto2, (12, 35))
    if iteracion >= M and not captura_guardada:
        pygame.image.save(pygame.display.get_surface(),str(ruta_captura))
        captura_guardada = True
        print(f"Captura guardada: {ruta_captura}")
    if video is not None and 0 < iteracion <= M:
        if iteracion != ultimo_frame_grabado:
            fotograma = pygame.surfarray.array3d(pygame.display.get_surface()).transpose(1, 0, 2)
            video.append_data(fotograma)
            ultimo_frame_grabado = iteracion
    pygame.display.flip()
    if args.lote and captura_guardada:
        ejecutando = False
    reloj.tick(60)
if video is not None:
    video.close()
    print(f"Video guardado: {ruta_video}")
pygame.quit()

