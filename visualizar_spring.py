import pygame
from spring import actualizar_posiciones, calcular_fuerzas_optimizado
import random
import math
import time
import statistics
from generadores_spring import obtener_generadores
from pathlib import Path
import argparse
def ajustar_posiciones_pantalla(posiciones, ancho, alto, encabezado=65, margen=25):
    xs = [x for x, y in posiciones.values()]
    ys = [y for x, y in posiciones.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    rango_x = max(max_x - min_x, 1)
    rango_y = max(max_y - min_y, 1)
    ancho_disponible = ancho - 2 * margen
    alto_disponible = alto - encabezado - 2 * margen
    escala = min(1.0, ancho_disponible / rango_x, alto_disponible / rango_y)
    centro_x = (min_x + max_x) / 2
    centro_y = (min_y + max_y) / 2
    pantalla_centro_x = ancho / 2
    pantalla_centro_y = encabezado + (alto - encabezado) / 2
    posiciones_pantalla = {}
    for nodo, (x, y) in posiciones.items():
        x_pantalla = pantalla_centro_x + (x - centro_x) * escala
        y_pantalla = pantalla_centro_y + (y - centro_y) * escala
        posiciones_pantalla[nodo] = (round(x_pantalla), round(y_pantalla))
    return posiciones_pantalla
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
parser.add_argument("--nodos", type=int, choices=[100, 500], default=100)
parser.add_argument("--iteraciones", type=int, default=600)
parser.add_argument("--lote", action="store_true")
args = parser.parse_args()
if args.iteraciones <= 0:
    parser.error("--iteraciones debe ser mayor que cero")
pygame.init()
fuente = pygame.font.SysFont("Arial", 22)
pantalla = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Proyecto 5 - Eades")
reloj = pygame.time.Clock()
N = args.nodos
M = args.iteraciones
nombre_modelo = args.modelo
generadores = obtener_generadores(N)
ruta_capturas = Path("resultados_5/capturas")
ruta_capturas.mkdir(parents=True, exist_ok=True)
ruta_captura = ruta_capturas / f"{nombre_modelo}_{N}.png"
captura_guardada = False
random.seed(42)
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
    video = imageio.get_writer(str(ruta_video), fps=30, codec="libx264", macro_block_size=8)
for arista in grafo.aristas:
    u = arista.nodo1.id
    v = arista.nodo2.id
    aristas.append((u, v))
rng = random.Random(42)
posiciones = {}
for nodo in nodos:
    x = rng.uniform(480, 520)
    y = rng.uniform(512, 552)
    posiciones[nodo] = (x, y)
print("Modelo:", nombre_modelo)
print("Nodos:", len(nodos))
print("Aristas:", len(aristas))
print("Posiciones:", len(posiciones))
c1 = 2
c2 = 50
c3 = 1
c4 = 0.2
ejecutando = True
iteracion = 0
tiempos_ms = []
radio_nodo = 3 if N == 500 else 5
opacidad_arista = 25 if N == 500 else 90
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    if iteracion < M:
        inicio = time.perf_counter()
        fuerzas = calcular_fuerzas_optimizado(posiciones, vecinos, c1, c2, c3)
        nuevas_posiciones = actualizar_posiciones(posiciones, fuerzas, c4)
        tiempo_ms = (time.perf_counter() - inicio) * 1000
        tiempos_ms.append(tiempo_ms)
        desplazamiento_max = max(math.dist(posiciones[nodo], nuevas_posiciones[nodo]) for nodo in posiciones)
        posiciones = nuevas_posiciones
        iteracion += 1
        if iteracion == M:
            print("\nRESUMEN DEL EXPERIMENTO")
            print(f"Modelo: {nombre_modelo}")
            print(f"Nodos: {len(posiciones)}")
            print(f"Aristas: {len(aristas)}")
            print(f"Iteraciones: {M}")
            print(f"Tiempo promedio: {statistics.mean(tiempos_ms):.4f} ms")
            print(f"Tiempo mediano: {statistics.median(tiempos_ms):.4f} ms")
            print(f"Tiempo total de cálculo: {sum(tiempos_ms) / 1000:.4f} s")
            print(f"Desplazamiento final: {desplazamiento_max:.6f}")
    superficie = pygame.display.get_surface()
    ancho, alto = superficie.get_size()
    posiciones_pantalla = ajustar_posiciones_pantalla(posiciones, ancho, alto)
    superficie.fill((255, 255, 255))
    capa_aristas = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
    for u, v in aristas:
        pygame.draw.line(
            capa_aristas,
            (40, 40, 40, opacidad_arista),
            posiciones_pantalla[u],
            posiciones_pantalla[v],
            1
        )
    superficie.blit(capa_aristas, (0, 0))
    for nodo in nodos:
        pygame.draw.circle(
            superficie,
            (32, 184, 120),
            posiciones_pantalla[nodo],
            radio_nodo
        )
    pygame.draw.rect(superficie, (25, 25, 30), (0, 0, ancho, 65))
    info_modelo = (
        f"Modelo: {nombre_modelo} | "
        f"Nodos: {len(nodos)} | "
        f"Aristas: {len(aristas)}"
    )
    info_iteracion = f"Iteracion: {iteracion}/{M}"
    texto1 = fuente.render(info_modelo, True, (255, 255, 255))
    texto2 = fuente.render(info_iteracion, True, (255, 255, 255))
    superficie.blit(texto1, (12, 10))
    superficie.blit(texto2, (12, 35))
    if iteracion >= M and not captura_guardada:
        pygame.image.save(superficie, str(ruta_captura))
        captura_guardada = True
        print(f"Captura guardada: {ruta_captura}")
    if video is not None and 0 < iteracion <= M:
        if iteracion != ultimo_frame_grabado:
            fotograma = pygame.surfarray.array3d(superficie).transpose(1, 0, 2)
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



