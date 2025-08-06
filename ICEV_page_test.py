import pandas as pd
import streamlit as st
from f_ICEV_2 import GHG_ICEV, TCO_ICEV, GHG_ICEV_ac, TCO_ICEV_ac
import requests
import plotly.graph_objects as go
import time

vehicle_specs = {
    'Sub Compacto': {'mass': 800, 'fuel_eco': 10.5},
    'Compacto': {'mass': 1000, 'fuel_eco': 9.5},
    'Médio': {'mass': 1200, 'fuel_eco': 8.6},
    'Grande': {'mass': 1450, 'fuel_eco': 7.8},
    'Extra Grande': {'mass': 1700, 'fuel_eco': 7.1},
    'Onix 2024': {'mass': 1034, 'fuel_eco': 9.3}
}

df = pd.read_csv('ResultadosGlobais.csv',decimal='.')

def get_ipva_and_fuel_price(df, uf, dolar, exchange):
    al = df.loc[df['UF'] == uf, 'Alíquota IPVA'].values[0]
    fp = df.loc[df['UF'] == uf, 'Fuel Price'].values[0]
    if exchange == 'USD($)':
        fp = fp / dolar
    return al, fp

def get_ghg_fuel(tipo, uf, df):
    if tipo == 'E100':
        return df.loc[df['UF'] == uf, 'ghg_fuel_e'].values[0]
    elif tipo == 'E27':
        LHV = 39.32  
        d = 0.754    
        wtw = 75.07  
        return LHV * d * wtw

def get_dolar(): #Pega dolar atualizado
    resp = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
    return float(resp.json()['USDBRL']['bid'])

def display_metrics(result_ghg, result_tco, exchange): 
    def custom_metric(label, value, info=""):
        st.markdown(
            f"""
            <style>
            .tooltip-container {{
                position: relative;
                display: inline-block;
                cursor: pointer;
                font-size: 12px;
            }}
        
            .tooltip-container .tooltip-text {{
                visibility: hidden;
                width: 300px;
                background-color: #333;
                color: #fff;
                text-align: left;
                border-radius: 6px;
                padding: 14px;
                position: absolute;
                z-index: 1;
                bottom: 125%; 
                left: 50%;
                transform: translateX(-50%);
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 14px;
                white-space: normal;
            }}
        
            .tooltip-container:hover .tooltip-text {{
                visibility: visible;
                opacity: 1;
            }}
            </style>
        
            <div style='padding: 4px 0;'>
                <div style='font-size:22px; font-weight:bold; display: flex; align-items: center; gap: 6px;'>
                    {label}
                    <div class="tooltip-container" style="font-size:15px; color:#808080;">ⓘ
                        <div class="tooltip-text">{info}</div>
                    </div>
                </div>
                <div style='font-size:26px;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if exchange == 'BRL(R$)':
        custom_metric('GHG', f'{result_ghg[0]:.2f} g CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'R$ {result_tco[0]:.2f} (BRL)', 'Total Cost of Ownership in BRL.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (BRL/km)', 'Cost per kilometer (BRL).')
    else:
        custom_metric('GHG', f'{result_ghg[0]:.2f} g CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'$ {result_tco[0]:.2f} (USD)', 'Total Cost of Ownership in USD.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (USD/km)', 'Cost per kilometer (USD).')  

#configuração da página
st.set_page_config(layout='wide')
st.header("ICEV - TCO and GHG")
st.sidebar.markdown("# ICEV - TCO and GHG")

st.markdown("""
    <style>
    /* Opcional: Reduz o espaço entre elementos do sidebar */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

#formulário: lista de erros para armazenar o erro de cada campo e permitir a execução posteriormente com o execute
#cada campo possui sua própia função de erro que notifica ao usuário o campo a ser preenchido (adaptação para tornar mais visual usando html)
erros = []

tipo = st.sidebar.selectbox('Ethanol', ['E100','E27']
        )
veh_cat = st.sidebar.selectbox('Vehicle Category', list(vehicle_specs.keys()))

with st.sidebar.container():
    veh_cost = st.number_input("Vehicle Cost:", min_value=0.0, step=0.01, format="%.2f", key="veh_cost")
    if veh_cost <= 0.009:
        st.markdown("<span style='color:red; font-size:14px;'>Please enter a valid *Vehicle Cost*</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Vehicle Cost:"] {
            border: 2px solid red !important;
        }
        </style>
        """, unsafe_allow_html=True)
        erros.append("Please enter a valid *Vehicle Cost*.")

exchange = st.sidebar.radio('Select the currency:', ['BRL(R$)','USD($)'])

fe_pad = st.session_state.get("fe_pad", False)
with st.sidebar.container():
    fuel_eco = st.number_input("Fuel Eco:", min_value=0.0, step=0.01, format="%.2f", disabled=fe_pad, key="fuel_eco")
    if not fe_pad and fuel_eco <= 0.0:
        st.markdown("<span style='color:red; font-size:14px;'>Please enter a valid *Fuel Economy*</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Fuel Eco:"] {
            border: 2px solid red !important;
        }
        </style>
        """, unsafe_allow_html=True)
        erros.append("Please enter a valid *Fuel Economy*.")

