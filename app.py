# Home 

import streamlit as st

home_page = st.Page("Home.py",title = "TCO and GHG test")
page_1 = st.Page("ICEV_page_test.py", title = "ICEV - TCO and GHG")
page_2 = st.Page("BEV_page_test.py", title = "BEV - TCO and GHG")
page_3 = st.Page("FCEV_page_test.py", title = "FCEV - TCO and GHG")
page_4 = st.Page("Comparison.py", title = "Comparison")

pg = st.navigation([home_page,page_1,page_2,page_3,page_4])

pg.run()

# iniciação: prompt => streamlit run app.py