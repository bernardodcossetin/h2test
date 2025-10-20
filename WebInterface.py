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
    st.image('Side-bar2.png', width=525)
    st.markdown('''All form elements include a tooltip icon ('ⓘ') located on the right side of the input container title. This tooltip provides a brief description of the corresponding input field.  
                   To enable the “Apply” button, all required fields must be completed. Fields without a warning message are pre-filled with default values, which can be modified if desired.  
                ''')
    st.image('Side-bar3.png', width=600) 
    st.markdown('''The fields with a toggle for default values display the equivalent value of the vehicle stored in our database.  
                When a user enters a value and then activates the toggle to use the default value associated with that field, the field becomes unavailable for editing.  
                The displayed value remains visible, but the calculation will consider the default value instead.
                ''')
    st.image('Side-bar4.png', width=500)
    st.markdown('''**Type**:  
                This field allows you to select the type of fuel used by the vehicle for the analysis.  
                For ICEV (Internal Combustion Engine Vehicle), the options are **E27** and **E100**, corresponding to gasoline and ethanol, respectively.  
                For BEV (Battery Electric Vehicle), the available options are **BEV** and **BEV with PV** (photovoltaic system).  
                For FCEV (Fuel Cell Electric Vehicle), the options are **FCEV** and **FCEV with PV**.  
                ''')
    st.image('Side-bar5.png', width=500)
    st.markdown('''**Category**:  
                In this field, you can select the vehicle category or a specific model to be analyzed.  
                The generic categories (Compact, Sub-compact, Large, etc.) contain average information about the vehicles in our database that belong to each category.  
                Selecting a category or a specific vehicle also allows you to use default parameter values from our database for the calculations.  
                ''')
    st.image('Side-bar6.png', width=500)
    st.markdown('''**Vehicle Cost**:  
                This field represents the vehicle’s purchase cost and includes a currency selector.  
                It is important to ensure that the entered cost matches the selected currency to avoid inconsistencies in the results.  
                ''')
    st.image('Side-bar7.png', width=300)
    st.markdown('''**Fuel Eco**:  
                In the fuel economy field, the measurement unit displayed next to the field title depends on the selected vehicle type:  
                km/L for ICEV, kWh/km for BEV, and kg/km for FCEV.  
                If desired, users can choose to apply the default fuel economy value provided by the system.  
                ''')
    st.image('Side-bar8.png', width=800)
    st.markdown('''**Years**:  
                This field defines the **vehicle’s lifetime**, which can be adjusted using the slider from 1 to 20 years.  
                ''')
    st.image('Side-bar9.png', width=300)
    st.markdown('''**Yearly Mileage**:  
                This field indicates the total distance driven by the vehicle per year, measured in **kilometers**.  
                ''')
    st.image('Side-bar10.png', width=300)
    st.markdown('''**UF**:
                This field allows you to select the **Brazilian federative unit** (state) to include regional variables such as fuel price and IPVA tax rate in the analysis. 
                ''')
    st.image('Side-bar11.png', width=300)
    st.markdown('''**Battery Capacity**:  
                This field represents the battery capacity of the **electric vehicle**.  
                A default value for this parameter is also available in our database.   
                ''')
    st.image('Side-bar12.png', width=300)

with tabs[2]:
    st.markdown('''When the comparison page is opened, a message appears on the screen indicating the usage condition of the tool: it can only be used  
                when at least two vehicle types are selected from the options available in the sidebar.
                ''')
    st.image('Comparison1.png')
    st.markdown(''' In addition, since the purpose of this page is to compare multiple vehicles, the selected currency applies to all values across all vehicles.  
                In the sidebar, the selected vehicle categories must be chosen, as well as the currency to be used in the analysis.
                ''')
    st.image('Comparison2.png',width=500)
    st.markdown('''The comparison function offers multiple possibilities to compare different vehicle types with different fuel options.  
                The usage and data entry process are essentially the same as in the individual analysis pages.  
                The main difference lies in how the forms are arranged on the screen. 
                ''')
    st.image('Comparison3.png')
    st.markdown('''Here it is possible to compare various parameters, adjusting the input data for each case as desired. In other words,  
                it is not necessary for all selected vehicles to have the same lifetime, yearly mileage, or other parameters.  
                Once all required fields are completed, the “Apply” button becomes available, allowing the results to be displayed.
                ''')
with tabs[3]:
    st.markdown('''**ICEV, BEV, and FCEV – Charts and Output Data**  
                After the Apply button is clicked, the charts and results appear on the right side of the screen, next to the sidebar.  
                In the example shown, the BEV is used, but the same behavior applies to the other vehicle types.  
                ''')
    st.image('Results1.png', width=600)
    st.markdown('''The container that displays the charts is organized as a tab component, which includes both the emissions chart and the accumulated TCO chart.   
                Each chart is properly titled, and it is possible to switch between them by clicking the corresponding tab at the top of the container.
                ''')
    st.image('Results2.png', width=700)        
    st.markdown('''The emissions chart starts at year 0, which represents only the production emissions, and extends up to the selected analysis year.
                The curve grows over time until the last year, where it either decreases or flattens due to the applied recycling process (as detailed in Docs – Model Overview).  
                For BEV and FCEV, a noticeable jump appears on the curve at a certain point, representing the replacement of the battery or fuel cell.
                ''')
    st.image('Results3.png', width=600)
    st.markdown('''The TCO chart, in turn, starts its index at year 1 and extends to the final year, showing a flattening and decline toward the end.  
                Similarly, for BEV and FCEV, a jump occurs at a given year (depending on vehicle lifetime, annual mileage, and driving range), representing the replacement of the battery or fuel cell.  
                ''')
    st.image('Results4.png', width=600)
    st.markdown('''Next to the charts, the numerical results for GHG, GHG/km, TCO, and LCOD are displayed. Each result includes a tooltip providing a brief explanation of its meaning. 
                ''')
    st.image('Results5.png', width=300)
    st.markdown('''The numerical values used in the calculations can be checked in the collapsible table located just below the results section.
                ''')
    st.image('Results6.png', width=600)
    st.markdown('''**Comparison – Charts and Output Data**  
                In the comparison mode, the results are displayed immediately below the input form, followed by the charts. Both follow the same logic as the individual vehicle results.  
                The main difference lies in how the data and charts are presented.  
                Each vehicle category is represented as a line with a distinct color in the chart, with a corresponding label in the legend next to it.  
                To filter the results, simply click on the legend to toggle the visibility of the respective line in both charts.
                ''')


























