import requests
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import time
import threading

# Configuração do banco de dados MySQL
DATABASE_URI = 'mysql+pymysql://gabriel:Gabriel#12345!@localhost:3306/weathermeter'

# Conexão e configuração do SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definição da tabela 'temperatura'
class Temperatura(Base):
    __tablename__ = 'temperatura'

    id = Column(Integer, primary_key=True)
    cidade = Column(String(50))
    temperature = Column(Float)
    description = Column(String(100))
    time = Column(DateTime)

# Cria a tabela no banco de dados (se não existir)
Base.metadata.create_all(engine)

app = Flask(__name__)

# Função para salvar a cidade, temperatura e descrição no banco de dados
def salvar_dados_no_banco(city_name, temperature, description):
    nova_temperatura = Temperatura(cidade=city_name, temperature=temperature, description=description, time=datetime.now())
    session.add(nova_temperatura)
    session.commit()
    print(f"Dados salvos: {city_name} - {temperature}°C - {description}")

# Função para consumir a API do OpenWeather
def obter_temperatura(city_name):
    API_KEY = "2aa6d979d34f9c35275a767a6bc2d620"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=pt_br"

    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        temperatura = dados['main']['temp']  # Temperatura em Celsius
        descricao = dados['weather'][0]['description']  # Descrição do clima
        return temperatura, descricao
    else:
        print("Erro ao obter os dados da API")
        return None, None

# Função para buscar e salvar dados a cada 2 minutos
def coletar_dados_periodicamente():
    city_name = "Santa Vitória do Palmar"
    while True:
        temperatura_atual, descricao_atual = obter_temperatura(city_name)
        if temperatura_atual is not None:
            salvar_dados_no_banco(city_name, temperatura_atual, descricao_atual)
        time.sleep(120)  # Aguarda 120 segundos (2 minutos)

# Rota para temperatura da última hora
@app.route('/api/temperatura_ultima_hora')
def temperatura_ultima_hora():
    now = datetime.now()
    uma_hora_atras = now - timedelta(hours=1)
    query = f"SELECT cidade, temperature, time FROM temperatura WHERE time >= '{uma_hora_atras.strftime('%Y-%m-%d %H:%M:%S')}'"
    data = session.execute(query).fetchall()
    return jsonify([dict(row) for row in data])

# Rota para temperatura do dia atual
@app.route('/api/temperatura_dia_atual')
def temperatura_dia_atual():
    hoje = datetime.now().strftime('%Y-%m-%d')
    inicio_dia = f"{hoje} 00:00:00"
    fim_dia = f"{hoje} 23:59:59"
    query = f"SELECT cidade, temperature, time FROM temperatura WHERE time BETWEEN '{inicio_dia}' AND '{fim_dia}'"
    data = session.execute(query).fetchall()
    return jsonify([dict(row) for row in data])

# Rota para temperatura com intervalo personalizado
@app.route('/api/temperatura_intervalo')
def temperatura_intervalo():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    if not inicio or not fim:
        return jsonify({"error": "Parâmetros 'inicio' e 'fim' são obrigatórios"}), 400

    query = f"SELECT cidade, temperature, time FROM temperatura WHERE time BETWEEN '{inicio}' AND '{fim}'"
    data = session.execute(query).fetchall()
    return jsonify([dict(row) for row in data])

if __name__ == '__main__':
    # Inicia a coleta de dados em uma thread separada
    threading.Thread(target=coletar_dados_periodicamente, daemon=True).start()
    app.run(debug=True)
