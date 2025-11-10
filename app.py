import base64
import requests
import streamlit as st

def get_base64_image_from_url(url):
    response = requests.get(url)
    data = response.content
    return base64.b64encode(data).decode()

img_base64 = get_base64_image_from_url("https://res.cloudinary.com/dg4qs0bnq/image/upload/v1762348611/LEPTEN_ro2zl4.png")

st.set_page_config(layout='wide')

st.markdown(
    f"""
    <style>
        
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            height: 90px;  
            margin: -20px auto 30px auto;
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}

    </style>
    """,
    unsafe_allow_html=True
)

st.logo("https://res.cloudinary.com/dg4qs0bnq/image/upload/v1762348609/CNPq_vcogro.png",size="small",icon_image="https://res.cloudinary.com/dg4qs0bnq/image/upload/v1762348610/logo_iz23xu.png")

pages={
    "Docs": [st.Page("Introduction.py", title = "Introduction"),
             st.Page("WebInterface.py", title = "Using Web Interface"),
             st.Page("ModelOverview.py", title = "Model Overview")],
    "Modes": [
        st.Page("ICEV_page.py", title = "ICEV - TCO and GHG"),
        st.Page("BEV_page.py", title = "BEV - TCO and GHG"),
        st.Page("FCEV_page.py", title = "FCEV - TCO and GHG"),
        st.Page("Comparison.py", title = "Comparison"),
    ]  
}
pg = st.navigation(pages)

pg.run()