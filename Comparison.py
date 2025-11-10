import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
from f_tco_n_ghg import TCO_ICEV,TCO_FCEV,TCO_BEV,GHG_ICEV,GHG_FCEV,GHG_BEV
from veh_data_base import veh_data_base

def get_ipva_and_fuel_price(df, uf, dolar, exchange, category):
    al = df.loc[df['UF'] == uf, 'al'].values[0]
    if category =='ICEV with Ethanol':
        fp = df.loc[df['UF'] == uf, 'fp_e100'].values[0]
    else:
        fp = df.loc[df['UF'] == uf, 'fp_e27'].values[0]
    if exchange == 'USD($)':
        fp = fp / dolar
    return al, fp

def get_ghg_fuel(tipo, uf, df, category):
    if category =='ICEV with Ethanol':
        return df.loc[df['UF'] == uf, 'ghg_fuel_e'].values[0]
    else:
        LHV = 39.32  
        d = 0.754    
        wtw = 75.07  
        return LHV * d * wtw

def get_dolar(): 
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

def category_card(category, bg_color="#f0f2f6", border_color="#333"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color}; 
            padding: 5px; 
            border-radius: 10px; 
            margin-bottom: 25px;
            border-left: 6px solid {border_color};">
            <h3 style="margin-top:0;font-size:22px;">{category}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def category_card_placeholder():
    st.markdown(
        """
        <div style="
            padding: 5px; 
            margin-bottom: 25px;
            border-radius: 10px; 
            border-left: 6px solid transparent; 
            background-color: transparent;
        ">
            <h3 style="
                margin-top:0;
                font-size:22px; 
                height: 2.5em; 
                visibility: hidden;
            "></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_metric_titles(exchange):
    def custom_metric(label, info="", last=False):
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

            <div style='padding: 10px 0; {"margin-bottom:20px;" if last else ""}'>
                <div style='font-size:22px; font-weight:bold; display: flex; align-items: center; gap: 6px; justify-content: center;'>
                    {label}
                    <div class="tooltip-container" style="font-size:15px; color:#808080;">ⓘ
                        <div class="tooltip-text">{info}</div>
                    </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if exchange == 'BRL(R$)':
        custom_metric('GHG', 'Total GHG emissions over the vehicle’s lifecycle. Includes vehicle production, fuel use (with state-specific emission factors from production and transport), and recycling credits. Zero point = only production emissions.')
        st.divider()
        custom_metric('GHG/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', 'Total Cost of Ownership in BRL. Total Cost of Ownership with depreciation, regional fuel price (per state), insurance, taxes, maintenance, and resale value at end-of-life (flattening the curve).')
        st.divider()
        custom_metric('LCOD', 'Cost per kilometer (BRL).', last=True)
    else:
        custom_metric('GHG', 'Total GHG emissions over the vehicle’s lifecycle. Includes vehicle production, fuel use (with state-specific emission factors from production and transport), and recycling credits. Zero point = only production emissions.')
        st.divider()
        custom_metric('GHG/km', 'GHG emissions per kilometer.')
        st.divider()
        custom_metric('TCO', 'Total Cost of Ownership in USD. Total Cost of Ownership with depreciation, regional fuel price (per state), insurance, taxes, maintenance, and resale value at end-of-life (flattening the curve).')
        st.divider()
        custom_metric('LCOD', 'Cost per kilometer (USD).', last=True)

def display_metrics(result_ghg, result_tco, exchange, category):
    def custom_metric(value, last=False):
        st.markdown(
            f"""
            <div style='padding: 10px 0; {"margin-bottom:20px;" if last else ""}'>
                <div style='font-size:22px;text-align: center;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if category == 'ICEV with Ethanol':
        if exchange == 'BRL(R$)':
            custom_metric(f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric(f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric(f'R$ {result_tco[0]:.2f} (BRL)')
            st.divider()
            custom_metric(f'{result_tco[1]:.2f} (BRL/km)', last=True)
        else:
            custom_metric(f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric(f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric(f'$ {result_tco[0]:.2f} (USD)')
            st.divider()
            custom_metric(f'{result_tco[1]:.2f} (USD/km)', last=True)
            
    elif category == 'ICEV with Gasoline':
        if exchange == 'BRL(R$)':
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'R$ {result_tco[0]:.2f} (BRL)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (BRL/km)', last=True)
        else:
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'$ {result_tco[0]:.2f} (USD)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (USD/km)', last=True)
            
    elif category == 'BEV':
        if exchange == 'BRL(R$)':
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'R$ {result_tco[0]:.2f} (BRL)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (BRL/km)', last=True)
        else:
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'$ {result_tco[0]:.2f} (USD)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (USD/km)', last=True)
            
    elif category == 'FCEV with PV':
        if exchange == 'BRL(R$)':
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'R$ {result_tco[0]:.2f} (BRL)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (BRL/km)', last=True)
        else:
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'$ {result_tco[0]:.2f} (USD)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (USD/km)', last=True)
            
    else: # FCEV with SMR
        if exchange == 'BRL(R$)':
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'R$ {result_tco[0]:.2f} (BRL)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (BRL/km)', last=True)
        else:
            custom_metric( f'{result_ghg[0]:.2f} t CO₂eq')
            st.divider()
            custom_metric( f'{result_ghg[1]:.2f} g CO₂eq/km')
            st.divider()
            custom_metric( f'$ {result_tco[0]:.2f} (USD)')
            st.divider()
            custom_metric( f'{result_tco[1]:.2f} (USD/km)', last=True)

