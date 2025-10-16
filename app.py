import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_image("LEPTEN.png")

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

st.logo("CNPq.png",size="small",icon_image="logo.png")

pages={
    "Docs": [st.Page("Introduction.py", title = "Introduction"),
             st.Page("WebInterface.py", title = "Using Web Interface"),
             st.Page("ModelOverview.py", title = "Model Overview")],
    "Modes": [
        st.Page("ICEV_page_test.py", title = "ICEV - TCO and GHG"),
        st.Page("BEV_page_test.py", title = "BEV - TCO and GHG"),
        st.Page("FCEV_page_test.py", title = "FCEV - TCO and GHG"),
        st.Page("Comparison.py", title = "Comparison"),
    ]  
}
pg = st.navigation(pages)

pg.run()