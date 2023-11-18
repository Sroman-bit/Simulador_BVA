#Librerias a Importar

import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from datetime import datetime
import stocknews as sn
from googletrans import Translator
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from firebase_admin import credentials, initialize_app


translator = Translator()
import time
import random
import re  # Importar el módulo de expresiones regulares

#Funciones

# Función para el registro
def registro():
    st.header("Registrarse")
    correo = st.text_input("Correo Electrónico")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")

    registro_exitoso = False  # Variable para rastrear si el registro fue exitoso
    
    if st.button("Registrarse"):
        # Verificar si los campos están completos (puedes agregar más validaciones aquí)
        if correo and usuario and contrasena and confirmar_contrasena:
            # Verificar que las contraseñas coincidan
            if contrasena == confirmar_contrasena:
                # Realizar la lógica de registro
                registro_exitoso = registrar_usuario(correo, usuario, contrasena)
                # Llevar al usuario a la parte del simulador
                if registro_exitoso:
                    st.success("USUARIO REGISTRADO EXITOSAMENTE")
                    st.write("¡Bienvenido al simulador!")
            else:
                st.error("LAS CONSTRASEÑAS NO COINCIDEN.")
        else:
            st.warning("DEBES DILIGENCIAR TODOS LOS CAMPOS.")

