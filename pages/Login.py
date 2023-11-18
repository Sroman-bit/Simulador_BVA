#Librerias a Importar

import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from datetime import datetime
import stocknews as sn
from googletrans import Translator
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

translator = Translator()
import time
import random

# Función para el inicio de sesión
def login():
    st.header("Iniciar Sesión")
    correo = st.text_input("Correo Electrónico")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        # Verificar si los campos están completos (puedes agregar más validaciones aquí)
        if correo and usuario and contrasena:
            # Realizar la validación del usuario y contraseña
            resultado_validacion = validar_usuario(correo, usuario, contrasena)
            if resultado_validacion == "Inicio de sesión exitoso":
                st.success("¡Inicio de sesión exitoso! Ahora puedes acceder a todas las funciones del simulador.")
                # Resetear los campos.
                correo = ""
                usuario = ""
                contrasena = ""
            elif resultado_validacion == "Credenciales incorrectas":
                st.error("Credenciales incorrectas, verifica los datos y vuelve a escribirlos correctamente.")
            else:
                st.error("USUARIO NO ENCONTRADO: Este usuario no existe, primero debes registrarte para ello.")
        else:
            st.warning("Por favor, completa todos los campos.")

# Simulación de la validación del usuario
def validar_usuario(correo, usuario, contrasena):

    # Cerrar la conexión a Firebase si ya está inicializada
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())

    # Contenido directo del diccionario de credenciales
    cred_dict = {
        "type": "service_account",
        "project_id": "bolsadevaloresaneiap",
        "private_key_id": "5dc01e6a121dec2c4f7c86ea98df53559d9b1329",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrw//eHxkwAvl/\n/jBDuKp31kXbVthHXfjChLLZMxYiIYUGowpBLpYk3f1XnIfPBB9A0Tv56LBtREdu\n1qmxlPmjd7AEPM4ivfnq1XGgj/YRac8hhJOSpN5nKmq7Vy++jZ/NM2D/6L6ZVY5m\nsIUDGOr1Xu5Ehh7rcxwbhOWSuz3H6wGRjEe5rQq1vLEYRBZx7uMK/ASgTwMPrcjb\n66T41MscT1WIF+UIEVhEu/8GsU95HpED19a7/nOdYLicm59JuJ0vwWl4pc5Vh03l\n8h9CevNs5TI61OYc5oy/DjTIltj6KSc5rsyRQxqgVpwSZL+qgsNSSud8IN2ex+1O\nBO/Qr/SlAgMBAAECggEAEC/ITQZhOUUOfiFWKwucBO8MZj8o4pDYgHxA3ncR/uVp\nw9ZZgQsC2zaQSVFW+wtIZrNRE5v6BFIK6UcRdsqzO9RrofqY8m00wAydSKRIbBus\niVwVDBy9WLuGk2ED/tEZ3hyZZ4Rnccu+P68i2cffXIA1s/9vqoCOhYlgmRNMHyq+\n0ITr7DRdYvd5HSAm6Qn1uT1o78BI/A5uKJAjoPgyJ+CPv8lv658SidZKUGQMPZy3\nOf1yjvjSXpKd+5FaOtRBiELmOM5yqhSRF6K/1tm698vkjN98WFK/7AAiTeQMTh1l\nRkV5egtgdrLtNNAq5szZFMv4ZM9bdUqwmwEEITk8AQKBgQDYP7+IVK6ZoPYY7nXx\nNAJFwM3YUPWlOLT+z+4dCzc1LYvX+xZSJkVg0GQYtV1KODX6hNHS7BYMfm+fXA0O\n986XlNgP4pky+6bvbYGkklag9oyoZHGS1Ump7jnUIofzzcboXnMn5Y+1SE+9P5Qp\nL+TtQBglUfqkS0yN6lmnIMERvQKBgQDLVvNch3gTQ6mTVIete5Ekc9U2YDXarOHR\nDWMpCvhQ9J6yl+Zk6SJCsP4xpZ/EMJ7FTmpNk786YQ5sOp2Ty1hEF2lprmUAeBWg\nSTEqCpr2NmSgr8Eej/DFr6qqWNy7TSRtIRaDh6+k7Rvua3ZnGiEoPcLKwQpbntVT\nNyqoGNR5CQKBgGFA+kCz5PpOu58mz4A05bi9J1Zbwr4VrMDUfsAtJR0TaMsvrzAu\n6hDKZ9n85wHUGeKbDUqQxrHDwyumWHEc3ZqqZClwvXmCV+diFmYPMkqd11B8K9/f\ncIuuCe/vv7jUGNq0b5HH2kOrS8FO8LE9SvWwV6uhHNn6y2kftkZFos75AoGBAMc9\ns8f+lZGKwyYxtaAva9CkD07whtR2ge4th/Q3Y4kvqDCm1oIaTg+7DdfnydybJ3d9\nlnvdQYsaft9dr/mZTiuqJQgAccc74zTjguEG80A9m+w3Sqt/rxSFRF0WJXMB66di\nvIS0905LZwr/EU2FNOgRXET/Uf7ka3LWo12Ctu7BAoGAXHonxlrNK7S+PVQ7sJR7\nYjvpJkhleJ5J2SJgk6drI1+DawXem7b0m8Uwxn7OE5WDxvdfcJpGMmy71Cxvyez0\n2v9rNaZny6fs9/J0PE+ZpDE+hEZ71G8tc+GcZ4Pbz7zuP6vJPFxa4w2u/nHZmsq7hZD1fQDqFKDiC/yTlCSeCrI=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-ny0mg@bolsadevaloresaneiap.iam.gserviceaccount.com",
        "client_id": "118092414323030631083",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ny0mg%40bolsadevaloresaneiap.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    # Inicializa Firebase utilizando el diccionario
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    
    # Obtener una referencia a la base de datos
    db = firestore.client()

    # Referencia al documento del usuario
    doc_ref = db.collection("usuarios").document(usuario)

    # Verificar si el usuario existe en Firebase
    if doc_ref.get().exists:
        # Obtener los datos del usuario almacenados en Firebase
        datos_usuario = doc_ref.get().to_dict()

        # Verificar si las credenciales coinciden
        if ((datos_usuario["Correo Electrónico"] == correo) and 
            (datos_usuario["Contraseña"] == contrasena) and
            (datos_usuario["Usuario"] == usuario)):
            # Actualizar el campo 'usuario_logueado' en el documento 'variables'
            doc_ref_variables = db.collection("usuarios").document("variables")
            doc_ref_variables.update({"usuario_logueado": usuario})
            return "Inicio de sesión exitoso"  # Credenciales correctas
        else:
            return "Credenciales incorrectas"  # Contraseña incorrecta
    else:
        return "Usuario no encontrado"  # Usuario no existe en Firebase

#Codigo Principal

if __name__ == '__main__':

    st.title("Sistema de Ingreso de Usuario")
    login()
