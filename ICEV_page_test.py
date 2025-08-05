import pandas as pd
import streamlit as st
from f_ICEV_2 import GHG_ICEV, TCO_ICEV, GHG_ICEV_ac
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

df = pd.read_csv(r'C:\Users\bernardo.cossetin\Desktop\ProjetoH2\App_H2\ResultadosGlobais.csv',decimal='.')

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

def display_metrics(result_ghg, result_tco, exchange): #Adaptação para exibição dos resultados, usada para regular a fonte da label (não há função nativa da biblioteca para isso, sendo utilizado html para tal)
    def custom_metric(label, value):
        st.markdown(
            f"""
            <div style='padding: 4px 0;'>
                <div style='font-size:22px; font-weight:bold;'>{label}</div>
                <div style='font-size:26px; '>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    if exchange == 'BRL(R$)':
        custom_metric('GHG', f'{result_ghg[0]:.2f} gCO2eq')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} gCO2eq/km')
        st.divider()
        custom_metric('TCO', f'R$ {result_tco[0]:.2f} (BRL)')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (BRL/km)')
    else:
        custom_metric('GHG', f'{result_ghg[0]:.2f} gCO2eq')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} gCO2eq/km')
        st.divider()
        custom_metric('TCO', f'$ {result_tco[0]:.2f} (USD)')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (USD/km)')    

st.set_page_config(layout='wide')
st.header("ICEV - TCO and GHG")
st.sidebar.markdown("# ICEV - TCO and GHG")

tipo = st.sidebar.selectbox('Ethanol', ['E100','E27']
        )
    
veh_cat = st.sidebar.selectbox('Vehicle Category', list(vehicle_specs.keys())
                               )

veh_cost = st.sidebar.number_input("Vehicle Cost: ",
                               min_value=0.0,
                               step=0.01,
                               format="%.2f"
                               )

exchange = st.sidebar.radio('Select the currency:',
                            ['BRL(R$)','USD($)']
                            )
    
fe_pad = st.session_state.get("fe_pad", False)
fuel_eco = st.sidebar.number_input("Fuel Eco: ",
                               min_value=0.0,
                               step=0.01,
                               format="%.2f",
                               disabled=fe_pad
                               )
st.sidebar.toggle('Default Fuel Economy', key="fe_pad")
    
years = st.sidebar.number_input("Years: ",
                               min_value=0
                               )
    
yearly_mileage = st.sidebar.number_input("Yearly Mileage: ",
                               min_value=0
                               )

uf = st.sidebar.selectbox('UF', df['UF'].unique()
                         )

al = df.loc[df['UF'] == uf, 'Alíquota IPVA'].values[0]
fp = df.loc[df['UF'] == uf, 'Fuel Price'].values[0]

dolar = 4.98 #get_dolar()
al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange)
fp = round(fp, 2)
ghg_fuel_e = get_ghg_fuel(tipo, uf, df)

W = vehicle_specs[veh_cat]['mass']
if fe_pad:
    fuel_eco = vehicle_specs[veh_cat]['fuel_eco']

erros = []

if veh_cost <= 0.009:
    erros.append("Please enter a valid *Vehicle Cost*.")
if fuel_eco <= 0.0:
    erros.append("Please enter a valid *Fuel Economy*.")
if years < 0:
    erros.append("Please enter the *Vehicle Lifetime*.")
if yearly_mileage < 0:
    erros.append("Please enter the *Annual Mileage*.")

if erros:
    for erro in erros:
        st.warning(erro)
    st.info("Fill all required fields to enable analysis.")
    
execute = (len(erros)==0)

if st.sidebar.button('Apply',disabled=not execute):
    with st.spinner('Carregando...'):
        time.sleep(1)
    st.session_state.executou = True
    st.session_state.ultima_moeda = exchange  
    parametros = pd.DataFrame({'Arguments':['Ethanol','Category','Vehicle cost','Weight','Fuel Economy','UF','Fuel price'],
                                   'Values':[tipo,veh_cat,veh_cost,W,fuel_eco,uf,fp]
                                   })
    result_ghg = GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e)
    result_tco = TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp, r=0.1, dr=0.0641, ins=0.06)
    ghg_anos = GHG_ICEV_ac(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e)
    col_gp, col_df = st.columns([2.8, 1], border=True)
    with col_df:
        st.header('Results')
        st.divider()
        display_metrics(result_ghg, result_tco, exchange)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, years + 1)),
        y=ghg_anos[0],
        mode='lines+markers',
        name='GHG acumulado',
        line=dict(color='red')
        ))

    fig.update_layout(
        title=dict(text="GHG Acumulado", font=dict(size=30, family="Arial")),
        xaxis=dict(title=dict(text='Ano', font=dict(size=20))),
        yaxis=dict(title=dict(text='GHG total (kg CO₂e)', font=dict(size=20))),
        width=1200,
        height=700,
        hovermode='x unified'
        )
    with col_gp:
        st.plotly_chart(fig, use_container_width=True)
    with st.expander('See the input values used.'):
        st.dataframe(parametros, hide_index=True)
 
if 'executou' not in st.session_state:
    st.session_state.executou = False

if 'ultima_moeda' not in st.session_state:
    st.session_state.ultima_moeda = 'BRL(R$)'

if st.session_state.executou:
    if exchange != st.session_state.ultima_moeda:
        st.warning("You changed the currency before executing. Please verify the vehicle cost input, if you don't adjust it to match the selected currency, the result may be inaccurate.")    
    


    
    