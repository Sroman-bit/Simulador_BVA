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

#Funciones

#from pages import Login  # Importa el archivo login.py

# Obtener el valor de usuario_autenticado desde login.py
#usuario_autenticado = Login.usuario_autenticado

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

doc_ref_variables = db.collection("usuarios").document("variables")
doc = doc_ref_variables.get()
usuario_logueado = doc.to_dict().get("usuario_logueado")

def obtener_saldo_usuario(usuario):

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

    doc_ref_usuario = db.collection("usuarios").document(usuario)
    doc_usuario = doc_ref_usuario.get()

    return doc_usuario.get("Saldo")
    print(doc_usuario.get("Saldo"))

def conseguir_precio_actual(ticker):
    data_actual = yf.Ticker(ticker).history(period='1y')
    return {'': data_actual.iloc[-1].Close,}

st.set_page_config( page_title = "Simulador BVA")
ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
ticker = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
fecha_predeterminada = datetime(2020, 10, 10)
Fecha_Inicio = st.sidebar.date_input("Fecha de Inicio", fecha_predeterminada)
Fecha_Fin = st.sidebar.date_input("Fecha de Fin")
st.sidebar.header("Usuario logueado")
st.sidebar.text(usuario_logueado)
monto = 1000
texto = 'El precio actual de esta acción es '

#Grafico del movimiento de precios de la accion
tickerData = yf.Ticker(ticker)
nombre_empresa = ticker
data = yf.download(ticker, start = Fecha_Inicio , end = Fecha_Fin )
fig = px.line(data, x = data.index, y = data['Adj Close'], title = nombre_empresa)
st.plotly_chart(fig)
status_text = st.empty()


#Objetos, Clases y Funciones
class Stock:
    def __init__(self, ticker, precio, Cantidad):
        self.ticker = ticker
        self.precio = precio
        self.Cantidad = Cantidad

class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        self.stocks.append(stock)

    def remove_stock(self, ticker):
        for stock in self.stocks:
            if stock.ticker == ticker:
                self.stocks.remove(stock)

    def calcular_valor_portafolio(self):
        valor_total = 0
        for stock in self.stocks:
            valor_total += stock.precio * stock.Cantidad
        return valor_total

    def encontrar_stock(self, ticker):
        for stock in self.stocks:
            if stock.ticker == ticker:
                return stock
        return None
    def get_portfolio_info(self):
        portfolio_info = []
        for stock in self.stocks:
            portfolio_info.append((stock.ticker, stock.Cantidad))
        return portfolio_info

class User:
    def __init__(self, monto):
        self.balance = monto
        self.portfolio = Portfolio()
        self.invertido = []

    def comprar(self, Cantidad, precio,ticker):
        dinero_asignado = Cantidad * precio
        costo_transaccion = 0.025
        total_cost = dinero_asignado + costo_transaccion * dinero_asignado

        if self.balance >= total_cost:
            self.balance -= total_cost
            self.portfolio.add_stock(Stock(ticker, precio, Cantidad))
            if not self.invertido:
                self.invertido.append(dinero_asignado)
            else:
                self.invertido.append(dinero_asignado + self.invertido[-1])

    def vender(self, Cantidad, precio ,ticker):
        stock_por_vender = self.portfolio.encontrar_stock(ticker)
        if stock_por_vender and stock_por_vender.Cantidad >= Cantidad:
            dinero_asignado = Cantidad * precio
            costo_transaccion = 0.025
            total_proceeds = dinero_asignado - costo_transaccion * dinero_asignado

            self.balance += total_proceeds
            stock_por_vender.Cantidad -= Cantidad

            self.invertido.append(dinero_asignado + self.invertido[-1])

user = User(monto)

informacion_precios, noticias, Portafolio = st.tabs(["Datos de precios", "Top 10 noticias", "Portafolio Personal"])

