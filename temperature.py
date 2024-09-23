import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

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
    description = Column(String(100))  # Novo campo para descrição
    time = Column(DateTime)

# Cria a tabela no banco de dados (se não existir)
Base.metadata.create_all(engine)

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
        descricao = dados['weather'][0]['description']  # Descrição do clima em br &lang=pt_br
        return temperatura, descricao
    else:
        print("Erro ao obter os dados da API")
        return None, None

# Nome da cidade a ser consultada
city_name = "Pelotas"

# Loop para executar a cada 2 minutos
while True:
    # Obter a temperatura e descrição da cidade e salvar no banco de dados
    temperatura_atual, descricao_atual = obter_temperatura(city_name)
    if temperatura_atual is not None:
        salvar_dados_no_banco(city_name, temperatura_atual, descricao_atual)

    time.sleep(120)  
