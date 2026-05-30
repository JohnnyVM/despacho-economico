import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import math
import os
from pathlib import Path

def resolver_mpec_tramos_max_min(data_dir='data', output_dir='results'):
    """
    Optimizador MPEC para extracción de escenarios extremos.

    Args:
        data_dir: Directorio donde están los archivos CSV de entrada
        output_dir: Directorio donde se guardarán los resultados
    """
    print("="*85)
    print(" OPTIMIZADOR MPEC - EXTRACCIÓN DE ESCENARIOS EXTREMOS (MÁXIMO Y MÍNIMO) ")
    print("="*85)

    # Crear directorios si no existen
    Path(data_dir).mkdir(exist_ok=True)
    output_dir_min = Path(output_dir) / 'Min'
    output_dir_max = Path(output_dir) / 'Max'
    output_dir_min.mkdir(parents=True, exist_ok=True)
    output_dir_max.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------------------
    # 1. CARGA DE BASES DE DATOS (CSV)
    # ---------------------------------------------------------------------------------
    try:
        hist_file = Path(data_dir) / 'escenarios_historicos_completos.csv'
        tec_file = Path(data_dir) / 'parametros_tecnologicos.csv'
        cap_file = Path(data_dir) / 'potencia_instalada_agregada_tecnologia.csv'

        df_hist = pd.read_csv(hist_file, sep=';', encoding='utf-8-sig')
        df_tec = pd.read_csv(tec_file, sep=';', encoding='utf-8-sig')
        df_cap = pd.read_csv(cap_file, sep=';', encoding='utf-8-sig')
    except FileNotFoundError as e:
        print(f"Error cargando archivos: {e}")
        print(f"Asegúrate de que los archivos CSV estén en: {Path(data_dir).absolute()}")
        return

    # Mapeo de capacidades instaladas
    map_nombres = {'Ciclo combinado': 'Ciclo Comb.', 'Solar Fotovoltaica': 'Solar FV'}
    df_cap['Tec. generacion'] = df_cap['Tec. generacion'].replace(map_nombres)
    CAP_INSTALADA = dict(zip(df_cap['Tec. generacion'], df_cap['Potencia máxima MW']))

    # Parámetros Tecnológicos globales
    LCOE = dict(zip(df_tec['Tecnologia'], df_tec['LCOE_EUR_MWh']))
    DELTA = dict(zip(df_tec['Tecnologia'], df_tec['Delta_Flexibilidad']))

    # Parámetros Termodinámicos y de Contorno
    P_MAX_UNIT_CC = 491.19 # [MW] Potencia máxima monoeje.
    P_MIN_UNIT_CC = 196.48 # [MW] Mínimo técnico de estabilidad.
    EPSILON = 0.001        # Horquilla de tolerancia balance demanda.

    # Lista de escenarios (Estación y Hora) a simular
    escenarios = df_hist[['Estacion', 'Hora']].drop_duplicates().values.tolist()

    # Credenciales Gurobi WLS
    options = {
        "WLSACCESSID": "8093c9f6-faa4-4192-ae77-b9bf98403d40",
        "WLSSECRET": "b872a856-1174-41c9-83a8-bee19421c570",
        "LICENSEID": 2757221,
    }
    
    try:
        env = gp.Env(params=options)
    except gp.GurobiError as e:
        print(f"Error de Licencia Gurobi: {e}")
        return

    # ---------------------------------------------------------------------------------
    # 2. ITERACIÓN SOBRE ESCENARIOS HORARIOS
    # ---------------------------------------------------------------------------------
    for estacion, hora in escenarios:
        print(f"\n>> Procesando Escenario: {estacion} - {hora} ...")
        
        df_hora = df_hist[(df_hist['Estacion'] == estacion) & (df_hist['Hora'] == hora)]
        D = df_hora['Demanda_Total_MWh'].iloc[0]
        P_HIST = dict(zip(df_hora['Tecnologia'], df_hora['P_Historico_MW']))
        
        # Cálculo de la demanda térmica de punta para Must-Run
        df_punta = df_hist[(df_hist['Estacion'] == estacion) & (df_hist['Hora'] == '20:00') & (df_hist['Tecnologia'] == 'Ciclo Comb.')]
        P_PUNTA_CC = df_punta['P_Historico_MW'].iloc[0] if not df_punta.empty else 0.0
        
        n_cc = math.ceil(P_PUNTA_CC / P_MAX_UNIT_CC)
        P_MR_CC = n_cc * P_MIN_UNIT_CC

        G = list(P_HIST.keys())
        
        # Definición de Tramos
        TRAMOS = {
            'k_nuc_1': {'g': 'Nuclear',      'C_k': 0.00,                 'Pmin': 0.0, 'Pmax': P_HIST['Nuclear']},
            'k_eol_1': {'g': 'Eólica',       'C_k': 0.00,                 'Pmin': 0.0, 'Pmax': P_HIST['Eólica']},
            'k_sol_1': {'g': 'Solar FV',     'C_k': 0.00,                 'Pmin': 0.0, 'Pmax': P_HIST['Solar FV']},
            'k_cog_1': {'g': 'Cogeneración', 'C_k': LCOE['Cogeneración'], 'Pmin': 0.0, 'Pmax': P_HIST['Cogeneración'] * (1 + DELTA['Cogeneración'])},
            'k_cc_1':  {'g': 'Ciclo Comb.',  'C_k': 0.00,                 'Pmin': 0.0, 'Pmax': P_MR_CC},
            'k_cc_2':  {'g': 'Ciclo Comb.',  'C_k': LCOE['Ciclo Comb.'],  'Pmin': 0.0, 'Pmax': 10000.0},
            'k_cc_3':  {'g': 'Ciclo Comb.',  'C_k': 125.00,               'Pmin': 0.0, 'Pmax': CAP_INSTALADA.get('Ciclo Comb.', 21361.9)},
            'k_hid_1': {'g': 'Hidráulica',   'C_k': 0.00,                 'Pmin': 0.0, 'Pmax': 4500.0},
            'k_hid_2': {'g': 'Hidráulica',   'C_k': 82.00,                'Pmin': 0.0, 'Pmax': 14000.0},
            'k_hid_3': {'g': 'Hidráulica',   'C_k': 140.00,               'Pmin': 0.0, 'Pmax': CAP_INSTALADA.get('Hidráulica', 20339.6)}
        }

        K = list(TRAMOS.keys())
        K_g = {g: [k for k in K if TRAMOS[k]['g'] == g] for g in G}

        # Variables para rastrear los escenarios MÁXIMO y MÍNIMO
        mejor_beneficio_global = -float('inf')
        peor_beneficio_global = float('inf')
        
        casacion_max = []
        casacion_min = []
        lider_max = ""
        lider_min = ""

        # -----------------------------------------------------------------------------
        # 3. EVALUACIÓN DE TODOS LOS LÍDERES
        # -----------------------------------------------------------------------------
        for LIDER in G:
            m = gp.Model("MPEC", env=env)
            m.Params.NonConvex = 2
            m.Params.OutputFlag = 0

            p = m.addVars(K, lb=0, vtype=GRB.CONTINUOUS)
            pi_m_minus = m.addVar(lb=0, vtype=GRB.CONTINUOUS)
            pi_m_plus = m.addVar(lb=0, vtype=GRB.CONTINUOUS)
            pi_m = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS)
            mu = m.addVars(K, lb=0, vtype=GRB.CONTINUOUS)
            lam = m.addVars(K, lb=0, vtype=GRB.CONTINUOUS)
            u = m.addVars(K, vtype=GRB.BINARY)
            v = m.addVars(K, vtype=GRB.BINARY)
            w_plus = m.addVar(vtype=GRB.BINARY)
            w_minus = m.addVar(vtype=GRB.BINARY)

            # Función Objetivo
            obj = gp.quicksum((pi_m - TRAMOS[k]['C_k']) * p[k] for k in K_g[LIDER])
            m.setObjective(obj, GRB.MAXIMIZE)

            # Restricciones
            m.addConstr((pi_m == pi_m_plus - pi_m_minus))
            m.addConstr((gp.quicksum(p[k] for k in K) >= D * (1 - EPSILON)))
            m.addConstr((gp.quicksum(p[k] for k in K) <= D * (1 + EPSILON)))
            m.addConstrs((p[k] >= TRAMOS[k]['Pmin'] for k in K))
            m.addConstrs((p[k] <= TRAMOS[k]['Pmax'] for k in K))
            m.addConstrs((TRAMOS[k]['C_k'] - pi_m + mu[k] - lam[k] == 0 for k in K))

            for k in K:
                m.addConstr((u[k] == 1) >> (mu[k] == 0))
                m.addConstr((u[k] == 0) >> (TRAMOS[k]['Pmax'] - p[k] == 0))
                m.addConstr((v[k] == 1) >> (lam[k] == 0))
                m.addConstr((v[k] == 0) >> (p[k] - TRAMOS[k]['Pmin'] == 0))

            m.addConstr((w_plus == 1) >> (pi_m_plus == 0))
            m.addConstr((w_plus == 0) >> (D * (1 + EPSILON) - gp.quicksum(p[k] for k in K) == 0))
            m.addConstr((w_minus == 1) >> (pi_m_minus == 0))
            m.addConstr((w_minus == 0) >> (gp.quicksum(p[k] for k in K) - D * (1 - EPSILON) == 0))

            m.optimize()

            # -------------------------------------------------------------------------
            # 4. CAPTURA DUAL DE DATOS (MÁXIMO Y MÍNIMO)
            # -------------------------------------------------------------------------
            if m.Status == GRB.OPTIMAL:
                obj_val = m.ObjVal
                pi_final = pi_m.X
                
                # Recopilamos los datos de la iteración actual
                iteracion_actual = []
                for k in K:
                    iteracion_actual.append({
                        'Estacion': estacion,
                        'Hora': hora,
                        'Demanda_MWh': round(D, 2),
                        'Lider_Evaluado': LIDER,
                        'Pi_m_Endogeno_EUR': round(pi_final, 2),
                        'Beneficio_Lider_EUR': round(obj_val, 2),
                        'Tramo': k,
                        'Tecnologia': TRAMOS[k]['g'],
                        'C_Oferta_EUR': TRAMOS[k]['C_k'],
                        'Potencia_Casada_MW': round(p[k].X, 2)
                    })

                # Verificamos si es el nuevo MÁXIMO global
                if obj_val > mejor_beneficio_global:
                    mejor_beneficio_global = obj_val
                    lider_max = LIDER
                    casacion_max = iteracion_actual

                # Verificamos si es el nuevo MÍNIMO global
                if obj_val < peor_beneficio_global:
                    peor_beneficio_global = obj_val
                    lider_min = LIDER
                    casacion_min = iteracion_actual

        # -----------------------------------------------------------------------------
        # 5. GUARDADO DE LOS DOS ESCENARIOS EXTREMOS
        # -----------------------------------------------------------------------------
        if casacion_max and casacion_min:
            df_max = pd.DataFrame(casacion_max)
            df_min = pd.DataFrame(casacion_min)

            # Etiquetamos el tipo de extremo en el propio DataFrame antes de guardar
            df_max.insert(4, 'Tipo_Escenario', 'MAX_PODER_MERCADO')
            df_min.insert(4, 'Tipo_Escenario', 'MIN_PODER_MERCADO')

            file_max = output_dir_max / f"MPEC_MAX_{estacion}_{hora.replace(':','')}.csv"
            file_min = output_dir_min / f"MPEC_MIN_{estacion}_{hora.replace(':','')}.csv"

            df_max.to_csv(file_max, index=False, sep=';', encoding='utf-8-sig')
            df_min.to_csv(file_min, index=False, sep=';', encoding='utf-8-sig')
            
            print(f"  [+] MAX guardado -> Líder: {lider_max} ({casacion_max[0]['Pi_m_Endogeno_EUR']} €/MWh | {mejor_beneficio_global:,.2f} €)")
            print(f"  [-] MIN guardado -> Líder: {lider_min} ({casacion_min[0]['Pi_m_Endogeno_EUR']} €/MWh | {peor_beneficio_global:,.2f} €)")
        else:
            print("  [!] Fallo en la convergencia para esta hora.")

    print("\n" + "="*85)
    print(" OPTIMIZACIÓN FINALIZADA. ARCHIVOS MAX Y MIN GENERADOS CON ÉXITO. ")
    print("="*85)

if __name__ == "__main__":
    # Cambia estos parámetros según donde tengas tus archivos
    resolver_mpec_tramos_max_min(data_dir='data', output_dir='results')