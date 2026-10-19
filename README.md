# Proyecto 2: Árboles de búsqueda BFS y DFS

**Diseño y Análisis de Algoritmos — CIC-IPN**

## Objetivo

Ampliar la biblioteca de grafos del Proyecto 1 con tres métodos de la clase `Grafo` que, dado un nodo fuente `s`, devuelven el árbol de búsqueda correspondiente:

- `BFS(self, s)`: búsqueda en anchura mediante cola FIFO.
- `DFS_R(self, s)`: búsqueda en profundidad recursiva.
- `DFS_I(self, s)`: búsqueda en profundidad iterativa mediante una pila que conserva los vecinos pendientes.

Los recorridos abarcan únicamente los vértices **alcanzables desde `s`**; si el grafo está desconectado, el resultado no incluye los componentes restantes.

## Estructura del repositorio

```text
.
├── grafos.py                 # Clases Nodo, Arista y Grafo; 6 generadores; BFS y DFS
├── generar_resultados.py     # Generación, exportación y validación automatizadas
├── tarea 2.ipynb             # Pruebas y desarrollo del proyecto
├── resultados_2/             # Resultados originales entregados
├── .gitignore
└── README.md
```

Cada modelo tiene carpetas `30_nodos/`, `100_nodos/` y `500_nodos/`, con los archivos `original.gv`, `bfs.gv`, `dfs_recursivo.gv`, `dfs_iterativo.gv` y sus imágenes.

**Importante:** el script `generar_resultados.py` escribe en **`resultados_2_prueba/`**, separada de `resultados_2/`. De este modo se pueden regenerar experimentos sin sobrescribir los entregables originales. Se recomienda incluir `resultados_2_prueba/` en `.gitignore`.

## Modelos y parámetros

| Generador | Parámetros para 30, 100 y 500 nodos |
|---|---|
| Malla | `5×6`, `10×10`, `20×25` |
| Erdős–Rényi `G(n,m)` | `m = 3n` |
| Gilbert `G(n,p)` | `p = 6/(n-1)` |
| Geográfico | `r = 0.30`, `0.18`, `0.09` |
| Barabási–Albert | `d = 3` |
| Dorogovtsev–Mendes | `n = 30`, `100`, `500` |

Se emplea la semilla aleatoria `42` para facilitar la reproducción. El resultado exacto también puede depender del orden de ejecución y del procesamiento de vecinos.

## Resultados obtenidos

La columna **Alcanzados** indica los nodos visitados desde la fuente. En todas las pruebas, BFS y ambos DFS alcanzaron el mismo número de nodos.

| Generador | Nodos originales | Aristas originales | Alcanzados | Aristas de cada árbol |
|---|---:|---:|---:|---:|
| Malla | 30 | 49 | 30 | 29 |
| Malla | 100 | 180 | 100 | 99 |
| Malla | 500 | 955 | 500 | 499 |
| Erdős–Rényi | 30 | 90 | 30 | 29 |
| Erdős–Rényi | 100 | 300 | 99 | 98 |
| Erdős–Rényi | 500 | 1500 | 499 | 498 |
| Gilbert | 30 | 84 | 30 | 29 |
| Gilbert | 100 | 272 | 100 | 99 |
| Gilbert | 500 | 1479 | 500 | 499 |
| Geográfico | 30 | 95 | 30 | 29 |
| Geográfico | 100 | 395 | 100 | 99 |
| Geográfico | 500 | 2947 | 500 | 499 |
| Barabási–Albert | 30 | 84 | 30 | 29 |
| Barabási–Albert | 100 | 294 | 100 | 99 |
| Barabási–Albert | 500 | 1494 | 500 | 499 |
| Dorogovtsev–Mendes | 30 | 57 | 30 | 29 |
| Dorogovtsev–Mendes | 100 | 197 | 100 | 99 |
| Dorogovtsev–Mendes | 500 | 997 | 500 | 499 |

Los grafos Erdős–Rényi de 100 y 500 nodos dejaron, respectivamente, **un nodo no alcanzable** desde la fuente. Eso no constituye un fallo del algoritmo: el árbol representa la componente alcanzable.

## Validaciones

Se comprobó que los árboles generados:

1. Son conexos.
2. Cumplen `|E| = |V| - 1`.
3. Utilizan únicamente aristas presentes en el grafo original.
4. En los 18 experimentos, `DFS_R` y `DFS_I` produjeron el mismo conjunto de aristas.

La coincidencia de ambos DFS presupone el mismo orden de exploración de vecinos. BFS puede generar otro árbol, aunque visite los mismos vértices.

## Complejidad

| Algoritmo | Tiempo | Espacio auxiliar |
|---|---|---|
| BFS | `O(V + E)` | `O(V)` |
| DFS recursivo | `O(V + E)` | `O(V)` |
| DFS iterativo | `O(V + E)` | `O(V)` |

El análisis asume una representación por adyacencias y operaciones de conjuntos/diccionarios de costo constante promedio. `V` y `E` se refieren a la porción alcanzable del grafo; almacenar el árbol requiere espacio adicional `O(V)`.

## Visualizaciones

- **Originales:** Graphviz `sfdp`, motor de fuerzas multiescala relacionado con Yifan Hu.
- **Árboles BFS y DFS:** Graphviz `dot`, con disposición jerárquica.
- **Entregables:** 72 archivos `.gv`, 72 imágenes PNG y 36 SVG adicionales de árboles de 100 y 500 nodos.

Los SVG permiten ampliar árboles grandes sin pérdida de calidad.

## Instalación y ejecución

Se requiere **Python 3** y **Graphviz** con los ejecutables `dot` y `sfdp` disponibles. La versión inicial de `grafos.py` también importa `numpy`, `pandas` y `matplotlib`.

### macOS (Homebrew)

```bash
brew install graphviz
python -m pip install numpy pandas matplotlib
dot -V
```

**Gephi es opcional.** Es una aplicación de escritorio para explorar y visualizar grafos, no una dependencia necesaria de `generar_resultados.py`. Se puede instalar en macOS mediante:

```bash
brew install --cask gephi
```

### Reproducir los experimentos

Desde la raíz del repositorio:

```bash
python generar_resultados.py
```

El programa genera y valida nuevos grafos en **`resultados_2_prueba/`**. Los resultados originales en **`resultados_2/`** no se modifican.

### Ejemplo de uso de la biblioteca

```python
from grafos import grafo_malla

grafo = grafo_malla(5, 6)
s = grafo.nodos[(1, 1)]

arbol_bfs = grafo.BFS(s)
arbol_dfs_r = grafo.DFS_R(s)
arbol_dfs_i = grafo.DFS_I(s)
```

## Entregables

- Biblioteca y script Python, más notebook de pruebas.
- **18** grafos originales y **54** árboles calculados (`.gv`).
- **72** imágenes PNG y **36** SVG adicionales.
- **180 archivos de resultados** en total.
