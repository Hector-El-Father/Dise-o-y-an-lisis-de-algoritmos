
import subprocess
import sys
MODELOS = [
    "malla",
    "erdos_renyi",
    "gilbert",
    "geografico",
    "barabasi_albert",
    "dorogovtsev_mendes"
]
TAMAÑOS = [100, 500]
total = len(MODELOS) * len(TAMAÑOS)
contador = 0
for n in TAMAÑOS:
    for modelo in MODELOS:
        contador += 1
        print(f"\n{'=' * 55}")
        print(f"Experimento {contador}/{total}")
        print(f"Modelo: {modelo}")
        print(f"Nodos: {n}")
        print(f"{'=' * 55}")
        comando = [
            sys.executable,
            "visualizar_spring.py",
            "--modelo", modelo,
            "--nodos", str(n),
            "--lote"
        ]
        subprocess.run(
            comando,
            check=True
        )
print("\nTodos los experimentos terminaron correctamente.")
