import streamlit as st
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib
import re

DATA_DIR = "./data/emails/"
MODEL_DIR = "./data/"

# Cargar modelos de texto
email_classifier = joblib.load(os.path.join(MODEL_DIR, "email_classifier.pkl"))
tfidf_vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))

# Cargar modelo de URL (mantener en formato .h5)
url_nn_model = load_model(os.path.join(MODEL_DIR, "url_nn_model.h5"))

# Cargar scaler desde el archivo .pkl
scaler = joblib.load(os.path.join(MODEL_DIR, "url_scaler.pkl"))

# Función para verificar si una URL contiene una IP
def contains_ip(url):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return 1 if re.search(ip_pattern, url) else 0

# Función para verificar si hay muchos números seguidos de letras/caracteres especiales
def suspicious_patterns(url):
    pattern = r'\d+[a-zA-Z!@#$%^&*()_+=]'
    return 1 if re.search(pattern, url) else 0

# Función para preprocesar URLs
def preprocess_url(url):
    try:
        length = len(url)
        num_dots = url.count('.')
        num_slashes = url.count('/')
        num_hyphens = url.count('-')
        has_https = 1 if 'https' in url else 0
        ip_present = contains_ip(url)
        suspicious_pattern = suspicious_patterns(url)
        return [length, num_dots, num_slashes, num_hyphens, has_https, ip_present, suspicious_pattern]
    except Exception:
        return [0, 0, 0, 0, 0, 0, 0]

# Mostrar detalles del correo
def show_email_detail():
    if "selected_email" not in st.session_state:
        st.warning("Por favor, selecciona un correo desde la bandeja.")
        st.session_state["view"] = "inbox"
        st.rerun()

    email_file = st.session_state["selected_email"]

    # Cargar detalles del correo
    with open(os.path.join(DATA_DIR, email_file), 'r') as f:
        email_data = json.load(f)

    st.title(email_data["title"])
    st.write("**Texto del correo:**")
    st.write(email_data["text"])
    st.write("**URL asociada:**")
    st.write(email_data["url"])

    if st.button("Analizar"):
        # Análisis del texto del correo
        text_features = tfidf_vectorizer.transform([email_data["text"]])
        email_prediction = email_classifier.predict(text_features)[0]
        email_result = "⚠️ El correo analizado contiene características sospechosas y es clasificado como malicioso. Recomendamos no interactuar con él" if email_prediction == 1 else "✔️ El correo analizado parece seguro y no contiene elementos sospechosos. Puedes proceder con cautela."

        st.subheader("Resultados del Análisis")
        st.write(f"**Correo:** {email_result}")

        # Mostrar palabras clave más relevantes del correo
        st.subheader("Palabras clave relevantes en el análisis")
        feature_names = tfidf_vectorizer.get_feature_names_out()
        top_features = np.argsort(text_features.toarray()[0])[-10:]
        top_words = [feature_names[i] for i in top_features]
        top_importances = [text_features.toarray()[0][i] for i in top_features]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(top_words, top_importances, color='skyblue')
        ax.set_title("Palabras clave más relevantes")
        ax.set_xlabel("Peso TF-IDF")
        st.pyplot(fig)

        # Análisis de la URL
        url_features = preprocess_url(email_data["url"])
        url_scaled = scaler.transform([url_features])
        url_prediction = url_nn_model.predict(url_scaled)[0][0]
        url_result = "⚠️ La URL detectada contiene elementos que sugieren un comportamiento malicioso. Evita abrirla o compartirla." if url_prediction > 0.5 else "✔️ La URL analizada parece segura y no muestra indicios de comportamiento sospechoso. Puedes utilizarla con cautela."

        # Mostrar contribución de características de la URL
        st.subheader("Contribución de características de la URL")
        feature_labels = ['length', 'num_dots', 'num_slashes', 'num_hyphens', 'has_https', 'ip_present', 'suspicious_pattern']
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(feature_labels, url_scaled[0], color='salmon')
        ax.set_title("Contribución de las características de la URL")
        ax.set_xlabel("Valor escalado")
        st.pyplot(fig)

        st.write(f"**URL:** {url_result}")
        # Botón "Atrás" para regresar a la bandeja de entrada
    if st.button("Atrás"):
        st.session_state["view"] = "inbox"  # Cambiar la vista a la bandeja de entrada
        st.rerun()
