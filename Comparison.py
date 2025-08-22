import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
from f_tco_n_ghg import TCO_ICEV,TCO_FCEV,TCO_BEV,GHG_ICEV,GHG_FCEV,GHG_BEV

def get_ipva_and_fuel_price(df, uf, dolar, exchange):
    al = df.loc[df['UF'] == uf, 'al'].values[0]
    fp = df.loc[df['UF'] == uf, 'fp'].values[0]
    if exchange == 'BRL(R$)':
        fp = fp * dolar
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

def input_with_tooltip(label, tooltip, widget, *args, **kwargs):
    st.markdown(f"""
    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
        {label}
        <div class="tooltip-container">ⓘ
            <div class="tooltip-text">{tooltip}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return widget(*args, **kwargs)

def display_metrics(result_ghg, result_tco, exchange): 
    def custom_metric(label, value, info="", last=False):
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

            <div style='padding: 4px 0; {"margin-bottom:20px;" if last else ""}'>
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
        custom_metric('GHG', f'{result_ghg[0]:.2f} t CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'R$ {result_tco[0]:,.2f} (BRL)', 'Total Cost of Ownership in BRL.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (BRL/km)', 'Cost per kilometer (BRL).', last=True)
    else:
        custom_metric('GHG', f'{result_ghg[0]:.2f} t CO₂eq', 'Total GHG emissions over the vehicle’s lifecycle.')
        st.divider()
        custom_metric('GHG/km', f'{result_ghg[1]:.2f} g CO₂eq/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', f'$ {result_tco[0]:,.2f} (USD)', 'Total Cost of Ownership in USD.')
        st.divider()
        custom_metric('LCOD', f'{result_tco[1]:.2f} (USD/km)', 'Cost per kilometer (USD).', last=True) 

st.set_page_config(layout='wide')
st.markdown("# Comparison")
st.sidebar.markdown("# Comparison")

st.markdown("""
<style>
.tooltip-container {
    position: relative;
    display: inline-block;
    cursor: pointer;
    font-size: 14px;
    color: #808080;
}

.tooltip-container .tooltip-text {
    visibility: hidden;
    width: 180px;
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
    transform: translateX(0%);
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
    white-space: normal;
}

.tooltip-container:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
                    <div style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-25px;'>
                        Select the currency
                        <div class="tooltip-container">ⓘ
                            <div class="tooltip-text">Select the currency.</div>
                        </div>
                    </div>
                    <style>
                    div[data-baseweb="radio"] {
                        margin-bottom: 20px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
    exchange = st.radio('', ['BRL(R$)','USD($)'])
                
main_filter_comparison = st.segmented_control(
    "Comparison",
    ["ICEV", "EV", "FCEV"],
    selection_mode="multi")

if len(main_filter_comparison) < 2:
    st.warning('You must select at least two options to use this function.')
    execute = 0
else:
    column = st.columns(len(main_filter_comparison), border=True)

    inputs = {'ICEV': {}, 'FCEV': {}, 'EV': {}}
    
    for i, category in enumerate(main_filter_comparison):
        with column[i]:
            st.subheader(category)
            erros = []
    
            if category == 'ICEV':
                vehicle_specs = {
                    'Sub Compacto': {'mass': 800, 'fuel_eco': 10.5},
                    'Compacto': {'mass': 1000, 'fuel_eco': 9.5},
                    'Médio': {'mass': 1200, 'fuel_eco': 8.6},
                    'Grande': {'mass': 1450, 'fuel_eco': 7.8},
                    'Extra Grande': {'mass': 1700, 'fuel_eco': 7.1},
                    'Onix 2024': {'mass': 1034, 'fuel_eco': 9.3}
                }
                fuel_options = ['E100', 'E27']
                df = pd.read_csv(r'C:\Users\bernardo.cossetin\Desktop\ProjetoH2\App_H2\inputs_ET.csv', decimal='.')
    
            elif category == 'EV':
                vehicle_specs = {
                    'Sub Compacto': {'mass': 800, 'fuel_eco': 10.5},
                    'Compacto': {'mass': 1000, 'fuel_eco': 9.5},
                    'Médio': {'mass': 1200, 'fuel_eco': 8.6},
                    'Grande': {'mass': 1450, 'fuel_eco': 7.8},
                    'Extra Grande': {'mass': 1700, 'fuel_eco': 7.1},
                    'TESTE': {'mass': 977, 'fuel_eco': 0.1233}
                }
                fuel_options = ['BEV']
                df = pd.read_csv(r'C:\Users\bernardo.cossetin\Desktop\ProjetoH2\App_H2\inputs_EV.csv', decimal='.')
    
            else:  # FCEV
                vehicle_specs = {
                    'Sub Compacto': {'mass': 800, 'fuel_eco': 100},
                    'Compacto': {'mass': 1000, 'fuel_eco': 105},
                    'Médio': {'mass': 1200, 'fuel_eco': 110},
                    'Grande': {'mass': 1450, 'fuel_eco': 115},
                    'Extra Grande': {'mass': 1700, 'fuel_eco': 120},
                    'Toyota Mirai 2023': {'mass': 1900, 'fuel_eco': 122}
                }
                fuel_options = ['H2']
                df = pd.read_csv(r'C:\Users\bernardo.cossetin\Desktop\ProjetoH2\App_H2\inputs_H2.csv', decimal='.')

            tipo = input_with_tooltip(
                "Type", "Fuel type.",
                st.selectbox, "", fuel_options, key=f"tipo_{category}")
            inputs[category]["tipo"] = tipo
    
            veh_cat = input_with_tooltip(
                "Category", "Vehicle Category.",
                st.selectbox, "", list(vehicle_specs.keys()), key=f"veh_cat_{category}")
            inputs[category]["veh_cat"] = veh_cat
    
            veh_cost = input_with_tooltip(
                "Vehicle Cost", "Purchase cost of the vehicle.",
                st.number_input, "", min_value=0.0, step=0.01, format="%.2f", key=f"veh_cost_{category}")
            if veh_cost <= 0.009:
                erros.append("Please enter a valid *Vehicle Cost*.")
            inputs[category]["veh_cost"] = veh_cost
    
            fe_pad = st.session_state.get(f"fe_pad_{category}", False)
            fuel_eco_labels = {
                'ICEV': ("Fuel Eco (km/L)", "Fuel economy in kilometers per liter."),
                'EV': ("Energy Consumption (kWh/km)", "Energy consumption in kilometers per kilowatt-hour."),
                'FCEV': ("Fuel Eco (km/kg H₂)", "Fuel economy in kilometers per kilogram of hydrogen.")}
            label, tip = fuel_eco_labels[category]
    
            fuel_eco = input_with_tooltip(
                label, tip,
                st.number_input, "", min_value=0.0, step=0.01, format="%.2f",
                disabled=fe_pad, key=f"fuel_eco_{category}")
            st.toggle('Default Fuel Economy', key=f"fe_pad_{category}")
    
            if not fe_pad and fuel_eco <= 0.0:
                erros.append("Please enter a valid *Fuel Economy*.")
            if fe_pad:
                fuel_eco = vehicle_specs[veh_cat]['fuel_eco']
            inputs[category]["fuel_eco"] = fuel_eco
    
            years = input_with_tooltip(
                "Years", "Vehicle lifetime.",
                st.number_input, "", min_value=0, key=f"years_{category}")
            if years <= 0:
                erros.append("Please enter the *Vehicle Lifetime*.")
            inputs[category]["years"] = years
    
            yearly_mileage = input_with_tooltip(
                "Yearly mileage", "Number of kilometers driven per year.",
                st.number_input, "", min_value=0, key=f"mileage_{category}")
            if yearly_mileage <= 0:
                erros.append("Please enter the *Annual Mileage*.")
            inputs[category]["yearly_mileage"] = yearly_mileage
    
            if category == 'EV':
                veh_bat_cap = input_with_tooltip(
                    "Battery capacity", "Battery capacity",
                    st.number_input, "", min_value=0.0, step=0.01, key=f"bat_cap_{category}")
                if veh_bat_cap <= 0:
                    erros.append("Please enter the *Battery Capacity*.")
                inputs[category]["battery_capacity"] = veh_bat_cap
    
            uf = input_with_tooltip(
                "UF", "Federative unit.",
                st.selectbox, "", df['UF'].unique(), key=f"uf_{category}")
            inputs[category]["uf"] = uf
    
            dolar = 4.98  # get_dolar()
    
            if category == 'ICEV':
                al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange)
                ghg_fuel_e = get_ghg_fuel(tipo, uf, df)
                inputs[category].update({"al": al, "fp": fp, "ghg_fuel_e": ghg_fuel_e})
    
            elif category == 'EV':
                tf = df.loc[df['UF'] == uf, 'tf'].values[0]
                ghg_kwh = df.loc[df['UF'] == uf, 'ghg_kwh'].values[0]
                al = df.loc[df['UF'] == uf, 'al'].values[0]
                inputs[category].update({"al": al, "tf": tf, "ghg_kwh": ghg_kwh})
    
            elif category == 'FCEV':
                al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange)
                inputs[category].update({"al": al, "fp": fp})
    
            W = vehicle_specs[veh_cat]['mass']
            inputs[category]["mass"] = W
    
            execute = (len(erros) == 0)

