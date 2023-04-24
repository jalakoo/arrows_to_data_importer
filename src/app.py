import streamlit as st
import streamlit.components.v1 as components
from io import StringIO
from models.data_import import convert_from_arrows
import json

st.set_page_config(layout="wide")

st.title("Arrows To Data-Importer")

t1, t2, t3 = st.tabs(["Arrows", "Conversions", "Data-Importer"])
with t1:
    # Display arrows.app interface
    components.iframe("https://arrows.app", height=1000, scrolling=False)
with t2:

    selected_file = None
    uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        selected_file = stringio.read()

        # Create converted file
        loaded_file = json.loads(selected_file)
        data_import_dict = convert_from_arrows(loaded_file)
        data_import_json = json.dumps(data_import_dict)
        stem_name = uploaded_file.name.split('.')[0]

        # Button to download converted file
        st.download_button(
            "Download Data-Importer compatible file", 
            key=f"download_{uploaded_file.name}",
            data=data_import_json,
            mime="text/json",
            file_name=f"{stem_name}_model.json")
        
with t3:
    # Display Data Importer Interface
    components.iframe("https://data-importer.graphapp.io", height=1000, scrolling=False)
