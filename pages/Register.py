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
    
    # Obtén la ruta del directorio actual
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construye la ruta al archivo de credenciales
    credentials_path = os.path.join(current_dir, 'credentials', 'bolsadevaloresaneiap-5dc01e6a121d.json')
    
    # Inicializar Firebase
    cred = credentials.Certificate(credentials_path)
    initialize_app(cred)
    
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