if st.button('Apply', disabled=not execute):
    with st.spinner('Wait...'):
        time.sleep(1)
    st.session_state.executou = True
    st.session_state.ultima_moeda = exchange  
    params=inputs
    results = {}
    for cat, params in inputs.items():
        if cat in main_filter_comparison:
            if cat == "ICEV":
                result_ghg = GHG_ICEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"], params["ghg_fuel_e"])
                result_tco = TCO_ICEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["al"], params["uf"], params["fp"], exchange, dolar)
    
            elif cat == "EV":
                result_ghg = GHG_BEV(params["mass"], params["yearly_mileage"], params["fuel_eco"], 
                                     params["years"], params["ghg_kwh"], params["battery_capacity"])
                result_tco = TCO_BEV(params["veh_cost"], params["fuel_eco"], params["years"], 
                                     params["yearly_mileage"], params["tf"], params["al"], dolar, exchange, params["battery_capacity"])
    
            elif cat == "FCEV":
                result_ghg = GHG_FCEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"])
                result_tco = TCO_FCEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["fp"], params["al"], exchange, dolar)

            results[cat] = {"GHG": result_ghg, "TCO": result_tco}

    simbol = 'BRL(R$)' if exchange == 'BRL(R$)' else 'USD($)'

    fig_ghg = go.Figure()
    for cat, vals in results.items():
        fig_ghg.add_trace(go.Scatter(
            x=list(range(1, years + 1)),
            y=vals["GHG"][2],
            mode='lines+markers',
            name=f'{cat} - GHG'
        ))
    fig_ghg.update_layout(
        title=dict(text="GHG Emissions Over Time", font=dict(size=28, family="Arial")),
        xaxis=dict(title=dict(text='Year', font=dict(size=24)), tickfont=dict(size=20)),
        yaxis=dict(title=dict(text='GHG Emissions (t CO₂eq)', font=dict(size=24)), tickformat=',.2f', tickfont=dict(size=20)),
        width=1200,
        height=650,
        hovermode='x unified'
    )

    fig_tco = go.Figure()
    for cat, vals in results.items():
        fig_tco.add_trace(go.Scatter(
            x=list(range(1, years + 1)),
            y=vals["TCO"][2],
            mode='lines+markers',
            name=f'{cat} - TCO'
        ))
    fig_tco.update_layout(
        title=dict(text="Cumulative Total Cost of Ownership", font=dict(size=28, family="Arial")),
        xaxis=dict(title=dict(text='Ano', font=dict(size=24)), tickfont=dict(size=20)),
        yaxis=dict(title=dict(text=f'Total Cost of Ownership {simbol}', font=dict(size=24)), tickformat=',.0f', tickfont=dict(size=20)),
        width=1200,
        height=650,
        hovermode='x unified'
    )

    st.header("Results")
    st.divider()

    cols = st.columns(len(main_filter_comparison),border=True)

    for i, cat in enumerate(main_filter_comparison):
        if cat in results:
            with cols[i]:
                st.subheader(cat)
                st.divider()
                display_metrics(results[cat]['GHG'], results[cat]['TCO'], exchange)
                

    with st.container(border=True):
        tab1, tab2 = st.tabs(['GHG', 'TCO'])
        with tab1:
            st.plotly_chart(fig_ghg, use_container_width=True)
        with tab2:
            st.plotly_chart(fig_tco, use_container_width=True)


if 'executou' not in st.session_state:
    st.session_state.executou = False

if 'ultima_moeda' not in st.session_state:
    st.session_state.ultima_moeda = 'BRL(R$)'

if st.session_state.executou:
    if exchange != st.session_state.ultima_moeda:
        st.warning("You changed the currency before executing. Please verify the vehicle cost input, if you don't adjust it to match the selected currency, the result may be inaccurate.")