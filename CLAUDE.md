# MPEC Economic Dispatch Optimizer - Project Documentation

## Project Overview

This is a Thesis project (TFG) implementing an MPEC (Mathematical Programming with Equilibrium Constraints) optimizer for economic dispatch analysis in electricity markets. The solver identifies extreme scenarios (maximum and minimum market power) for different generator leaders.

## Key Information

### Technology Stack
- **Language**: Python 3.8+
- **Optimization**: Gurobi (requires license)
- **Data Processing**: pandas
- **Execution**: Local Python or Google Colab

### Project Structure
```
├── solver_por_tecnologia.py    # Main optimizer logic (refactored for flexible paths)
├── colab_solver.ipynb          # Google Colab notebook with complete setup
├── example_usage.py            # Usage examples
├── requirements.txt            # Python dependencies
├── data/                       # Input CSV files (git ignored, keep .gitkeep)
└── results/                    # Output results (git ignored)
```

### Important Files
- `solver_por_tecnologia.py`: Main script - takes `data_dir` and `output_dir` as parameters
- `colab_solver.ipynb`: Copy this to Google Colab for cloud execution
- `.gitignore`: Configured to ignore large CSV files and results

## Changes Made for Colab Compatibility

1. **Flexible Path Handling**: Replaced hardcoded Windows paths with parameterized `data_dir` and `output_dir`
2. **Documentation**: Created comprehensive README and inline documentation
3. **Requirements**: Created requirements.txt for easy dependency installation
4. **Example Scripts**: Added example_usage.py showing different configurations
5. **Colab Notebook**: Full step-by-step notebook for cloud execution
6. **Error Messages**: Improved error handling with helpful messages

## Development Notes

### Function Signature
```python
resolver_mpec_tramos_max_min(data_dir='data', output_dir='results')
```

Parameters:
- `data_dir`: Directory containing CSV input files
- `output_dir`: Directory where results will be saved (creates Max/ and Min/ subdirectories)

### Input CSV Files Required
1. `escenarios_historicos_completos.csv` - Historical scenarios
2. `parametros_tecnologicos.csv` - Technology parameters
3. `potencia_instalada_agregada_tecnologia.csv` - Installed capacity

All CSV files must be UTF-8 encoded with `;` as separator.

### Output Files
- `results/Max/MPEC_MAX_[Estacion]_[Hora].csv` - Maximum market power scenarios
- `results/Min/MPEC_MIN_[Estacion]_[Hora].csv` - Minimum market power scenarios

## Gurobi License Configuration

### For Colab (recommended)
Use Web License Server (WLS) credentials:
```python
import os
os.environ['GUROBI_WLSACCESSID'] = 'your_id'
os.environ['GUROBI_WLSSECRET'] = 'your_secret'
os.environ['GUROBI_LICENSEID'] = 'your_license_id'
```

### Local Development
Academic license via `grbgetkey` or environment variables.

## Usage Patterns

### Local Execution
```bash
pip install -r requirements.txt
python solver_por_tecnologia.py
```

### Colab Execution
1. Upload colab_solver.ipynb to Google Colab
2. Follow step-by-step instructions in notebook
3. Mount Drive, upload data, configure Gurobi, run optimizer

### Custom Configuration
```python
from solver_por_tecnologia import resolver_mpec_tramos_max_min
resolver_mpec_tramos_max_min(data_dir='path/to/data', output_dir='path/to/output')
```

## Git Workflow

- `.gitignore` ignores large CSV files and results directories
- `data/.gitkeep` ensures data/ directory is tracked
- Keep solver code, notebooks, and documentation in git
- CSV data and results are user-provided/generated, not committed

## Common Issues & Solutions

1. **Gurobi License Error**: Verify WLS credentials or run `grbgetkey`
2. **CSV Not Found**: Ensure files are in `data/` directory with exact names
3. **Encoding Issues**: Save CSV as UTF-8 with `;` separator
4. **Colab Module Errors**: Run `!pip install --upgrade gurobipy pandas`

## Future Improvements

- Add data validation module
- Create CLI with argparse for parameter management
- Add progress callbacks/logging
- Create test suite with sample data
- Add visualization of results

## Contact & License

This is a TFG (Thesis Project) - see README.md for details.