st.sidebar.markdown(
    """
    <div style="
        background-color: #FFFFFF; 
        padding: 5px; 
        border-radius: 10px; 
        margin-bottom: 5px;
        border-left: 6px solid #223067;">
        <h3 style="font-size:20px;margin-top:0;">Comparison</h3>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar.container():
    st.markdown("""
                        <div>
                        <h3 style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-50px;'>
                            Category Comparison</h3>
                        </div>
                        <style>
                        div[data-baseweb="radio"] {
                            margin-bottom: 20px;
                        }
                        </style>
                        """, unsafe_allow_html=True)          
    main_filter_comparison = st.sidebar.multiselect(
            "",
            ["ICEV with Ethanol", "ICEV with Gasoline", "BEV", "FCEV", "FCEV with PV"])
    
with st.sidebar.container():
    st.markdown("""
                        <div>
                        <h3 style='font-size:16px; font-weight:bold; display:flex; align-items:center; gap:6px; margin-bottom:-50px;'>
                            Select the currency</h3>
                        </div>
                        <style>
                        div[data-baseweb="radio"] {
                            margin-bottom: 20px;
                        }
                        </style>
                        """, unsafe_allow_html=True)
    exchange = st.sidebar.radio('', ['BRL(R$)','USD($)'])

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

category_styles = {
    "ICEV with Ethanol": {"bg": "#E4E4E4", "border": "#223067"},
    "ICEV with Gasoline": {"bg": "#E4E4E4", "border": "#223067"},
    "BEV": {"bg": "#E4E4E4", "border": "#223067"},
    "FCEV": {"bg": "#E4E4E4", "border": "#223067"},
    "FCEV with PV": {"bg": "#E4E4E4", "border": "#223067"}
}

if len(main_filter_comparison) < 2:
    st.warning('You must select at least two options to use this function.')
    execute = 0
else:
    inputs = {
        'ICEV with Ethanol': {},
        'ICEV with Gasoline': {},
        'FCEV': {},
        'FCEV with PV': {},
        'BEV': {},
        'BEV with PV': {}
    }

    max_cols = 3  
    
    for start in range(0, len(main_filter_comparison), max_cols):
        subset = main_filter_comparison[start:start + max_cols]
        columns = st.columns(max_cols)
        for i, category in enumerate(subset):
            with columns[i]:
                with st.container(border=True):

                    category_card(category, category_styles[category]["bg"], category_styles[category]["border"])
    
                    erros = []
            
                    if category == 'ICEV with Ethanol':
                        vdb = veh_data_base('ICEV')
                        fuel_options = ['E100']
                        df = pd.read_csv('inputs_ET.csv', decimal='.')
                    
                    elif category == 'ICEV with Gasoline':
                        vdb = veh_data_base('ICEV')
                        fuel_options = ['E27']
                        df = pd.read_csv('inputs_ET.csv', decimal='.')
                    
                    elif category == 'BEV':
                        vdb = veh_data_base('BEV')
                        fuel_options = ['BEV']
                        df = pd.read_csv('inputs_EV.csv', decimal='.')
                        
                    elif category == 'FCEV with PV':
                        vdb = veh_data_base('FCEV')
                        fuel_options = ['PV H2']
                        df = pd.read_csv('inputs_H2.csv', decimal='.')
            
                    elif category == 'FCEV':
                        vdb = veh_data_base('FCEV')
                        fuel_options = ['H2']
                        df = pd.read_csv('inputs_H2.csv', decimal='.')
                    
                    tipo = input_with_tooltip(
                        "Type", "Fuel type.",
                        st.selectbox, "", fuel_options, key=f"tipo_{category}")
                    inputs[category]["tipo"] = tipo
            
                    veh_cat = input_with_tooltip(
                        "Category", "Generic vehicle categories with default mass and fuel economy (both shown in results). Values can be customized.",
                        st.selectbox, "", list(vdb.columns), key=f"veh_cat_{category}")
                    inputs[category]["veh_cat"] = veh_cat
            
                    veh_cost = input_with_tooltip(
                        "Vehicle Cost", "Purchase cost of the vehicle.",
                        st.number_input, "", min_value=0.0, step=0.01, format="%.2f", key=f"veh_cost_{category}")
                    if veh_cost <= 0.009:
                        st.markdown("""
                                    <div style='color:red; font-size:14px; margin-top:-10px; margin-bottom:-5px;'>
                                    Please enter a valid *Vehicle Cost*
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                    )
                        st.markdown("""
                        <style>
                        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Vehicle Cost:"] {
                           ;border: 2px solid red !important; 
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        erros.append("Please enter a valid *Vehicle Cost*.")
                    inputs[category]["veh_cost"] = veh_cost
            
                    fe_pad = st.session_state.get(f"fe_pad_{category}", False)
                    fuel_eco_labels = {
                        'ICEV with Ethanol': ("Fuel Eco (km/L)", "Fuel economy in kilometers per liter."),
                        'ICEV with Gasoline': ("Fuel Eco (km/L)", "Fuel economy in kilometers per liter."),
                        'BEV': ("Energy Consumption (kWh/km)", "Energy consumption in kilometers per kilowatt-hour."),
                        'FCEV': ("Fuel Eco (km/kg H₂)", "Fuel economy in kilometers per kilogram of hydrogen."),
                        'FCEV with PV': ("Fuel Eco (km/kg H₂)", "Fuel economy in kilometers per kilogram of hydrogen.")}
                    label, tip = fuel_eco_labels[category]
            
                    fuel_eco = input_with_tooltip(
                        label, tip,
                        st.number_input, "", min_value=0.0, step=0.01, format="%.2f",
                        disabled=fe_pad, key=f"fuel_eco_{category}")
                    st.toggle('Default Fuel Economy', key=f"fe_pad_{category}")
            
                    if not fe_pad and fuel_eco <= 0.0:
                        st.markdown("""
                                    <div style='color:red; font-size:14px; margin-top:-10px; margin-bottom:-5px;'>
                                    Please enter a valid *Fuel Economy*
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                    )
                        st.markdown("""
                        <style>
                        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Fuel Eco:"] {
                            border: 2px solid red !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        erros.append("Please enter a valid *Fuel Economy*.")
                    if fe_pad:
                        if category == 'ICEV with Ethanol':
                            fuel_eco = vdb[veh_cat]['Ethanol Fuel Economy [km/L]']
                        elif category == 'ICEV with Gasoline':
                            fuel_eco = vdb[veh_cat]['Gasoline Fuel Economy [km/L]']
                        elif category == 'BEV':
                            fuel_eco = vdb[veh_cat]['Electric Fuel Economy [kWh/km]']
                        elif category == 'FCEV':
                            fuel_eco = vdb[veh_cat]['Hydrogen Fuel Economy [km/kg H₂]']
                        elif category == 'FCEV with PV':
                            fuel_eco = vdb[veh_cat]['Hydrogen Fuel Economy [km/kg H₂]']
                    inputs[category]["fuel_eco"] = fuel_eco
            
                    years = input_with_tooltip("Year","Vehicle lifetime", st.slider,"", 1, 20, 10, key=f"years_{category}")
                    st.markdown("""
                        <style>
                        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Years:"] {
                            border: 2px solid red !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                    inputs[category]["years"] = years
            
                    yearly_mileage = input_with_tooltip(
                        "Yearly mileage", "Number of kilometers driven per year.",
                        st.number_input, "", min_value=0, key=f"mileage_{category}")
                    if yearly_mileage <= 0:
                        st.markdown("""
                                    <div style='color:red; font-size:14px; margin-top:-10px; margin-bottom:-5px;'>
                                    Please enter a valid *Annual Mileage*.
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                    )
                        st.markdown("""
                        <style>
                        div[data-testid="stNumberInput"] input[data-baseweb="input"][aria-label="Yearly Mileage:"] {
                            border: 2px solid red !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        erros.append("Please enter the *Annual Mileage*.")
                    inputs[category]["yearly_mileage"] = yearly_mileage
            
                    if category == 'BEV':
                        veh_bat_cap = input_with_tooltip(
                            "Battery capacity", "Battery capacity",
                            st.number_input, "", min_value=0.0, step=0.01, key=f"bat_cap_{category}")
                        if veh_bat_cap <= 0:
                            st.markdown("""
                                        <div style='color:red; font-size:14px; margin-top:-10px; margin-bottom:-5px;'>
                                        Please enter a valid *Battery capacity*.
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                        )
                            erros.append("Please enter the *Battery Capacity*.")
                        inputs[category]["battery_capacity"] = veh_bat_cap
            
                    uf = input_with_tooltip(
                        "UF", "Federative unit.",
                        st.selectbox, "", df['UF'].unique(), key=f"uf_{category}")
                    inputs[category]["uf"] = uf
                    
                    dolar = 4.98  # get_dolar()
            
                    if category == 'ICEV with Ethanol':
                        al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange, category)
                        ghg_fuel_e = get_ghg_fuel(tipo, uf, df, category)
                        inputs[category].update({"al": al, "fp": fp, "ghg_fuel_e": ghg_fuel_e})
            
                    elif category == 'ICEV with Gasoline':
                        al, fp = get_ipva_and_fuel_price(df, uf, dolar, exchange, category)
                        ghg_fuel_e = get_ghg_fuel(tipo, uf, df, category)
                        inputs[category].update({"al": al, "fp": fp, "ghg_fuel_e": ghg_fuel_e})
            
                    elif category == 'BEV':
                        tf = df.loc[df['UF'] == uf, 'tf'].values[0]
                        ghg_kwh = df.loc[df['UF'] == uf, 'ghg_kwh'].values[0]
                        al = df.loc[df['UF'] == uf, 'al'].values[0]
                        inputs[category].update({"al": al, "tf": tf, "ghg_kwh": ghg_kwh})
            
                    elif category == 'FCEV':
                        al = df.loc[df['UF'] == uf, 'al'].values[0]
                        fp = df.loc[df['UF'] == uf, 'fp'].values[0]
                        if exchange == 'BRL(R$)':
                            fp = fp * dolar
                        inputs[category].update({"al": al, "fp": fp})
                        
                    elif category == 'FCEV with PV':
                        al = df.loc[df['UF'] == uf, 'al'].values[0]
                        fp = df.loc[df['UF'] == uf, 'fp_pv'].values[0]
                        if exchange == 'BRL(R$)':
                            fp = fp * dolar
                        inputs[category].update({"al": al, "fp": fp})
            
                    W = vdb[veh_cat]['Vehicle Mass [kg]']
                    inputs[category]["mass"] = W
            
                    execute = (len(erros) == 0)

if st.sidebar.button('Apply', disabled=not execute, use_container_width=True):
    with st.spinner('Wait...'):
        time.sleep(1)
    st.session_state.executou = True
    st.session_state.ultima_moeda = exchange  
    params=inputs
    results = {}
    for cat, params in inputs.items():
        if cat in main_filter_comparison:
            if cat == "ICEV with Ethanol":
                result_ghg = GHG_ICEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"], params["ghg_fuel_e"])
                result_tco = TCO_ICEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["al"], params["uf"], params["fp"], exchange, dolar)
                
            elif cat == "ICEV with Gasoline":
                result_ghg = GHG_ICEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"], params["ghg_fuel_e"])
                result_tco = TCO_ICEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["al"], params["uf"], params["fp"], exchange, dolar)
    
            elif cat == "BEV":
                result_ghg = GHG_BEV(params["mass"], params["yearly_mileage"], params["fuel_eco"], 
                                     params["years"], params["ghg_kwh"], params["battery_capacity"])
                result_tco = TCO_BEV(params["veh_cost"], params["fuel_eco"], params["years"], 
                                     params["yearly_mileage"], params["tf"], params["al"], dolar, exchange, params["battery_capacity"])
    
            elif cat == "FCEV":
                result_ghg = GHG_FCEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"])
                result_tco = TCO_FCEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["fp"], params["al"], exchange, dolar)
                
            elif cat == "FCEV with PV":
                result_ghg = GHG_FCEV(params["tipo"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["mass"], params["years"])
                result_tco = TCO_FCEV(params["veh_cost"], params["yearly_mileage"], 
                                      params["fuel_eco"], params["years"], params["fp"], params["al"], exchange, dolar)

            results[cat] = {"GHG": result_ghg, "TCO": result_tco}

    simbol = 'BRL(R$)' if exchange == 'BRL(R$)' else 'USD($)'

    fig_ghg = go.Figure()
    for cat, vals in results.items():
        fig_ghg.add_trace(go.Scatter(
            x=list(range(0, years + 1)),
            y=vals["GHG"][2],
            mode='lines+markers',
            name=f'{cat} - GHG'
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
    for cat, vals in results.items():
        fig_tco.add_trace(go.Scatter(
            x=list(range(1, years + 1)),
            y=vals["TCO"][2],
            mode='lines+markers',
            name=f'{cat} - TCO'
        ))
    fig_tco.update_layout(
        title=dict(text="Cumulative Total Cost of Ownership", font=dict(size=28, family="Arial")),
        xaxis=dict(title=dict(text='Year', font=dict(size=24)), tickfont=dict(size=24)),
        yaxis=dict(title=dict(text=f'Total Cost of Ownership {simbol}', font=dict(size=24)), tickformat=',.0f', tickfont=dict(size=24),gridcolor="gray"),
        width=1200,
        height=650,
        hovermode='x unified'
    )

    st.header("Results")
    st.divider()

    col_disc, col_result = st.columns([1,8],border=False)
    
    with col_disc:
        category_card_placeholder()
        display_metric_titles(exchange)
    with col_result:
        cols = st.columns(len(main_filter_comparison),border=False)
        for i, cat in enumerate(main_filter_comparison):
            if cat in results:
                with cols[i]:
                    category_card(cat, category_styles[category]["bg"], category_styles[category]["border"])
                    display_metrics(results[cat]['GHG'], results[cat]['TCO'], exchange, category)            

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
