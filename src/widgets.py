import streamlit as st
import os

def list_file_expanders(
    folder_path: str,
    specific_extension: str = None,
    opened_callback: callable = None
):
    try:
        # Find files to display
        paths = []
        for _path in os.scandir(folder_path):
            paths.append(_path)
        paths.sort(key=lambda x: x.name, reverse=True)
        for path in paths:
            if path.is_file() is False:
                continue
            if specific_extension != None:
                if path.name.endswith(specific_extension) == False:
                    continue
            with st.expander(path.name):
                if opened_callback != None:
                    opened_callback(path)
    except Exception as e:
        st.error(e)