with informacion_precios:
      st.header("Movimiento de Precios de la Acción")
      st.write(data)
      st.write("Open: El precio al que se inició la negociación de acciones en un día específico.")
      st.write("High: El precio más alto de la acción durante un día específico. Es decir, el precio más alto al que se habían vendido las acciones en el mercado ese día.")
      st.write("Low: El precio de la acción en su punto más bajo durante un día en particular. En otras palabras, el precio más bajo al que se habían vendido las acciones en el mercado ese día.")
      st.write("Close: El precio al que finalizó la negociación de acciones en un día de mercado específico.")
      st.write("Adj Close: El precio de cierre (Close) de la acción se resta de los dividendos o divisiones que se declararon sobre las acciones durante el día de negociación para llegar a este precio.")
      st.write("Volume: Número total de acciones vendidas en el mercado durante un determinado día. Es un indicador crucial de la actividad del mercado y puede mostrar la fuerza y ​​dirección del movimiento del precio de una acción")

with noticias:
    st.header(f"Noticias de {ticker}")

    sn = sn.StockNews(ticker, save_news = False)
    df_noticias = sn.read_rss()
    for i in range(10):
      st.subheader(f"Noticia {i + 1}")
      st.write(df_noticias['published'][i])
      titulo_traducido = translator.translate(df_noticias['title'][i], src='en', dest='es')
      st.write(titulo_traducido.text)
      resumen_traducido = translator.translate(df_noticias['summary'][i], src='en', dest='es')
      st.write(resumen_traducido.text)

