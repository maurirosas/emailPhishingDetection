import streamlit as st
import os
import json

DATA_DIR = "./data/emails/"

def show_add_email():
    st.title("Agregar Nuevo Correo")

    title = st.text_input("Título del correo")
    text = st.text_area("Texto del correo")
    url = st.text_input("URL asociada")

    if st.button("Añadir"):
        if not title or not text or not url:
            st.error("Todos los campos son obligatorios.")
        else:
            email_data = {
                "title": title,
                "text": text,
                "url": url
            }
            file_name = f"{title.replace(' ', '_')}.json"
            with open(os.path.join(DATA_DIR, file_name), 'w') as f:
                json.dump(email_data, f)
            st.success(f"Correo '{title}' agregado exitosamente.")
            st.session_state["view"] = "inbox"
            st.rerun()