# Simulación del registro de usuario
def registrar_usuario(correo, usuario, contrasena):

    # Cerrar la conexión a Firebase si ya está inicializada
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())
    
    # Configuración de credenciales directamente en el código
    cred = {
        "type": "service_account",
        "project_id": "bolsadevaloresaneiap",
        "private_key_id": "5dc01e6a121dec2c4f7c86ea98df53559d9b1329",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrw//eHxkwAvl/\n/jBDuKp31kXbVthHXfjChLLZMxYiIYUGowpBLpYk3f1XnIfPBB9A0Tv56LBtREdu\n1qmxlPmjd7AEPM4ivfnq1XGgj/YRac8hhJOSpN5nKmq7Vy++jZ/NM2D/6L6ZVY5m\nsIUDGOr1Xu5Ehh7rcxwbhOWSuz3H6wGRjEe5rQq1vLEYRBZx7uMK/ASgTwMPrcjb\n66T41MscT1WIF+UIEVhEu/8GsU95HpED19a7/nOdYLicm59JuJ0vwWl4pc5Vh03l\n8h9CevNs5TI61OYc5oy/DjTIltj6KSc5rsyRQxqgVpwSZL+qgsNSSud8IN2ex+1O\nBO/Qr/SlAgMBAAECggEAEC/ITQZhOUUOfiFWKwucBO8MZj8o4pDYgHxA3ncR/uVp\nw9ZZgQsC2zaQSVFW+wtIZrNRE5v6BFIK6UcRdsqzO9RrofqY8m00wAydSKRIbBus\niVwVDBy9WLuGk2ED/tEZ3hyZZ4Rnccu+P68i2cffXIA1s/9vqoCOhYlgmRNMHyq+\n0ITr7DRdYvd5HSAm6Qn1uT1o78BI/A5uKJAjoPgyJ+CPv8lv658SidZKUGQMPZy3\nOf1yjvjSXpKd+5FaOtRBiELmOM5yqhSRF6K/1tm698vkjN98WFK/7AAiTeQMTh1l\nRkV5egtgdrLtNNAq5szZFMv4ZM9bdUqwmwEEITk8AQKBgQDYP7+IVK6ZoPYY7nXx\nNAJFwM3YUPWlOLT+z+4dCzc1LYvX+xZSJkVg0GQYtV1KODX6hNHS7BYMfm+fXA0O\n986XlNgP4pky+6bvbYGkklag9oyoZHGS1Ump7jnUIofzzcboXnMn5Y+1SE+9P5Qp\nL+TtQBglUfqkS0yN6lmnIMERvQKBgQDLVvNch3gTQ6mTVIete5Ekc9U2YDXarOHR\nDWMpCvhQ9J6yl+Zk6SJCsP4xpZ/EMJ7FTmpNk786YQ5sOp2Ty1hEF2lprmUAeBWg\nSTEqCpr2NmSgr8Eej/DFr6qqWNy7TSRtIRaDh6+k7Rvua3ZnGiEoPcLKwQpbntVT\nNyqoGNR5CQKBgGFA+kCz5PpOu58mz4A05bi9J1Zbwr4VrMDUfsAtJR0TaMsvrzAu\n6hDKZ9n85wHUGeKbDUqQxrHDwyumWHEc3ZqqZClwvXmCV+diFmYPMkqd11B8K9/f\ncIuuCe/vv7jUGNq0b5HH2kOrS8FO8LE9SvWwV6uhHNn6y2kftkZFos75AoGBAMc9\ns8f+lZGKwyYxtaAva9CkD07whtR2ge4th/Q3Y4kvqDCm1oIaTg+7DdfnydybJ3d9\nlnvdQYsaft9dr/mZTiuqJQgAccc74zTjguEG80A9m+w3Sqt/rxSFRF0WJXMB66di\nvIS0905LZwr/EU2FNOgRXET/Uf7ka3LWo12Ctu7BAoGAXHonxlrNK7S+PVQ7sJR7\nYjvpJkhleJ5J2SJgk6drI1+DawXem7b0m8Uwxn7OE5WDxvdfcJpGMmy71Cxvyez0\n2v9rNaZny6fs9/J0PE+ZpDE+hEZ71G8tc+GcZ4Pbz7zuP6vJPFxa4w2u/nHZmsq7\nhZD1fQDqFKDiC/yTlCSeCrI=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-ny0mg@bolsadevaloresaneiap.iam.gserviceaccount.com",
        "client_id": "118092414323030631083",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ny0mg%40bolsadevaloresaneiap.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    # Inicializa Firebase utilizando el diccionario
    firebase_admin.initialize_app(cred)
    
    # Obtener una referencia a la base de datos
    db = firestore.client()

    # Verificar si el usuario ya existe
    doc_ref_usuario = db.collection("usuarios").document(usuario)
    if doc_ref_usuario.get().exists:
        st.warning("USUARIO EXISTENTE: El usuario ya existe. Por favor, elige otro nombre de usuario.")
        return False  # Indicar que el registro no fue exitoso

    # Verificar si el correo ya está en uso
    doc_ref_correo = db.collection("usuarios").where("`Correo Electrónico`", "==", correo).limit(1)
    if len(list(doc_ref_correo.stream())) > 0:
        st.warning("CORREO EN USO: El correo electrónico ya está asociado a otro usuario. Por favor, utiliza otro correo.")
        return False  # Indicar que el registro no fue exitoso

    # Verificar que el correo tenga el dominio correcto
    if not correo.endswith("@aneiap.co"):
        st.warning("CORREO INVÁLIDO: El correo electrónico debe ser tu correo ANEIAP.")
        return False  # Indicar que el registro no fue exitoso

    # Verificar la validez de la contraseña
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', contrasena):
        st.warning("CONTRASEÑA INVÁLIDA: La contraseña debe tener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula y un número.")
        return False  # Indicar que el registro no fue exitoso    

    # Si el usuario y el correo son únicos, proceder con el registro
    datos_usuario = {
        "Usuario": usuario,
        "Correo Electrónico": correo,
        "Contraseña": contrasena,
        "Saldo": 10000,  # Saldo inicial
        "Portafolio": [],  # Portafolio vacío
        "HistorialTransacciones": []  # Historial de transacciones vacío
    }
    
    # Insertar los datos en Firebase
    doc_ref_usuario.set(datos_usuario)

    # Restablecer los campos de entrada
    correo = ""
    usuario = ""
    contrasena = ""
    confirmar_contrasena = ""

    return True  # Indicar que el registro fue exitoso


#Codigo Principal

# Código Principal
if __name__ == '__main__':
    st.title("Sistema de Registro de Usuario")
    registro()
