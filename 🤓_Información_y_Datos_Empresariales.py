#Librerias a Importar

import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from datetime import datetime
import stocknews as sn
from googletrans import Translator

translator = Translator()
import time
import random

#Funciones

def conseguir_precio_actual(ticker):
    data_actual = yf.Ticker(ticker).history(period='1y')
    return {'': data_actual.iloc[-1].Close,}

# Función para el inicio de sesión
def login():
    st.header("Iniciar Sesión")
    correo = st.text_input("Correo Electrónico")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        # Verificar si los campos están completos (puedes agregar más validaciones aquí)
        if correo and usuario and contrasena:
            # Realizar la validación del usuario y contraseña (puedes agregar tu propia lógica)
            if validar_usuario(correo, usuario, contrasena):
                st.success("Inicio de sesión exitoso")
                # Llevar al usuario a la parte del simulador
                mostrar_simulador()
            else:
                st.error("Credenciales incorrectas")
        else:
            st.warning("Por favor, completa todos los campos.")

# Función para el registro
def registro():
    st.header("Registrarse")
    correo = st.text_input("Correo Electrónico")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password")
    
    if st.button("Registrarse"):
        # Verificar si los campos están completos (puedes agregar más validaciones aquí)
        if correo and usuario and contrasena and confirmar_contrasena:
            # Verificar que las contraseñas coincidan
            if contrasena == confirmar_contrasena:
                # Realizar la lógica de registro (puedes agregar tu propia lógica)
                registrar_usuario(correo, usuario, contrasena)
                st.success("Registro exitoso")
                # Llevar al usuario a la parte del simulador
                mostrar_simulador()
            else:
                st.error("Las contraseñas no coinciden")
        else:
            st.warning("Por favor, completa todos los campos.")

# Función para mostrar el simulador
def mostrar_simulador():
    st.write("¡Bienvenido al simulador!")
    # Aquí puedes agregar la lógica y la interfaz del simulador

# Simulación de la validación del usuario
def validar_usuario(correo, usuario, contrasena):
    # Aquí deberías agregar tu propia lógica de validación de usuario
    # Puedes comparar las credenciales con las almacenadas en una base de datos o archivo
    # En este ejemplo, solo se simula la validación
    return True

# Simulación del registro de usuario
def registrar_usuario(correo, usuario, contrasena):
    # Aquí deberías agregar tu propia lógica de registro de usuario
    # Puedes almacenar las credenciales en una base de datos o archivo
    # En este ejemplo, solo se simula el registro
    pass

#Codigo Principal

st.title("Sistema de Validación de Usuario")

# Página de inicio que permite al usuario seleccionar entre iniciar sesión y registrarse
pagina_inicio = st.radio("Elija una opción:", ("Iniciar Sesión", "Registrarse"))

if pagina_inicio == "Iniciar Sesión":
    login()
elif pagina_inicio == "Registrarse":
    registro()

st.set_page_config( page_title = "Simulador BVA")
ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
ticker = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
fecha_predeterminada = datetime(2020, 10, 10)
Fecha_Inicio = st.sidebar.date_input("Fecha de Inicio", fecha_predeterminada)
Fecha_Fin = st.sidebar.date_input("Fecha de Fin")
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
    precio = conseguir_precio_actual(ticker)
    precio_actual = round(precio[''], 4) * random.uniform(0.995, 1.005)
    status_text.text(texto + str(precio_actual))

    if boton_comprar:
        user.comprar(Cantidad, precio_actual,ticker)
        user_balance = user.balance  # Obtener el balance actualizado
        portfolio_value = user.portfolio.calcular_valor_portafolio()
        investment_history = user.invertido
        st.text(f"Balance de Usuario: {user_balance}")
        st.text(f"Valor del Portafolio: {portfolio_value}")
        st.text(f"Historial de Inversiones o transacciones: {investment_history}")
        portfolio_info = user.portfolio.get_portfolio_info()
        for ticker, Cantidad in portfolio_info:
          st.text(f"ticker: {ticker}, Cantidad: {Cantidad}")

    if boton_vender:
        user.vender(Cantidad, precio_actual,ticker)
        user_balance = user.balance  # Obtener el balance actualizado
        portfolio_value = user.portfolio.calcular_valor_portafolio()
        investment_history = user.invertido
        st.text(f"Balance de Usuario: {user_balance}")
        st.text(f"Valor del Portafolio: {portfolio_value}")
        st.text(f"Historial de Inversiones o transacciones: {investment_history}")
        portfolio_info = user.portfolio.get_portfolio_info()
        for ticker, Cantidad in portfolio_info:
          st.text(f"ticker: {ticker}, Cantidad: {Cantidad}")
