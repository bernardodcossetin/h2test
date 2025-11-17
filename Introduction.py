import streamlit as st

st.title("Introduction")

st.subheader("About the project")

st.markdown(''' The TCO and GHG Simulator is a free and open-source computational model developed by LEPTEN (Laboratory of Process Engineering and Energy Conversion Technologies), sponsored by CNPq.  
            Its objective is to perform and present quantitative analyses of the Brazilian automotive market, focusing on greenhouse gas emissions throughout a vehicle’s lifetime, as well as the economic impact for users.    
            The project was divided into some stages (and the following references):
            ''')
st.markdown("""
            • A regional approach to estimating economic and environmental impacts when running a vehicle with ethanol in Brazil  
            • Cost and placement of solar green hydrogen production stations to supply FCEV fleet growth in Brazilian states  
            • Estimating total cost related to using EVs or ICEVs with different energy and fuel sources in each Brazilian state  
            • User-friendly computational model for TCO and GHG analysis of combustion and electric vehicles
            """)
col1,col2 = st.columns([3,1])
with col1:
    st.markdown('PEREIRA FELICIDADE, LEONARDO; RUGERI BORGES BONINI, VINICIUS ; SILVA JUNIOR, LUIZ H. ;  ; DA SILVA, ALEXANDRE KUPKA . COST AND PLACEMENT OF SOLAR GREEN HYDROGEN PRODUCTION STATIONS TO SUPPLY FCEV FLEET GROWTH IN BRAZILIAN STATES. In: 20th Brazilian Congress of Thermal Sciences and Engineering, 2024. Proceedings of the 20th Brazilian Congress of Thermal Sciences and Engineering.')

with col2:
    st.download_button(label='Click here to see the reference',data='')
st.subheader('Website Overview')          
st.markdown('''So this platform was developed to present the results obtained in the research. The website features four main sections: ICEV, BEV, and FCEV  
            TCO and GHG Analysis, and the Comparison page. 
            ''')
st.markdown('''The first three sections provide detailed individual results, which can also be compared on the comparison page.  
            The model was built in Python based on previously developed models from associated projects. It includes a wide range of input data (vehicle data and Brazilian regional economic data),  
            which will be updated over time. Users can also view and download the original base models as well as the models specific to this project from our repository.
            ''')





