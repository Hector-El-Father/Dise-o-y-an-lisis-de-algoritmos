# Proyecto 5 — Algoritmo de Eades (Spring Embedder)

**Diseño y Análisis de Algoritmos**  
**Maestría en Ciencias en Ingeniería de Cómputo — CIC-IPN**

## 1. Descripción

Implementación en Python del algoritmo de Eades para la distribución y visualización de grafos mediante fuerzas de atracción y repulsión.

El proyecto reutiliza una biblioteca propia de grafos e incorpora una visualización animada con Pygame, cálculo optimizado de fuerzas y generación automatizada de evidencias.

## 2. Modelos de generación

Se implementaron visualizaciones para seis modelos:

1. Malla
2. Erdős–Rényi
3. Gilbert
4. Geográfico
5. Barabási–Albert
6. Dorogovtsev–Mendes

Cada modelo se ejecuta con **100 y 500 nodos**, generando un total de **12 simulaciones**, con 600 iteraciones predeterminadas.

## 3. Algoritmo de Eades

El algoritmo utiliza las siguientes magnitudes de fuerza:

**Atracción entre nodos adyacentes:**

`Fa(d) = c1 * log(d / c2)`

**Repulsión entre nodos no adyacentes:**

`Fr(d) = c3 / sqrt(d)`

**Actualización de posiciones:**

`P(t+1) = P(t) + c4 * F(t)`

Parámetros utilizados:

| Parámetro | Valor |
|---|---:|
| c1 | 2 |
| c2 | 50 |
| c3 | 1 |
| c4 | 0.2 |
| Iteraciones | 600 |

Se desarrolló una versión optimizada que evalúa cada pareja de nodos una sola vez y aplica fuerzas opuestas a ambos vértices.

La complejidad temporal del cálculo de fuerzas permanece en **Θ(n²) por iteración**.

## 4. Estructura del proyecto

```text
├── grafos.py
├── spring.py
├── generadores_spring.py
├── visualizar_spring.py
├── lote_eades.py
├── requirements.txt
├── README.md
└── resultados_5/
    ├── capturas/
    └── capitulos_youtube.txt
```

**Descripción de los archivos principales:**

- `grafos.py`: biblioteca de grafos y modelos de generación.
- `spring.py`: fuerzas de atracción, repulsión y actualización de posiciones.
- `generadores_spring.py`: configuración de los seis modelos.
- `visualizar_spring.py`: simulación animada, registro de tiempos y exportación de evidencias.
- `lote_eades.py`: automatización de las 12 ejecuciones.
- `requirements.txt`: dependencias de Python.

## 5. Instalación

Clonar la rama del proyecto:

```bash
git clone -b proyecto-5-eades https://github.com/Hector-El-Father/Dise-o-y-an-lisis-de-algoritmos.git
cd Dise-o-y-an-lisis-de-algoritmos
```

Crear y activar el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 6. Ejecución

**Simulación de 100 nodos:**

```bash
python visualizar_spring.py --modelo malla --nodos 100
```

**Simulación de 500 nodos:**

```bash
python visualizar_spring.py --modelo barabasi_albert --nodos 500 --iteraciones 600
```

**Generación automática de las 12 ejecuciones:**

```bash
python lote_eades.py
```

El modo lote genera capturas y videos de las simulaciones.

## 7. Evidencias y resultados

### Video de ejecución

Se presenta un montaje de las 12 simulaciones, organizado por modelo de generación y cantidad de nodos. El video contiene capítulos para identificar cada grafo.

**[Ver video completo del Proyecto 5 en YouTube](https://www.youtube.com/watch?v=2300jAKpl0c)**

### Capturas de pantalla

Las capturas de los grafos de 100 y 500 nodos se encuentran en:

**[Ver capturas de los grafos](resultados_5/capturas/)**

Las imágenes se identifican por el nombre del modelo y el número de nodos, por ejemplo:

- `malla_100.png`
- `malla_500.png`
- `barabasi_albert_100.png`
- `barabasi_albert_500.png`

Los videos MP4 individuales no se almacenan en el repositorio para evitar archivos pesados.

## 8. Consideraciones

Las simulaciones utilizan un número fijo de iteraciones para facilitar su comparación.

Alcanzar las 600 iteraciones no garantiza la convergencia ni la eliminación de cruces entre aristas.

Las coordenadas del grafo se ajustan únicamente durante la visualización para mantener los vértices dentro de la ventana, sin modificar el cálculo de fuerzas.

## 9. Referencia

Eades, P. (1984). *A heuristic for graph drawing*. Congressus Numerantium, 42, 149–160.

