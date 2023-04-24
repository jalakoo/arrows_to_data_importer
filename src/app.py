import streamlit as st
import streamlit.components.v1 as components
from widgets import list_file_expanders
from file_utils import save_file, load_json, delete_file
from io import StringIO
from models.data_import import convert_from_arrows
import json
from pathlib import Path

st.set_page_config(layout="wide")

st.title("Arrows To Data-Importer")

t1, t2, t3 = st.tabs(["Arrows", "Conversions", "Data-Importer"])
with t1:
    # Display arrows.app interface
    components.iframe("https://arrows.app", height=1000, scrolling=False)
with t2:
    # Option for uploading / selecting an arrows.app json file that
    # has been converted to a data-importer json file
    uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
    if uploaded_file is not None:
        filepath = f"./uploads/{uploaded_file.name}"
        try:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            file_to_save = stringio.read()
            save_file(
                filepath= filepath,
                data=file_to_save)
        except:
            st.error(f"Error saving file")

    # Creates UI within selected Expanded list item
    def opened_callback(path):
        # Create converted file
        selected_file = load_json(path)
        data_import_dict = convert_from_arrows(selected_file)
        data_import_json = json.dumps(data_import_dict)
        stem_name = Path(path).stem
        
        # Button to download converted file
        st.download_button(
            "Download Data-Importer compatible file", 
            key=f"download_{path.name}",
            data=data_import_json,
            mime="text/json",
            file_name=f"{stem_name}_data_importer_model.json")
        
        # Display file contents
        if path.name.endswith('.zip') == False:
            with open(path, 'r') as f:
                st.text(f.read())

        # Delete file
        if st.button('Delete file', key=f'delete_{path}'):
            delete_file(path)
            st.info(f'{path} deleted. Please refresh page.')

    list_file_expanders(
        folder_path="./uploads",
        specific_extension=".json",
        opened_callback=opened_callback
    )
with t3:
    # Display Data Importer Interface
    components.iframe("https://data-importer.graphapp.io", height=1000, scrolling=False)
