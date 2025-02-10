import streamlit as st
import os
import json

DATA_DIR = "./data/emails/"  # Ruta de los correos JSON

def show_inbox():
    st.title("📨 Bandeja de Entrada")
    st.subheader("📩 Correos recibidos")

    # Listar archivos de correos en la carpeta
    emails = os.listdir(DATA_DIR)
    if not emails:
        st.info("No hay correos en la bandeja.")
        return

    # Mostrar lista de correos
    for email_file in emails:
        with open(os.path.join(DATA_DIR, email_file), 'r') as f:
            email_data = json.load(f)
        st.write(f"**Título:** {email_data['title']}")
        if st.button(f"Abrir {email_data['title']}"):
            st.session_state["selected_email"] = email_file
            st.session_state["view"] = "email_detail"
            st.rerun()

    # Agregar un nuevo correo
    if st.button("Agregar nuevo correo"):
        st.session_state["view"] = "add_email"
        st.rerun()
