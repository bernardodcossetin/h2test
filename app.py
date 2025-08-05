# Home 

import streamlit as st

home_page = st.Page("Home.py",title = "TCO and GHG test")
page_1 = st.Page("ICEV_page_test.py", title = "ICEV - TCO and GHG")
#page_2 = st.Page("EV_page_test.py", title = "EV - TCO and GHG")
#page_3 = st.Page("HEV_page_test.py", title = "HEV - TCO and GHG")
page_4 = st.Page("Comparison.py", title = "Comparison")

pg = st.navigation([home_page,page_1,page_4])

pg.run()

# iniciação: prompt => streamlit run app.py