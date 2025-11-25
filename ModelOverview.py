import streamlit as st

st.title("Model Overview")

st.markdown(''' This section provides a general explanation of the computational model used, aiming to clarify the notations, data sources, input fields, where the data comes from, and how the model operates.  
            It is important to note that this explanation is based on a generic version of the model for illustrative purposes. For deeper understanding and complete technical details, we invite users to visit our repository.  
            Contrary to how information is displayed on the website, the following diagram illustrates how the input data is requested from the user, showing which parameters are needed to operate the tool. 
            ''')

st.markdown('''**The abbreviations stand for:** 
                  
            • al = IPVA tax rate   
            • uf = federative unit (state) of Brazil  
            • fp = fuel price   
            • tf = electricity tariff   
            • dr = average annual vehicle depreciation rate   
            • r = discount rate    
            • ins = percentage of the vehicle’s assessed value corresponding to the insurance cost   
            • GHG = life-cycle cumulative emissions  
            • GHG_km = emissions normalized per kilometer driven over the years  
            • TCO = total cost of ownership  
            • LCOD = levelized cost of driving
            ''')

st.markdown('''**The code requires the following data:**
              
            • type_fuel = fuel type used     
            • fuel_eco = fuel economy     
            • veh_cost = initial acquisition cost     
            • years = useful lifetime considered in the analysis     
            • yearly_mileage = annual mileage    
            • exchange = currency used in the analysis (same as the acquisition value)   
            • veh_bat_cap = battery capacity   
            ''')
            
st.markdown(''' The variables al, fp, tf, dr, r, ins, are retrieved directly from the database or from the codes, and the fuel_eco and veh_bat_cap may also be obtained from the database at the user’s discretion.  
These inputs are returned to the computational function, generating accumulated yearly values for both GHG emissions and TCO. These results are stored in a list, which serves as the basis for the charts rendered on the results page of the platform.    
We again emphasize the importance of consulting the models available in our repository for clarification of any questions, as each category follows a specific set of equations and assumptions, especially regarding emissions calculations.''')

col1,col2=st.columns(2)

with col1:
    st.markdown('**TCO Example:**')
    code = '''def TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp, exchange, dolar):
        r = 0.1          
        dr = 0.06412427874061244      
        ins = 0.06       
        C_vehicle = veh_cost
        C_maintenance = 800/dolar
        soma_q=0
        if exchange == 'BRL(R$)':
            C_maintenance = C_maintenance*dolar
        consumption = yearly_mileage / fuel_eco
        C_fuel = fp * consumption
        TCO_accumulated = []
        TCO = C_vehicle  
        for y in range(1, years + 1):
            V_venal = veh_cost * (1 - dr) ** y
            C_insurance = V_venal * ins
            C_taxes = V_venal * al
            fator_desc = 1 / (1 + r) ** y
            custo_anual = (C_maintenance + C_fuel + C_insurance + C_taxes) * fator_desc
            soma_q+= yearly_mileage* fator_desc
            TCO += custo_anual
            if y == years:
                C_resale = -veh_cost * (1 - dr) ** years
                TCO += C_resale / (1 + r) ** years
            TCO_accumulated.append(TCO)
        LCOD=TCO/soma_q

        return [np.array(TCO),np.array(LCOD),TCO_accumulated]'''
    st.code(code, language="python")
with col2:
    st.markdown('**GHG Example:**')
    code = '''def GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e):
        GHG_vehicle = 4.56e3 * W
        GHG_recycling = -2.93e3 * W
        consumption = yearly_mileage / fuel_eco
        GHG_fuel_year = consumption * ghg_fuel_e
        ghg_accumulated = []
        for y in range(0, years + 1):
            ghg_total = (GHG_vehicle + GHG_fuel_year * y)/ 10**6
            if y == years:
                ghg_total = (GHG_vehicle + GHG_recycling + GHG_fuel_year * y)/ 10**6
            ghg_accumulated.append(ghg_total)
        GHG=(GHG_vehicle+GHG_recycling+GHG_fuel_year*years)/10**6
        GHG_km=GHG* 10**6/(years*yearly_mileage)
    
        return [np.array(GHG),np.array(GHG_km),ghg_accumulated]'''
    st.code(code, language="python")









