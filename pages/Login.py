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

# Variable global para almacenar el nombre de usuario autenticado
usuario_autenticado = None

# Función para el inicio de sesión
def login():
    global usuario_autenticado  # Declarar la variable como global
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
                # Almacena el nombre de usuario en la variable global
                usuario_autenticado = usuario
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
    
    # Obtén la ruta del directorio actual
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construye la ruta al archivo de credenciales
    credentials_path = os.path.join(current_dir, 'credentials', 'bolsadevaloresaneiap-5dc01e6a121d.json')
    
    # Inicializar Firebase
    cred = credentials.Certificate(credentials_path)
    initialize_app(cred)
    
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
            return "Inicio de sesión exitoso"  # Credenciales correctas
        else:
            return "Credenciales incorrectas"  # Contraseña incorrecta
    else:
        return "Usuario no encontrado"  # Usuario no existe en Firebase

#Codigo Principal

if __name__ == '__main__':

    st.title("Sistema de Ingreso de Usuario")
    login()
