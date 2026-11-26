
import math
def distancia(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    d = math.sqrt(dx**2 + dy**2)
    return dx, dy, d
def direccion(dx, dy, d):
    if d == 0:
        return 0, 0
    x = dx / d
    y = dy / d
    return x, y
def repulsion(dx, dy, d, c3):
    if d == 0:
        return 0.0, 0.0
    z = c3 / math.sqrt(d)
    x, y = direccion(dx, dy, d)
    fx = z * x
    fy = z * y
    return fx, fy
def atraccion(dx, dy, d, c1, c2):
    if d == 0:
        return 0.0, 0.0
    fa = c1 * math.log(d / c2)
    # Dirección desde A hacia B
    x, y = direccion(-dx, -dy, d)
    # Componentes de la fuerza
    fx = fa * x
    fy = fa * y
    return fx, fy

def actualizar_posiciones(posiciones, fuerzas, c4):
    nuevas_posiciones = {}
    for nodo in posiciones:
        x, y = posiciones[nodo]
        fx, fy = fuerzas[nodo]
        nuevo_x = x + c4 * fx
        nuevo_y = y + c4 * fy
        nuevas_posiciones[nodo] = (nuevo_x, nuevo_y)
    return nuevas_posiciones
def calcular_fuerzas(posiciones, vecinos, c1, c2, c3):
    fuerzas = {}
    for nodo in posiciones:
        fx_total = 0
        fy_total = 0
        for otro in posiciones:
            if nodo == otro:
                continue
            dx, dy, d = distancia(posiciones[nodo],posiciones[otro])
            if d == 0:
                continue
            if otro in vecinos[nodo]:
                fx, fy = atraccion(dx, dy, d, c1, c2)
            else:
                fx, fy = repulsion(dx, dy, d, c3)
            fx_total += fx
            fy_total += fy
        fuerzas[nodo] = (fx_total, fy_total)
    return fuerzas

def calcular_fuerzas_optimizado(posiciones, vecinos, c1, c2, c3):
    nodos = list(posiciones)
    fuerzas = {nodo: [0.0, 0.0]for nodo in nodos}
    for i in range(len(nodos)):
        u = nodos[i]
        for j in range(i + 1, len(nodos)):
            v = nodos[j]
            dx, dy, d = distancia(posiciones[u],posiciones[v])
            if d == 0:
                continue
            if v in vecinos[u]:
                fx, fy = atraccion(dx, dy, d, c1, c2)
            else:
                fx, fy = repulsion(dx, dy, d, c3)
            fuerzas[u][0] += fx
            fuerzas[u][1] += fy
            fuerzas[v][0] -= fx
            fuerzas[v][1] -= fy
    return {nodo: tuple(fuerza) for nodo, fuerza in fuerzas.items()}

def spring(posiciones, vecinos, c1, c2, c3, c4, M):
    for i in range(M):
        fuerzas = calcular_fuerzas(posiciones,vecinos,c1,c2,c3)
        nuevas_posiciones = actualizar_posiciones(posiciones,fuerzas,c4)
        posiciones=nuevas_posiciones
    return posiciones
