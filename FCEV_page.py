import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
from f_tco_n_ghg import GHG_FCEV, TCO_FCEV
from veh_data_base import veh_data_base
from datetime import datetime, timedelta

st.markdown("""
    <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

vdb_FCEV = veh_data_base('FCEV')

df = pd.read_csv('inputs_H2.csv',decimal='.')

def get_ipva_and_fuel_price(df, uf, dolar, exchange, tipo):
    if tipo == 'H2':
        al = df.loc[df['UF'] == uf, 'al'].values[0]
        fp = df.loc[df['UF'] == uf, 'fp'].values[0]
    else:
        al = df.loc[df['UF'] == uf, 'al'].values[0]
        fp = df.loc[df['UF'] == uf, 'fp_pv'].values[0]
    if exchange == 'BRL(R$)':
        fp = fp * dolar
    return al, fp

def dolar_ptax():
    hoje = datetime.today()
    for dias_atras in range(0, 7):
        data = hoje - timedelta(days=dias_atras)
        data_str = data.strftime("%m-%d-%Y")  
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data_str}'&$format=json"
        )
        r = requests.get(url)
        r.raise_for_status()
        dados = r.json()
        if dados.get("value"):
            return dados["value"][0]["cotacaoVenda"]

def display_metrics(result_ghg, result_tco, exchange): 
    def custom_metric(label, value, info=""):
        st.markdown(
            f"""
            <style>
            .tooltip-main {{
                position: relative;
                display: inline-block;
                cursor: pointer;
                font-size: 14px;
            }}
        
            .tooltip-main .tooltip-text {{
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
        
            .tooltip-main:hover .tooltip-text {{
                visibility: visible;
                opacity: 1;
            }}
            </style>
        
            <div style='padding: 4px 0;'>
                <div style='font-size:22px; font-weight:bold; display: flex; align-items: center; gap: 6px;'>
                    {label}
                    <div class="tooltip-main" style="font-size:15px; color:#808080;">ⓘ
                        <div class="tooltip-text">{info}</div>
                    </div>
                </div>
                <div style='font-size:26px;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if exchange == 'BRL(R$)':
        custom_metric('GHG', f'{result_ghg[0]:.2f} t CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle. Includes vehicle and fuel cell production (plus replacements every ~10 years), hydrogen production, grid losses, state-specific hydrogen emissions, and recycling credits. Zero point = only production emissions.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'R$ {result_tco[0]:.2f} (BRL)', 'Total Cost of Ownership in BRL. Total Cost of Ownership with depreciation, regional hydrogen price (per state), insurance, taxes, maintenance, fuel cell replacements (visible as jumps), and resale value at end-of-life.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (BRL/km)', 'Cost per kilometer (BRL).')
    else:
        custom_metric('GHG', f'{result_ghg[0]:.2f} t CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle. Includes vehicle and fuel cell production (plus replacements every ~10 years), hydrogen production, grid losses, state-specific hydrogen emissions, and recycling credits. Zero point = only production emissions.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'$ {result_tco[0]:.2f} (USD)', 'Total Cost of Ownership in USD. Total Cost of Ownership with depreciation, regional hydrogen price (per state), insurance, taxes, maintenance, fuel cell replacements (visible as jumps), and resale value at end-of-life.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (USD/km)', 'Cost per kilometer (USD).')    

st.header("FCEV - TCO and GHG")
st.sidebar.markdown("""
    <div style="
        background-color: #FFFFFF; 
        padding: 5px; 
        border-radius: 10px; 
        margin-bottom: 25px;
        border-left: 6px solid #223067;">
        <h3 style="font-size:20px;margin-top:0;">FCEV</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
            <style>
.tooltip-container {
    position: relative;
    display: inline-flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    color: #808080;
    line-height: 1; 
    transform: translateY(2px); 
}

.tooltip-container .tooltip-text {
    visibility: hidden;
    width: 150px;
    background-color: #333;
    color: #fff;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    right: 0;
    left: 50%;
    transform: translateX(-25%);
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 14px;
    white-space: normal;
}

.tooltip-container:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }
    </style>
""", unsafe_allow_html=True)

erros = []

with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Type
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Fuel type.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    tipo = st.sidebar.selectbox("", ['H2','PV H2'])
    
with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Category
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Generic vehicle categories with default mass and fuel economy (both shown in results). Values can be customized.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    veh_cat = st.sidebar.selectbox("", list(vdb_FCEV.columns))

with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Vehicle Cost
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Purchase cost of the vehicle, excluding financing and subsidies.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    veh_cost = st.number_input("", min_value=0.0, step=0.01, format="%.2f", key="veh_cost")
    if veh_cost <= 0.009:
        st.markdown("<span style='color:red; font-size:14px;'>Please enter a valid *Vehicle Cost*</span>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Vehicle Cost:"] {
           ;border: 2px solid red !important; 
        }
        </style>
        """, unsafe_allow_html=True)
        erros.append("Please enter a valid *Vehicle Cost*.")

with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Select the currency
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Rates sourced from the Central Bank of Brazil (PTAX).</div>
        </div>
    </div>
    <style>
    div[data-baseweb="radio"] {{
        margin-top: 5px !important;
        margin-bottom: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    exchange = st.sidebar.radio('', ['BRL(R$)','USD($)'])

fe_pad = st.session_state.get("fe_pad", False)
with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Fuel Eco (km/kg)
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Fuel economy in kilometers per H₂ kilogram.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fuel_eco = st.number_input("", min_value=0.0, step=0.01, format="%.2f", disabled=fe_pad, key="fuel_eco")
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
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Years
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Vehicle lifetime.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    years = st.slider("", 1, 20, 10, key="years")
    

with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        Yearly mileage
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">Number of kilometers driven per year.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    yearly_mileage = st.number_input("", min_value=0, key="mileage")
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

with st.sidebar.container():
    st.markdown("""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        UF
    </div>
    <style>
    div[data-baseweb="select"] {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)   
    uf = st.sidebar.selectbox("", df['UF'].unique())

if erros:
    st.info("Fill all required fields to enable analysis.")

dolar = dolar_ptax()
al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange, tipo)

W = vdb_FCEV[veh_cat]['Vehicle Mass [kg]']
if fe_pad:
    fuel_eco = vdb_FCEV[veh_cat]['Hydrogen Fuel Economy [km/kg H₂]']
    
execute = (len(erros)==0)

if st.sidebar.button('Apply',disabled=not execute,use_container_width=True):
    with st.spinner('Wait...'):
        time.sleep(1)
    st.session_state.executou = True
    st.session_state.ultima_moeda = exchange  
    parametros = pd.DataFrame({'Arguments':['Ethanol','Category','Vehicle cost','Weight','Fuel Economy','UF','Fuel price'],
                                   'Values':[tipo,veh_cat,veh_cost,W,fuel_eco,uf,fp]
                                   })
    result_ghg = GHG_FCEV(tipo, yearly_mileage, fuel_eco, W, years)
    result_tco = TCO_FCEV(veh_cost, yearly_mileage, fuel_eco, years, fp, al, exchange, dolar)
    
    if exchange == 'BRL(R$)':
        simbol = 'BRL(R$)'
    else:
        simbol = 'USD($)'
    
    fig_ghg = go.Figure()
    fig_ghg.add_trace(go.Scatter(
        x=list(range(0, years + 1)),
        y=result_ghg[2],
        mode='lines+markers',
        name='GHG acumulado',
        line=dict(color='red',dash='solid')
    ))
    fig_ghg.update_layout(
        title=dict(text="GHG Emissions Over Time", font=dict(size=28, family="Arial")),
        xaxis=dict(title=dict(text='Year', font=dict(size=24)), tickfont=dict(size=24)),
        yaxis=dict(title=dict(text='GHG Emissions (t CO₂eq)', font=dict(size=24)), tickformat=',.2f', tickfont=dict(size=24),gridcolor="gray"),
        width=1200,
        height=650,
        hovermode='x unified'
    )
    
    fig_tco = go.Figure()
    fig_tco.add_trace(go.Scatter(
        x=list(range(1, years + 1)),
        y=result_tco[2],
        mode='lines+markers',
        name='TCO acumulado',
        line=dict(color='red')
    ))
    fig_tco.update_layout(
        title=dict(text="Cumulative Total Cost of Ownership", font=dict(size=28, family="Arial")),
        xaxis=dict(title=dict(text='Ano', font=dict(size=24)), tickfont=dict(size=24)),
        yaxis=dict(title=dict(text=f'Total Cost of Ownership {simbol}', font=dict(size=24)), tickformat=',.0f', tickfont=dict(size=24),gridcolor="gray"),
        width=1200,
        height=650,
        hovermode='x unified'
    )
    
    col_gp, col_df = st.columns([4, 1], border=True)
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

if exchange == 'USD($)':
    data_cotacao = datetime.today().strftime("%d/%m/%Y")
    info_txt = (
        f"The US dollar was quoted today ({data_cotacao}) "
        f"at BRL {dolar:.2f}. Rates sourced from the Central Bank of Brazil (PTAX).")
    st.sidebar.info(info_txt)