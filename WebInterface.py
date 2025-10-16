import streamlit as st

st.title("Web Interface Tutorial")

st.markdown('''This page provides tutorials and detailed explanations on how to use the TCO and GHG Analysis tool.  
            It describes the different components of the website (sidebar menu, individual category pages, comparison overview, and displayed results) in the following sequence:  
                Sidebar components → ICEV, BEV, and FCEV inputs / Comparison inputs → General outputs.''')

tabs=st.tabs(['Side-bar components','ICEV, BEV and FCEV inputs','Comparison inputs','Graphs and output data'])

with tabs[0]:
    st.markdown('''The user’s first interaction with the interface is through the sidebar.  
                This section provides the main navigation elements, listed as follows:  
  
:blue-background[Modes ⌵]  
:blue-background[ㅤㅤ-> ICEV – TCO and GHG]  
:blue-background[ㅤㅤ-> BEV – TCO and GHG]  
:blue-background[ㅤㅤ-> FCEV – TCO and GHG]  
:blue-background[ㅤㅤ-> Comparison]                     
  
The first three elements allow the user to analyze each vehicle type and fuel category individually, while the last one provides a comparison across all categories.''')

with tabs[1]:
    st.markdown('''Selecting one of these trhee elements:  
                :blue-background[ㅤㅤ-> ICEV – TCO and GHG]  
                :blue-background[ㅤㅤ-> BEV – TCO and GHG]  
                :blue-background[ㅤㅤ-> FCEV – TCO and GHG] ''')
    st.markdown('The page showed must be like de following image, with the title of the fuel category near the menu and the following form.')
    st.image('Side-bar2.png')
    st.markdown('''All form elements include a tooltip icon ('ⓘ') located on the right side of the input container title. This tooltip provides a brief description of the corresponding input field.  
                   To enable the “Apply” button, all required fields must be completed. Fields without a warning message are pre-filled with default values, which can be modified if desired.  
                ''')
    st.image('Side-bar3.png') 
    st.markdown('''The fields with a toggle for default values display the equivalent value of the vehicle stored in our database.  
                When a user enters a value and then activates the toggle to use the default value associated with that field, the field becomes unavailable for editing.  
                The displayed value remains visible, but the calculation will consider the default value instead.
                ''')
    st.image('Side-bar4.png')
    
    
#Alterar as imgaens, colocar sempre unidade de medida, fazer as imagens para cada campo das 3 categorias.