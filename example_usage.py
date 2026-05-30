"""
Ejemplo de uso del MPEC Optimizer

Este script muestra cómo usar el optimizador con diferentes configuraciones.
"""

from solver_por_tecnologia import resolver_mpec_tramos_max_min
import os

# Ejemplo 1: Usar directorios por defecto (data/ y results/)
print("Ejemplo 1: Configuración por defecto")
print("-" * 50)
resolver_mpec_tramos_max_min(data_dir='data', output_dir='results')

print("\n" + "=" * 50 + "\n")

# Ejemplo 2: Usar directorios personalizados
print("Ejemplo 2: Directorios personalizados")
print("-" * 50)

# Crear directorios de ejemplo
os.makedirs('custom_data', exist_ok=True)
os.makedirs('custom_results', exist_ok=True)

# Copiar datos a la carpeta personalizada
import shutil
if os.path.exists('data'):
    for file in os.listdir('data'):
        src = os.path.join('data', file)
        dst = os.path.join('custom_data', file)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

# Ejecutar con directorios personalizados
resolver_mpec_tramos_max_min(data_dir='custom_data', output_dir='custom_results')

print("\n" + "=" * 50 + "\n")

# Ejemplo 3: Verificar resultados generados
print("Ejemplo 3: Listar archivos de resultados")
print("-" * 50)

for root, dirs, files in os.walk('results'):
    level = root.replace('results', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in sorted(files)[:5]:  # Mostrar primeros 5 archivos
        print(f'{subindent}{file}')
    if len(files) > 5:
        print(f'{subindent}... y {len(files) - 5} archivos más')

print("\nLos resultados están en las carpetas:")
print("  - results/Max/  : Escenarios con máximo poder de mercado")
print("  - results/Min/  : Escenarios con mínimo poder de mercado")
