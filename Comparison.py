# Comparate

import pandas as pd
import streamlit as st
from f_ICEV import GHG_ICEV, TCO_ICEV, GHG_ICEV_ac
import requests
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.markdown("# Comparison")
st.sidebar.markdown("# Comparison")

main_filter_comparison = st.segmented_control("Comparison",["ICEV","EV","FCEV"], selection_mode="multi")

if len(main_filter_comparison) < 2:
    st.warning('You must select at least two options to use this function.')
else:
    column = st.columns(len(main_filter_comparison))
    
    for i, category in enumerate(main_filter_comparison):
        with column[i]:
            if category == 'ICEV':
                st.subheader(category)
                tipo = st.selectbox('Ethanol', 
                                    ['E100','E27'],
                                    )
                    
                veh_cat = st.selectbox('Vehicle Category', 
                                       ['Sub Compacto',
                                        'Compacto',
                                        'Médio',
                                        'Grande',
                                        'Extra Grande'],
                                       key=f"{category}_cat_{i}"
                                 )
        
                veh_cost = st.number_input("Vehicle Cost: ",
                                            min_value=0,
                                            key=f"{category}_cost_{i}"   
                                               )
                    
                fe_pad = st.session_state.get(f"{category}_fepad_{i}", False)
                fuel_eco = st.number_input("Fuel Eco: ",
                                               min_value=0.0,
                                               step=0.01,
                                               format="%.2f",
                                               disabled=fe_pad,
                                               key=f"{category}_fe_{i}"
                                               )
                st.checkbox('Default Fuel Economy', key=f"{category}_fepad_{i}")
                    
                years = st.number_input("Years: ",
                                        min_value=0,
                                        key=f"{category}_years_{i}"
                                        )
                    
                yearly_mileage = st.number_input("Yearly Mileage: ",
                                               min_value=0,
                                               key=f"{category}_mileage_{i}"
                                               )
            elif category == 'EV':
                st.subheader(category)
                veh_cat_EV = st.selectbox('Vehicle Category', 
                                           ['Sub Compacto',
                                            'Compacto',
                                            'Médio',
                                            'Grande',
                                            'Extra Grande'],
                                           key=f"{category}_cat_{i}"
                                 )
        
                veh_cost_EV = st.number_input("Vehicle Cost: ",
                                               min_value=0,
                                               key=f"{category}_cost_{i}"
                                               )
                    
                    
                fe_pad_EV = st.session_state.get(f"{category}_fepad_{i}", False)
                fuel_eco_EV = st.number_input("Fuel Eco: ",
                                               min_value=0.0,
                                               step=0.01,
                                               format="%.2f",
                                               disabled=fe_pad_EV,
                                               key=f"{category}_fe_{i}"
                                               )
                st.checkbox('Default Fuel Economy', key=f"{category}_fepad_{i}")
                    
                years_EV = st.number_input("Years: ",
                                               min_value=0,
                                               key=f"{category}_years_{i}"
                                               )
                    
                yearly_mileage_EV = st.number_input("Yearly Mileage: ",
                                               min_value=0,
                                               key=f"{category}_mileage_{i}"
                                               )
            elif category == 'FCEV':
                st.subheader(category)
                veh_cat_FCEV = st.selectbox('FCEV Vehicle Category', 
                                           ['Sub Compacto',
                                            'Compacto',
                                            'Médio',
                                            'Grande',
                                            'Extra Grande'],
                                           key=f"{category}_cat_{i}"
                                 )
        
                veh_cost_FCEV = st.number_input("Vehicle Cost: ",
                                               min_value=0,
                                               key=f"{category}_cost_{i}"
                                               )
                    
                    
                fe_pad_FCEV = st.session_state.get(f"{category}_fepad_{i}", False)
                fuel_eco_FCEV = st.number_input("Fuel Eco: ",
                                               min_value=0.0,
                                               step=0.01,
                                               format="%.2f",
                                               disabled=fe_pad_FCEV,
                                               key=f"{category}_fe_{i}"
                                               )
                st.checkbox('Default Fuel Economy', key=f"{category}_fepad_{i}")
                    
                years_FCEV = st.number_input("Years: ",
                                               min_value=0,
                                               key=f"{category}_years_{i}"
                                               )
                    
                yearly_mileage_FCEV = st.number_input("Yearly Mileage: ",
                                               min_value=0,
                                               key=f"{category}_mileage_{i}"
                                               )