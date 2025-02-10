import streamlit as st
from views.inbox import show_inbox
from views.email_detail import show_email_detail
from views.add_email import show_add_email

# Inicializar el estado de la vista
if "view" not in st.session_state:
    st.session_state["view"] = "inbox"

# Control del flujo de vistas
if st.session_state["view"] == "inbox":
    show_inbox()
elif st.session_state["view"] == "email_detail":
    show_email_detail()
elif st.session_state["view"] == "add_email":
    show_add_email()
