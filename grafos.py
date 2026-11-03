# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from pathlib import Path
from collections import deque
import subprocess
import heapq

# %%
class Nodo:
    def __init__(self, id,nombre=None):
        self.id=id
        self.nombre=nombre
    def __eq__(self, nodo_comparado):
        return self.id == nodo_comparado.id

# %%
class Arista:
    def __init__(self, nodo1, nodo2, peso=1):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso=peso
    def __eq__(self, arista_comparada):
        return (
            (self.nodo1 == arista_comparada.nodo1 and self.nodo2 == arista_comparada.nodo2)
            or
            (self.nodo1 == arista_comparada.nodo2 and self.nodo2 == arista_comparada.nodo1)
        )
    def __hash__(self):
        return hash(frozenset([self.nodo1.id,self.nodo2.id]))
    def __str__(self):
        return f"{self.nodo1.nombre} -- {self.nodo2.nombre}"

# %%
class Grafo:
    def __init__(self):
        self.nodos={}
        self.aristas=set()
        self.adyacencias={}
        self.pesos={}
    def agregar_nodo(self, nodo):
        #si el id no esta en los nodos
        if nodo.id not in self.nodos:
            self.nodos[nodo.id]=nodo
            self.adyacencias[nodo.id]=set()
            self.pesos[nodo.id]={}
        else:
            print("el nodo ya a sido definido para este grafo")

    def agregar_arista(self, arista):
        """Agrega una arista al grafo este metodo
        la arista se agrega si:
        1. No es un lazo
        2. ambos nodos pertenecen al grafo
        3. La arista no existe previamente
        """
        # Evita revisar lazos 
        if arista.nodo1==arista.nodo2:
            print("No se permite enlazar un nodo con si mismo")
            return
        # Comprueba que ambos nodos existan
        for nodo in [arista.nodo1, arista.nodo2]:
            if nodo.id not in self.nodos:
                print("el nodo no esta presente en el grafo")
                return
        # Evitar que aristas se dupliquen
        if arista in self.aristas:
            print("Esta arista ya esta presente en el grafo")
            return
        #Agrega la arista al grafo
        self.aristas.add(arista)
        #actualiza las adyacencias en ambos sentidos
        self.adyacencias[arista.nodo1.id].add(arista.nodo2.id)
        self.adyacencias[arista.nodo2.id].add(arista.nodo1.id)
        # Registramos el peso en ambos sentidos
        self.pesos[arista.nodo1.id][arista.nodo2.id] = arista.peso
        self.pesos[arista.nodo2.id][arista.nodo1.id] = arista.peso
       
    def obtener_vecinos(self, nodo):
        vecinos_del_nodo=[]
        for vecinos_id in self.adyacencias[nodo.id]:
            vecinos_del_nodo.append(self.nodos[vecinos_id])
        return vecinos_del_nodo
    def obtener_grados_nodo(self, nodo):
        return len(self.adyacencias[nodo.id])
    def obtener_adyacencias(self):
        adyacencias_nombres={}
        for id_nodo, vecinos_id in self.adyacencias.items():
            vecinos_nombre=set()
            for id_vecino in vecinos_id:
                vecinos_nombre.add(self.nodos[id_vecino].nombre)
            adyacencias_nombres[self.nodos[id_nodo].nombre]=vecinos_nombre
        return adyacencias_nombres
    def obtener_numero_vertices(self):
        return len(self.nodos)
    
    def obtener_numero_aristas(self):
        return len(self.aristas)
    
    def obtener_grado_promedio(self):
        suma_grados = 0
        for nodo in self.nodos.values():
            suma_grados = suma_grados + self.obtener_grados_nodo(nodo)
        if self.obtener_numero_vertices() == 0:
            return 0
        else:
            return suma_grados / self.obtener_numero_vertices()
        
    def obtener_densidad(self):
        numero_vertices=self.obtener_numero_vertices()
        numero_aristas=self.obtener_numero_aristas()
        if numero_vertices==0 or numero_vertices==1:
            return 0
        else:
            return (2*numero_aristas)/(numero_vertices*(numero_vertices-1))
    def obtener_grado_maximo(self):
        grado_maximo=0
        for nodo in self.nodos.values():
            grado_nodo=self.obtener_grados_nodo(nodo)
            if grado_nodo > grado_maximo:
                grado_maximo = grado_nodo
        return grado_maximo
    def obtener_grado_minimo(self):
        if self.obtener_numero_vertices()==0:
            return 0
        grado_minimo=self.obtener_grado_maximo()
        for nodo in self.nodos.values():
            grado_nodo=self.obtener_grados_nodo(nodo)
            if grado_minimo > grado_nodo:
                grado_minimo=grado_nodo
        return grado_minimo
    def guardar_gv(self, nombre_archivo):
        with open(nombre_archivo, "w") as archivo:
            archivo.write("graph G {\n")
            for nodo in self.nodos.values():
                archivo.write(f'"{nodo.nombre}";\n')
            for arista in self.aristas:
                    archivo.write(
                        f'"{arista.nodo1.nombre}" -- '
                        f'"{arista.nodo2.nombre}" '
                        f'[label="{arista.peso}"];\n'
    )
            archivo.write("}\n")
    def BFS(self, s):
        visitados = set()
        cola = deque()
        arbol = Grafo()
        visitados.add(s.id)
        cola.append(s)
        arbol.agregar_nodo(s)
        while cola:
            actual = cola.popleft()

            for vecino in self.obtener_vecinos(actual):
                if vecino.id not in visitados:
                    visitados.add(vecino.id)
                    cola.append(vecino)
                    arbol.agregar_nodo(vecino)
                    arbol.agregar_arista(Arista(actual, vecino))
        return arbol
    
    def DFS_R(self, s):
        visitados = set()
        arbol = Grafo()
        def explorar(actual):
            visitados.add(actual.id)
            for vecino in self.obtener_vecinos(actual):
                if vecino.id not in visitados:
                    arbol.agregar_nodo(vecino)
                    arbol.agregar_arista(Arista(actual, vecino))
                    explorar(vecino)
        arbol.agregar_nodo(s)
        explorar(s)
        return arbol
    def DFS_I(self, s):
        visitados = {s.id}
        arbol = Grafo()

        arbol.agregar_nodo(s)
        pila = [(s, iter(self.obtener_vecinos(s)))]
        while pila:
            actual, vecinos = pila[-1]
            try:
                vecino = next(vecinos)
            except StopIteration:
                pila.pop()
                continue
            if vecino.id not in visitados:
                visitados.add(vecino.id)
                arbol.agregar_nodo(vecino)
                arbol.agregar_arista(Arista(actual, vecino))
                pila.append((vecino, iter(self.obtener_vecinos(vecino))))
        return arbol
    
    def Dijkstra(self, s):
        distancia = {}
        predecesor = {}
        for v in self.nodos:
            distancia[v] = float("inf")
            predecesor[v] = None
        distancia[s] = 0
        cola = []
        heapq.heappush(cola, (0, s))
        while cola:
            distancia_actual, u = heapq.heappop(cola)
            if distancia_actual > distancia[u]:
                continue
            for v in self.adyacencias[u]:
                peso = self.pesos[u][v]
                nueva_distancia = distancia[u] + peso
                if nueva_distancia < distancia[v]:
                    distancia[v] = nueva_distancia
                    predecesor[v] = u
                    heapq.heappush(cola, (nueva_distancia, v))
        arbol=Grafo()
        for id_nodo in self.nodos:
            if distancia[id_nodo] != float("inf"):
                nodo_original = self.nodos[id_nodo]
                nombre = f"{nodo_original.nombre} ({distancia[id_nodo]})"
                nodo_nuevo = Nodo(id_nodo, nombre)
                arbol.agregar_nodo(nodo_nuevo)

        for nodo, anterior in predecesor.items():
            if anterior is None:
                continue   
            nodo_origen = arbol.nodos[anterior]
            nodo_destino = arbol.nodos[nodo]
            peso = self.pesos[anterior][nodo]
            arista_nueva = Arista(nodo_origen,nodo_destino,peso=peso)
            arbol.agregar_arista(arista_nueva)
        return arbol,distancia, predecesor

