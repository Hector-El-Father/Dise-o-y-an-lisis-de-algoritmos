import random
from grafos import (grafo_malla,grafo_erdos_renyi,grafo_gilbert,grafo_geografico,grafo_barabasi_albert,grafo_dorogovtsev_mendes,asignar_pesos)
import random
from time import perf_counter
from statistics import median

def validar_mst(original, mst, peso_total):
    V = original.obtener_numero_vertices()
    E = mst.obtener_numero_aristas()
    # 1. Verificamos que conserva todos los nodos
    assert set(mst.nodos) == set(original.nodos)
    # 2. Un árbol tiene V-1 aristas
    assert E == V - 1
    # 3. Comprobamos conectividad usando BFS
    s = next(iter(mst.nodos.values()))
    recorrido = mst.BFS(s)
    assert recorrido.obtener_numero_vertices() == V
    # 4. Comprobamos las aristas y sus pesos
    for arista in mst.aristas:
        u = arista.nodo1.id
        v = arista.nodo2.id
        assert v in original.adyacencias[u]
        assert arista.peso == original.pesos[u][v]
    # 5. Verificamos el peso acumulado
    suma_pesos = sum(a.peso for a in mst.aristas)
    assert suma_pesos == peso_total
    return True

def es_conexo(grafo):
    if grafo.obtener_numero_vertices() == 0:
        return False
    s = next(iter(grafo.nodos.values()))
    recorrido = grafo.BFS(s)
    return (recorrido.obtener_numero_vertices() == grafo.obtener_numero_vertices())
def generar_conexo(generador, semilla_base=42, max_intentos=100):
    for intento in range(max_intentos):
        # Cambiamos la semilla para cada intento
        semilla_actual = semilla_base + intento
        random.seed(semilla_actual)
        # Generamos un nuevo grafo
        grafo = generador()
        if grafo is None:
            raise ValueError("El generador no produjo un grafo válido")
        # Verificamos si todos los nodos están conectados
        if es_conexo(grafo):
            return grafo, semilla_actual, intento + 1
    raise RuntimeError(
        f"No se obtuvo un grafo conexo "
        f"después de {max_intentos} intentos"
    )
def maximo_en_camino(arbol, origen, destino):
    pila = [(origen, float("-inf"))]
    visitados = set()
    while pila:
        actual, maximo = pila.pop()
        if actual == destino:
            return maximo
        if actual in visitados:
            continue
        visitados.add(actual)
        for vecino in arbol.adyacencias[actual]:
            if vecino not in visitados:
                peso = arbol.pesos[actual][vecino]
                pila.append((
                    vecino,
                    max(maximo, peso)
                ))
    raise ValueError("No existe un camino entre los nodos")


def validar_optimalidad(original, mst):
    for arista in original.aristas:
        u = arista.nodo1.id
        v = arista.nodo2.id
        # Si la arista ya pertenece al MST, la omitimos
        if v in mst.adyacencias[u]:
            continue
        # Mayor peso en el camino del árbol
        mayor = maximo_en_camino(mst, u, v)
        # ¿Existe una sustitución que reduzca el peso?
        if arista.peso < mayor:
            raise AssertionError(
                f"El MST no es óptimo: "
                f"la arista {u}-{v} pesa {arista.peso}, "
                f"pero sustituiría una de peso {mayor}"
            )
    return True


def obtener_generadores(n):
    dimensiones = {
        30: (5, 6),
        500: (20, 25)
    }
    radios = {
        30: 0.30,
        500: 0.09
    }
    m, filas = dimensiones[n]
    return {
        "malla": lambda: grafo_malla(m, filas),
        "erdos_renyi": lambda: grafo_erdos_renyi(n, 3*n),
        "gilbert": lambda: grafo_gilbert(n, 6/(n-1)),
        "geografico": lambda: grafo_geografico(n, radios[n]),
        "barabasi_albert": lambda: grafo_barabasi_albert(n, 3),
        "dorogovtsev_mendes": lambda: grafo_dorogovtsev_mendes(n)
    }

def comparar_algoritmos(grafo, repeticiones=3):
    # Obtenemos el identificador del nodo inicial para Prim
    s = next(iter(grafo.nodos))
    algoritmos = {
        "Kruskal": lambda: grafo.Kruskal(),
        "Kruskal inverso": lambda: grafo.Kruskal_Inverso(),
        "Prim": lambda: grafo.Prim(s)
    }
    resultados = {}
    for nombre, ejecutar in algoritmos.items():
        tiempos = []
        pesos = []
        for _ in range(repeticiones):
            inicio = perf_counter()
            mst, peso_total = ejecutar()
            tiempo = perf_counter() - inicio
            tiempos.append(tiempo * 1000)
            pesos.append(peso_total)
        # Comprobamos consistencia entre ejecuciones
        assert len(set(pesos)) == 1
        # Validamos el árbol de la última ejecución
        validar_mst(grafo, mst, peso_total)
        validar_optimalidad(grafo, mst)
        resultados[nombre] = {
            "peso": peso_total,
            "tiempo_ms": median(tiempos),
            "aristas": mst.obtener_numero_aristas()
        }
    # Los tres algoritmos deben obtener el mismo peso
    pesos_finales = {resultado["peso"] for resultado in resultados.values()}
    assert len(pesos_finales) == 1, ("Los tres algoritmos obtuvieron pesos diferentes")
    return resultados

def ejecutar_comparacion():

    for n in [30, 500]:

        generadores = obtener_generadores(n)

        for nombre, generador in generadores.items():

            # 1. Generamos un grafo conexo
            grafo, semilla, intentos = generar_conexo(
                generador,
                semilla_base=42,
                max_intentos=100
            )

            # 2. Asignamos pesos
            grafo = asignar_pesos(
                grafo,
                peso_min=1,
                peso_max=10,
                semilla=42
            )

            # 3. Comparamos los tres algoritmos
            resultados = comparar_algoritmos(
                grafo,
                repeticiones=3
            )

            directo = resultados["Kruskal"]
            inverso = resultados["Kruskal inverso"]
            prim = resultados["Prim"]

            # 4. Mostramos los resultados
            print(f"\n{nombre} | {n} nodos")
            print(f"Semilla: {semilla} | Intentos: {intentos}")

            print(f"Peso Kruskal: {directo['peso']}")
            print(f"Peso inverso: {inverso['peso']}")
            print(f"Peso Prim: {prim['peso']}")

            print(
                f"Tiempo Kruskal: "
                f"{directo['tiempo_ms']:.4f} ms"
            )
            print(
                f"Tiempo inverso: "
                f"{inverso['tiempo_ms']:.4f} ms"
            )
            print(
                f"Tiempo Prim: "
                f"{prim['tiempo_ms']:.4f} ms"
            )
            print("Comparación: CORRECTA")
if __name__ == "__main__":
    ejecutar_comparacion()

