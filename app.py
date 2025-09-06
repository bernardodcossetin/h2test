# Home 

import streamlit as st
st.markdown(
    """
    <style>
        [data-testid="stSidebar"]::before {
            content: "TCO and GHG Analysis";
            display: block;
            font-size: 30px;
            font-weight: bold;
            color: white;
            padding: 25px 20px 0px 20px;
            margin-bottom: -60px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
pages={
    "Home Page": [st.Page("Home.py", title = "Home Page"),],
    "Modes": [
        st.Page("ICEV_page_test.py", title = "ICEV - TCO and GHG"),
        st.Page("BEV_page_test.py", title = "BEV - TCO and GHG"),
        st.Page("FCEV_page_test.py", title = "FCEV - TCO and GHG"),
        st.Page("Comparison.py", title = "Comparison"),
    ]  
}
pg = st.navigation(pages)

pg.run()


# iniciação: prompt => streamlit run app.py


