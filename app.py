# Home 

import streamlit as st

pages={
    "Home Page": [st.Page("Home.py", title = "Home Page"),],
    "Modes": [
        st.Page("ICEV_page_test.py", title = "ICEV - TCO and GHG"),
        st.Page("BEV_page_test.py", title = "BEV - TCO and GHG"),
        st.Page("FCEV_page_test.py", title = "FCEV - TCO and GHG"),
        st.Page("Comparison.py", title = "Comparison"),
    ]  
}
pg = st.navigation([home_page,page_1,page_2,page_3,page_4])

pg.run()


# iniciação: prompt => streamlit run app.py
