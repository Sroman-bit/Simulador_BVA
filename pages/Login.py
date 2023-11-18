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

    # Inicializar Firebase
    cred = credentials.Certificate(r'C:\Users\avill\OneDrive\Escritorio\REPOSITORIO_BDVANEIAP\Simulador_BVA\bolsadevaloresaneiap-5dc01e6a121d.json')
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