# %%
# m representa columnas
# n representa filas
def grafo_malla(m, n, peso_min=1, peso_max=11):
    grafo = Grafo()
    rng = random.Random(42)
    for i in range(1, m+1):
        for j in range(1, n+1):
            nodo = Nodo(
                (i, j),
                f"n{i},{j}"
            )
            grafo.agregar_nodo(nodo)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i < m:
                peso=rng.randint(peso_min, peso_max)
                arista_nueva=Arista(grafo.nodos[(i,j)],grafo.nodos[(i+1,j)], peso=peso)
                grafo.agregar_arista(arista_nueva)
            if j < n:
                peso=rng.randint(peso_min, peso_max)
                arista_nueva=Arista(grafo.nodos[(i,j)],grafo.nodos[(i,j+1)], peso=peso)
                grafo.agregar_arista(arista_nueva)
    return grafo

# %%
#Creamos \(n\) vértices y seleccionamos uniformemente al azar \(m\) pares distintos de vértices distintos.
# n representa el numero de nodos
# m representa el numero de aristas
def grafo_erdos_renyi(n,m):
    max_aristas = n * (n - 1) // 2
    if n<=0:
        return None
    if m < 0 or m > max_aristas:
        return None
    grafo = Grafo()
    aristas_posibles=[]
    for i in range(1, n+1):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            arista = Arista(grafo.nodos[i], grafo.nodos[j])
            aristas_posibles.append(arista)
    aristas_elegidas = random.sample(aristas_posibles, m)
    for arista in aristas_elegidas:
        grafo.agregar_arista(arista)
    return grafo