st.sidebar.toggle('Default Fuel Economy', key="fe_pad")

with st.sidebar.container():
    years = st.number_input("Years:", min_value=0, key="years")
    if years <= 0:
        st.markdown("<span style='color:red; font-size:14px;'>Please enter the *Vehicle Lifetime*</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Years:"] {
            border: 2px solid red !important;
        }
        </style>
        """, unsafe_allow_html=True)
        erros.append("Please enter the *Vehicle Lifetime*.")

with st.sidebar.container():
    yearly_mileage = st.number_input("Yearly Mileage:", min_value=0, key="mileage")
    if yearly_mileage <= 0:
        st.markdown("<span style='color:red; font-size:14px;'>Please enter the *Annual Mileage*</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Yearly Mileage:"] {
            border: 2px solid red !important;
        }
        </style>
        """, unsafe_allow_html=True)
        erros.append("Please enter the *Annual Mileage*.")

uf = st.sidebar.selectbox('UF', df['UF'].unique())

if erros:
    st.info("Fill all required fields to enable analysis.")

#busca os valores
al = df.loc[df['UF'] == uf, 'Alíquota IPVA'].values[0]
fp = df.loc[df['UF'] == uf, 'Fuel Price'].values[0]

dolar = 4.98 #get_dolar()
al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange)
fp = round(fp, 2)
ghg_fuel_e = get_ghg_fuel(tipo, uf, df)

W = vehicle_specs[veh_cat]['mass']
if fe_pad:
    fuel_eco = vehicle_specs[veh_cat]['fuel_eco']
#permite a execução/libera o potão de execução
execute = (len(erros)==0)

if st.sidebar.button('Apply',disabled=not execute):
    with st.spinner('Wait...'):
        time.sleep(1)
    st.session_state.executou = True
    st.session_state.ultima_moeda = exchange  
    parametros = pd.DataFrame({'Arguments':['Ethanol','Category','Vehicle cost','Weight','Fuel Economy','UF','Fuel price'],
                                   'Values':[tipo,veh_cat,veh_cost,W,fuel_eco,uf,fp]
                                   })
    result_ghg = GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e)
    result_tco = TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp)
    ghg_anos = GHG_ICEV_ac(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e)
    tco_anos = TCO_ICEV_ac(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp)
    
    if exchange == 'BRL(R$)':
        simbol = 'BRL(R$)'
    else:
        simbol = 'USD($)'
    
    fig_ghg = go.Figure()
    fig_ghg.add_trace(go.Scatter(
        x=list(range(1, years + 1)),
        y=ghg_anos[0],
        mode='lines+markers',
        name='GHG acumulado',
        line=dict(color='red')
    ))
    fig_ghg.update_layout(
        title=dict(text="GHG Emissions Over Time", font=dict(size=26, family="Arial")),
        xaxis=dict(title=dict(text='Year', font=dict(size=20)), tickfont=dict(size=16)),
        yaxis=dict(title=dict(text='GHG Emissions (g CO₂eq)', font=dict(size=20)), tickformat=',.0f', tickfont=dict(size=16)),
        width=1200,
        height=700,
        hovermode='x unified'
    )
    
    fig_tco = go.Figure()
    fig_tco.add_trace(go.Scatter(
        x=list(range(1, years + 1)),
        y=tco_anos[0],
        mode='lines+markers',
        name='TCO acumulado',
        line=dict(color='red')
    ))
    fig_tco.update_layout(
        title=dict(text="Cumulative Total Cost of Ownership", font=dict(size=26, family="Arial")),
        xaxis=dict(title=dict(text='Ano', font=dict(size=20)), tickfont=dict(size=16)),
        yaxis=dict(title=dict(text=f'Total Cost of Ownership {simbol}', font=dict(size=20)), tickformat=',.0f', tickfont=dict(size=16)),
        width=1200,
        height=700,
        hovermode='x unified'
    )
    
    col_gp, col_df = st.columns([3.5, 1], border=True)
    with col_df:
        st.header('Results')
        st.divider()
        display_metrics(result_ghg, result_tco, exchange)
    with col_gp:
        tab1, tab2 = st.tabs(['GHG', 'TCO'])
        with tab1:
            st.plotly_chart(fig_ghg, use_container_width=True)
        with tab2:
            st.plotly_chart(fig_tco, use_container_width=True)
    with st.expander('See the input values used.'):
        st.dataframe(parametros, hide_index=True)
 
if 'executou' not in st.session_state:
    st.session_state.executou = False

if 'ultima_moeda' not in st.session_state:
    st.session_state.ultima_moeda = 'BRL(R$)'

if st.session_state.executou:
    if exchange != st.session_state.ultima_moeda:
        st.warning("You changed the currency before executing. Please verify the vehicle cost input, if you don't adjust it to match the selected currency, the result may be inaccurate.")    
    


    

    

