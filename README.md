# Proyecto 4 — Árboles de Expansión Mínima (MST)

**Diseño y Análisis de Algoritmos**  
Maestría en Ciencias en Ingeniería de Cómputo — CIC-IPN

## Descripción

Utilizando la biblioteca de grafos desarrollada en los proyectos anteriores, se implementaron tres algoritmos para calcular el árbol de expansión mínima (*Minimum Spanning Tree*, MST) de un grafo no dirigido, ponderado y conexo.

Los algoritmos implementados en la clase `Grafo` son:

- **Kruskal directo:** utiliza Union-Find con compresión de caminos y unión por tamaño.
- **Kruskal inverso:** elimina aristas de mayor a menor peso, verificando la conectividad mediante BFS.
- **Prim:** utiliza una cola de prioridad (`heapq`) para seleccionar las aristas de menor peso.

## Generación de grafos

Se utilizaron seis modelos de generación:

1. Malla
2. Erdős–Rényi
3. Gilbert
4. Geográfico
5. Barabási–Albert
6. Dorogovtsev–Mendes

Para cada modelo se generaron dos grafos, de **30 y 500 nodos**, asignando pesos aleatorios entre 1 y 10.

Se utilizó una semilla base de 42 para garantizar la reproducibilidad de los resultados.

## Estructura del proyecto

```text
├── grafos.py
├── validando_MST.py
├── generar_resultados_mst.py
└── resultados_4/
    ├── malla/
    ├── erdos_renyi/
    ├── gilbert/
    ├── geografico/
    ├── barabasi_albert/
    └── dorogovtsev_mendes/
```

Cada carpeta contiene los grafos originales, los árboles calculados y sus visualizaciones.

## Ejecución

Se requiere Python 3, las dependencias utilizadas por la biblioteca y Graphviz para generar las imágenes.

**Validar los algoritmos:**

```bash
python validando_MST.py
```

**Generar los resultados y visualizaciones:**

```bash
python generar_resultados_mst.py
```

## Validación

Se verificó que los árboles obtenidos cumplieran las siguientes propiedades:

- Contener todos los nodos originales.
- Tener exactamente `V - 1` aristas.
- Ser conexos y no contener ciclos.
- Conservar las aristas y sus pesos originales.
- Presentar el mismo peso total en los tres algoritmos.

Los tres algoritmos coincidieron en el peso del MST para los **12 grafos evaluados**.

## Entregables

- Código fuente de los algoritmos.
- Archivos `.gv` de los grafos originales y sus MST.
- Visualizaciones en formato PNG y SVG.
- Tablas con los pesos de los MST obtenidos.
- Validaciones y comparaciones de tiempos de ejecución.