# %%
def grafo_gilbert(n, p):
    if n<=0:
        return None
    if p<=0 or p>=1:
        return None
    grafo = Grafo()
    for i in range(1, n + 1):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if random.random() < p:
                arista_nueva=Arista(grafo.nodos[i],grafo.nodos[j])
                grafo.agregar_arista(arista_nueva)
    return grafo

# %%
def grafo_geografico(n, r):
    if n<=0:
        return None
    if r<=0 or r>=1:
        return None
    grafo = Grafo()
    coordenadas={}
    for i in range(1, n + 1):
        nodo = Nodo(i,f"n{i}")
        grafo.agregar_nodo(nodo)
        x = random.random()
        y = random.random()
        coordenadas[i]=(x,y)
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            x1, y1 = coordenadas[i]
            x2, y2 = coordenadas[j]
            x_diff=(x1-x2)**2
            y_diff=(y1-y2)**2
            d=(x_diff+y_diff)**0.5
            if d<=r:
                arista_nueva=Arista(grafo.nodos[i],grafo.nodos[j])
                grafo.agregar_arista(arista_nueva)  
    return grafo

# %%
def grafo_barabasi_albert(n, d):
    if n<=0:
        return None
    if d<=1:
        return None
    if d>=n:
        return None
    grafo = Grafo()
    for i in range(1, d+1):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
    for i in range(1, d + 1):
        for j in range(i + 1, d + 1):
            arista_nueva=Arista(grafo.nodos[i],grafo.nodos[j])
            grafo.agregar_arista(arista_nueva)
    for i in range(d + 1, n + 1):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
        nodos_candidatos = []
        pesos = []
        for id_nodo in range(1, i):
            nodos_candidatos.append(grafo.nodos[id_nodo])
            pesos.append(grafo.obtener_grados_nodo(grafo.nodos[id_nodo]))
        for _ in range(d):
            elegido = random.choices(nodos_candidatos,weights=pesos,k=1)[0]
            indice = nodos_candidatos.index(elegido)
            arista_nueva = Arista(nodo, elegido)
            grafo.agregar_arista(arista_nueva)
            nodos_candidatos.pop(indice)
            pesos.pop(indice)
    return grafo

# %%
def grafo_dorogovtsev_mendes(n):
    if n < 3:
        return None
    grafo = Grafo()
    for i in range(1, 4):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
    for i in range(1, 4):
         for j in range(i + 1, 4):
            arista_nueva=Arista(grafo.nodos[i],grafo.nodos[j])
            grafo.agregar_arista(arista_nueva)
    for i in range(4, n + 1):
        nodo = Nodo(i, f"n{i}")
        grafo.agregar_nodo(nodo)
        lista_arista = list(grafo.aristas)
        elegido = random.choice(lista_arista)
        arista_nueva=Arista(nodo,elegido.nodo1)
        grafo.agregar_arista(arista_nueva)
        arista_nueva=Arista(nodo,elegido.nodo2)
        grafo.agregar_arista(arista_nueva)
    return grafo

def asignar_pesos(grafo, peso_min=1, peso_max=10, semilla=42):
    if peso_min < 0 or peso_min > peso_max:
        raise ValueError("Rango de pesos inválido")
    rng = random.Random(semilla)
    # Ordenamos las aristas para garantizar reproducibilidad
    aristas_ordenadas = sorted(grafo.aristas, key=lambda a: tuple(sorted((repr(a.nodo1.id), repr(a.nodo2.id)))))
    for arista in aristas_ordenadas:
        # Generamos un peso por arista
        peso = rng.randint(peso_min, peso_max)
        u = arista.nodo1.id
        v = arista.nodo2.id
        # Actualizamos el objeto Arista
        arista.peso = peso
        # Actualizamos el diccionario en ambos sentidos
        grafo.pesos[u][v] = peso
        grafo.pesos[v][u] = peso
    return grafo
# %%



