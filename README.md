# Despacho Económico - MPEC Optimizer

Optimizador MPEC (Mathematical Programming with Equilibrium Constraints) para la extracción de escenarios extremos de despacho económico en mercados de energía eléctrica.

## Estructura del Proyecto

```
tfg/
├── solver_por_tecnologia.py      # Script principal del optimizador
├── colab_solver.ipynb            # Notebook para Google Colab
├── requirements.txt              # Dependencias Python
├── data/                         # Carpeta para archivos de entrada (CSV)
│   ├── escenarios_historicos_completos.csv
│   ├── parametros_tecnologicos.csv
│   └── potencia_instalada_agregada_tecnologia.csv
├── results/                      # Carpeta para resultados (generada automáticamente)
│   ├── Max/                      # Escenarios con máximo poder de mercado
│   └── Min/                      # Escenarios con mínimo poder de mercado
└── README.md                     # Este archivo
```

## Requisitos

### Localmente
- Python 3.8+
- Gurobi Optimizer (licencia académica)
- pandas
- gurobipy

### Google Colab
- Cuenta de Google
- Archivos CSV de datos
- Licencia Gurobi WLS (Web License Server)

## Instalación Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tfg.git
cd tfg
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Gurobi

#### Opción A: Licencia WLS (Web License Server)
```python
# En tu script o antes de ejecutar:
import gurobipy as gp
options = {
    "WLSACCESSID": "tu_access_id",
    "WLSSECRET": "tu_secret",
    "LICENSEID": tu_license_id,
}
env = gp.Env(params=options)
```

#### Opción B: Licencia académica local
```bash
# Obtén tu licencia en https://www.gurobi.com/academia/
grbgetkey your_key_here
```

### 4. Preparar datos
Coloca tus archivos CSV en la carpeta `data/`:
- `escenarios_historicos_completos.csv`
- `parametros_tecnologicos.csv`
- `potencia_instalada_agregada_tecnologia.csv`

Los archivos deben estar en formato UTF-8 con separador `;`

### 5. Ejecutar el optimizador
```bash
python solver_por_tecnologia.py
```

## Uso en Google Colab

### Opción 1: Usar el Notebook Colab
1. Abre [Google Colab](https://colab.research.google.com/)
2. Sube el archivo `colab_solver.ipynb`
3. Sigue las instrucciones en el notebook

### Opción 2: Crear un nuevo Notebook
1. Crea un nuevo notebook en Colab
2. Copia las celdas del `colab_solver.ipynb`
3. Sigue los pasos:

```python
# 1. Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Instalar dependencias
!pip install gurobipy pandas

# 3. Configurar Gurobi WLS
import os
os.environ['GUROBI_WLSACCESSID'] = 'tu_access_id'
os.environ['GUROBI_WLSSECRET'] = 'tu_secret'
os.environ['GUROBI_LICENSEID'] = 'tu_license_id'

# 4. Descargar y ejecutar el solver
!git clone https://github.com/tu-usuario/tfg.git
%cd tfg
from solver_por_tecnologia import resolver_mpec_tramos_max_min
resolver_mpec_tramos_max_min(data_dir='data', output_dir='results')
```

## Archivos de Entrada (CSV)

### escenarios_historicos_completos.csv
Contiene datos históricos por estación y hora.

Columnas requeridas:
- `Estacion`: Estación del año
- `Hora`: Hora del día (HH:MM)
- `Tecnologia`: Tipo de tecnología de generación
- `Demanda_Total_MWh`: Demanda total en MWh
- `P_Historico_MW`: Potencia histórica en MW

### parametros_tecnologicos.csv
Parámetros de cada tecnología.

Columnas requeridas:
- `Tecnologia`: Nombre de la tecnología
- `LCOE_EUR_MWh`: Costo levelizado de energía
- `Delta_Flexibilidad`: Factor de flexibilidad

### potencia_instalada_agregada_tecnologia.csv
Capacidad instalada por tecnología.

Columnas requeridas:
- `Tec. generacion`: Nombre de la tecnología
- `Potencia máxima MW`: Potencia máxima instalada

## Archivos de Salida

Los resultados se guardan en CSV con siguiente estructura:

**results/Max/MPEC_MAX_[Estacion]_[Hora].csv**
- Escenarios con máximo poder de mercado para el líder

**results/Min/MPEC_MIN_[Estacion]_[Hora].csv**
- Escenarios con mínimo poder de mercado para el líder

Columnas de salida:
- `Estacion`: Estación procesada
- `Hora`: Hora procesada
- `Demanda_MWh`: Demanda total
- `Lider_Evaluado`: Generador líder evaluado
- `Tipo_Escenario`: MAX_PODER_MERCADO o MIN_PODER_MERCADO
- `Pi_m_Endogeno_EUR`: Precio endógeno del mercado
- `Beneficio_Lider_EUR`: Beneficio total del líder
- `Tramo`: ID del tramo de oferta
- `Tecnologia`: Tecnología del tramo
- `C_Oferta_EUR`: Costo de oferta del tramo
- `Potencia_Casada_MW`: Potencia casada en el tramo

## Troubleshooting

### Error de Gurobi License
```
Gurobi Error 10009: No Gurobi license found
```
**Solución**: Verifica que las credenciales WLS sean correctas o que hayas ejecutado `grbgetkey`.

### Error de archivos CSV no encontrados
**Solución**: Asegúrate que los archivos estén en la carpeta `data/` con los nombres exactos.

### Error de codificación (encoding)
**Solución**: Los archivos CSV deben estar en UTF-8 con BOM. Usa Excel o un editor de texto como VS Code para guardar correctamente.

### Google Colab: módulos no encontrados
**Solución**: Ejecuta `!pip install --upgrade gurobipy pandas` en una celda antes de importar.

## Licencia

Trabajo de Fin de Grado (TFG)

## Contacto

Para preguntas o issues, abre un issue en GitHub o contacta al autor.