with Portafolio:
    st.header("Portafolio del Usuario")
    boton_comprar = st.button("Comprar esta Acción")
    boton_vender = st.button("Vender esta Acción")
    Cantidad = st.slider("¿Cuantas acciones de este Empresa deseas Comprar/Vender?", 1, 100, 10)
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
    
    # Obtener el portafolio actual del usuario y mostrarlo en la aplicación
    try:
        # Obtener el portafolio actual del usuario y mostrarlo en la aplicación
        portafolio_actual = db.collection("usuarios").document(usuario_logueado).get().to_dict().get("Portafolio", [])
        st.write(portafolio_actual)
    except Exception as e:
        # Manejar la excepción específica (puedes personalizar esto según el tipo de excepción que se produzca)
        st.warning("PARA ACCEDER A LAS FUNCIONES DEL PORTAFOLIO COMPLETAS SIN ERRORES DEBES PRIMERO LOGUEARTE, VE A LOGIN E INGRESA TU USUARIO.")

    precio = conseguir_precio_actual(ticker)
    precio_actual = round(precio[''], 4) * random.uniform(0.995, 1.005)
    status_text.text(texto + str(precio_actual))

    if boton_comprar:
        try:
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
    
            # Obtener el saldo del usuario
            saldo_usuario = obtener_saldo_usuario(usuario_logueado)
    
            # Calcular el costo total de las acciones
            costo_total = Cantidad * precio_actual
    
            # Verificar si el usuario tiene suficiente saldo
            if saldo_usuario is not None and saldo_usuario >= costo_total:
    
                # Actualizar el saldo del usuario en la base de datos
                nuevo_saldo = saldo_usuario - costo_total
                db.collection("usuarios").document(usuario_logueado).update({"Saldo": nuevo_saldo})
    
                # Obtener la fecha actual
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
                # Obtener el portafolio actual del usuario
                portafolio_actual = db.collection("usuarios").document(usuario_logueado).get().to_dict().get("Portafolio", [])
                # Verificar si el usuario ya tiene acciones de ese ticker en su portafolio
                stock_existente = next((stock for stock in portafolio_actual if stock["Ticker"] == ticker), None)
                # Actualizar el portafolio del usuario
                if stock_existente:
                    # Si el usuario ya tiene acciones de ese ticker, actualizar la cantidad
                    stock_existente["Cantidad"] += Cantidad
                    # Crear una nueva lista de portafolio actualizada
                    nuevo_portafolio = [stock if stock["Ticker"] != ticker else stock_existente for stock in portafolio_actual]
                    # Actualizar el campo "Portafolio" en el documento de la base de datos
                    db.collection("usuarios").document(usuario_logueado).update({
                        "Portafolio": nuevo_portafolio
                    })
                else:
                    # Si el usuario no tiene acciones de ese ticker, añadir un nuevo portafolio
                    nueva_accion = {"Ticker": ticker, "Cantidad": Cantidad}
                    db.collection("usuarios").document(usuario_logueado).update({
                        "Portafolio": firestore.ArrayUnion([nueva_accion])
                    })
    
                # Actualizar el historial de transacciones del usuario
                historial_transacciones = {
                    "Ticker": ticker,
                    "Cantidad": Cantidad,
                    "Precio Individual": precio_actual,
                    "Saldo Anterior": saldo_usuario,
                    "Nuevo Saldo": nuevo_saldo,
                    "Fecha": fecha_actual
                }
    
                # Añadir el historial de transacciones al usuario
                db.collection("usuarios").document(usuario_logueado).update({
                    "HistorialTransacciones": firestore.ArrayUnion([historial_transacciones])
                })
    
                # Actualizar la interfaz de usuario
                st.success(f"Compra exitosa: {Cantidad} acciones de {ticker} por un total de {costo_total}. Saldo restante: {nuevo_saldo}")
            else:
                st.warning("No tienes suficiente saldo para realizar esta compra.")
        except Exception as e:
            # Manejar la excepción específica (puedes personalizar esto según el tipo de excepción que se produzca)
            st.warning("Error al procesar la compra. Por favor, inicie sesión para realizar transacciones.")

    if boton_vender:
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

        # Obtener el saldo del usuario
        saldo_usuario = obtener_saldo_usuario(usuario_logueado)

        # Obtener el portafolio actual del usuario
        portafolio_actual = db.collection("usuarios").document(usuario_logueado).get().to_dict().get("Portafolio", [])

        # Buscar el stock a vender en el portafolio del usuario
        stock_a_vender = next((stock for stock in portafolio_actual if stock["Ticker"] == ticker), None)

        # Verificar si el usuario tiene suficientes acciones para vender
        if stock_a_vender is not None and stock_a_vender["Cantidad"] >= Cantidad:

            # Calcular el monto total de la venta
            monto_venta = Cantidad * precio_actual

            # Actualizar el saldo del usuario en la base de datos (aumentar)
            nuevo_saldo = saldo_usuario + monto_venta
            db.collection("usuarios").document(usuario_logueado).update({"Saldo": nuevo_saldo})

            # Obtener la fecha actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Actualizar el historial de transacciones del usuario (añadiendo la venta)
            historial_transacciones = {
                "Ticker": ticker,
                "Cantidad": -Cantidad,  # El signo negativo indica una venta
                "Precio Individual": precio_actual,
                "Saldo Anterior": obtener_saldo_usuario(usuario_logueado),
                "Nuevo Saldo": nuevo_saldo,
                "Fecha": fecha_actual
            }
            st.write(stock_a_vender)
            # Verificar si se vende la totalidad del stock
            if stock_a_vender["Cantidad"] == Cantidad:
                # Eliminar la acción vendida del portafolio del usuario
                db.collection("usuarios").document(usuario_logueado).update({
                    "HistorialTransacciones": firestore.ArrayUnion([historial_transacciones]),
                    "Portafolio": firestore.ArrayRemove([stock_a_vender])
                })
                st.write("cumplió")
            else:
                # Actualizar la cantidad de acciones en el portafolio del usuario
                stock_a_vender["Cantidad"] -= Cantidad
                # Actualizar el portafolio del usuario en la base de datos
                nuevo_portafolio = [stock if stock["Ticker"] != ticker else stock_a_vender for stock in portafolio_actual]
                # Actualizar el campo "Portafolio" en el documento de la base de datos
                db.collection("usuarios").document(usuario_logueado).update({
                    "HistorialTransacciones": firestore.ArrayUnion([historial_transacciones]),
                    "Portafolio": nuevo_portafolio
                })

            # Actualizar la interfaz de usuario
            st.success(f"Venta exitosa: {Cantidad} acciones de {ticker} por un total de {Cantidad * precio_actual}. Nuevo saldo: {nuevo_saldo}")
        else:
            st.warning("No tienes suficientes acciones para realizar esta venta.")
