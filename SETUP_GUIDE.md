# Quick Setup Guide for Google Colab

## 30-Second Quick Start

### Option 1: Upload Notebook to Colab (Easiest)
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click "File" → "Upload notebook"
3. Select `colab_solver.ipynb` from this repository
4. Follow the cells step-by-step

### Option 2: Run from GitHub
In a Colab cell, run:
```python
!git clone https://github.com/tu-usuario/tfg.git
%cd tfg
!pip install -r requirements.txt
```

## What You'll Need

### 1. Data Files (3 CSV files)
Upload these to Colab or have them in Google Drive:
- `escenarios_historicos_completos.csv`
- `parametros_tecnologicos.csv`
- `potencia_instalada_agregada_tecnologia.csv`

**Format Requirements:**
- UTF-8 encoding
- `;` as separator (semicolon)
- Headers in first row

### 2. Gurobi License
Get a free academic license:
- Visit: https://www.gurobi.com/academia/
- Request academic license
- You'll receive WLS credentials (3 values):
  - Access ID
  - Secret
  - License ID

### 3. Google Account
- For Colab (free)
- For Google Drive (to store data/results)

## Step-by-Step Instructions

### In Google Colab:

**Cell 1: Mount Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
```

**Cell 2: Clone Repository**
```python
import os
os.chdir('/content')
!git clone https://github.com/tu-usuario/tfg.git
%cd tfg
```

**Cell 3: Install Dependencies**
```python
!pip install gurobipy pandas
```

**Cell 4: Upload Data Files**
```python
from google.colab import files
print("Select your 3 CSV files:")
uploaded = files.upload()

for filename in uploaded:
    os.rename(filename, f'data/{filename}')
```

**Cell 5: Set Gurobi License**
```python
import os
os.environ['GUROBI_WLSACCESSID'] = 'your_access_id_here'
os.environ['GUROBI_WLSSECRET'] = 'your_secret_here'
os.environ['GUROBI_LICENSEID'] = 'your_license_id_here'
```

**Cell 6: Run Optimizer**
```python
from solver_por_tecnologia import resolver_mpec_tramos_max_min
resolver_mpec_tramos_max_min(data_dir='data', output_dir='results')
```

**Cell 7: Download Results**
```python
import shutil
shutil.make_archive('resultados', 'zip', 'results')
files.download('resultados.zip')
```

## CSV File Preparation

### How to create the CSV files correctly:

**In Microsoft Excel or LibreOffice Calc:**
1. Create spreadsheet with required columns
2. Fill data
3. Save As → Format: "CSV (.csv)" or "Text CSV"
4. When asked about delimiter, choose "Semicolon"
5. Encoding: "UTF-8"
6. Result: `filename.csv`

**Using Python:**
```python
import pandas as pd

df = pd.read_csv('your_file.csv', sep=';', encoding='utf-8-sig')
df.to_csv('your_file.csv', sep=';', encoding='utf-8-sig', index=False)
```

**Using LibreOffice from Command Line:**
```bash
libreoffice --headless --convert-to csv --outdir . input.xlsx
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'gurobipy'"
```python
!pip install gurobipy
```

### "No Gurobi license found"
1. Check your license credentials are correct
2. Make sure you've obtained a Gurobi academic license
3. Try using WLS (Web License Server) instead of local license

### "CSV file not found"
- Make sure file is in `data/` folder
- Check exact filename matches requirement
- Verify encoding is UTF-8

### "UnicodeDecodeError in CSV"
- CSV file encoding issue
- Open in LibreOffice, save as UTF-8 with semicolon separator
- Try: `pd.read_csv(file, sep=';', encoding='utf-8-sig')`

### Colab session timeout
- Colab sessions timeout after 12 hours of inactivity
- Save results frequently
- For large computations, download intermediate results

## File Structure in Colab

After running all cells:
```
/content/tfg/
├── solver_por_tecnologia.py
├── colab_solver.ipynb
├── requirements.txt
├── data/
│   ├── escenarios_historicos_completos.csv (uploaded)
│   ├── parametros_tecnologicos.csv (uploaded)
│   └── potencia_instalada_agregada_tecnologia.csv (uploaded)
└── results/
    ├── Max/
    │   ├── MPEC_MAX_Invierno_0000.csv
    │   ├── MPEC_MAX_Invierno_0100.csv
    │   └── ... (more files)
    └── Min/
        ├── MPEC_MIN_Invierno_0000.csv
        ├── MPEC_MIN_Invierno_0100.csv
        └── ... (more files)
```

## Output Files Explanation

**results/Max/** - Maximum market power scenarios
- Each file: `MPEC_MAX_[Season]_[Hour].csv`
- Shows scenario where market power is maximized for the leader generator

**results/Min/** - Minimum market power scenarios
- Each file: `MPEC_MIN_[Season]_[Hour].csv`
- Shows scenario where market power is minimized for the leader generator

Column meanings:
- `Pi_m_Endogeno_EUR`: Endogenous market price
- `Beneficio_Lider_EUR`: Total benefit for leader
- `Potencia_Casada_MW`: Power matched in each generation segment

## Getting Help

1. Check [README.md](README.md) for full documentation
2. See [CLAUDE.md](CLAUDE.md) for technical details
3. Check [example_usage.py](example_usage.py) for code examples
4. Visit [Gurobi Docs](https://www.gurobi.com/documentation/) for optimization help

## Security Note

⚠️ **Never share your Gurobi license credentials!**
- They're personal to your academic license
- If shared, others could misuse your license
- If compromised, regenerate them in Gurobi account
- In collaborative notebooks, use Colab Secrets (Settings → Secrets)

## Next Steps

1. ✅ Prepare your CSV data files
2. ✅ Get Gurobi academic license
3. ✅ Open colab_solver.ipynb in Google Colab
4. ✅ Follow the cells step-by-step
5. ✅ Download your results!

Good luck! 🚀
