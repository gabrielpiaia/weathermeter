from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import os
import logging

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para conectar ao banco de dados e buscar dados
def execute_query(query):
    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "gabriel"),
            password=os.getenv("DB_PASSWORD", "Gabriel#12345!"),
            database=os.getenv("DB_NAME", "weathermeter")
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        logging.info(f"Query executed successfully: {query}")
        return result
    except Error as e:
        logging.error(f"Erro ao conectar ao MySQL: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 1. Rota para temperatura da última hora
@app.route('/api/temperatura_ultima_hora')
def temperatura_ultima_hora():
    try:
        now = datetime.now()
        uma_hora_atras = now - timedelta(hours=1)
        query = f"SELECT cidade, temperature, time FROM temperatura WHERE time >= '{uma_hora_atras.strftime('%Y-%m-%d %H:%M:%S')}'"
        logging.debug(f"Executing query: {query}")
        data = execute_query(query)

        if data is None:
            logging.error("Query returned None.")
            return jsonify({"error": "Query execution failed"}), 500
        
        if not data:
            logging.warning("No data found for the last hour")
            return jsonify([]), 200  # Retorna uma lista vazia com status 200

        logging.info(f"Data returned: {data}")
        return jsonify(data), 200
    except Exception as e:
        logging.error(f"Error occurred in temperatura_ultima_hora: {e}")
        return jsonify({"error": "Internal server error"}), 500

# 2. Rota para temperatura do dia atual
@app.route('/api/temperatura_dia_atual')
def temperatura_dia_atual():
    cidade = request.args.get('cidade')  # Obtém o parâmetro 'cidade' da URL

    if not cidade:
        logging.warning("Missing 'cidade' parameter in request.")
        return jsonify({"error": "Parâmetro 'cidade' é obrigatório"}), 400

    try:
        hoje = datetime.now().strftime('%Y-%m-%d')
        inicio_dia = f"{hoje} 00:00:00"
        fim_dia = f"{hoje} 23:59:59"
        query = f"SELECT cidade, temperature, time FROM temperatura WHERE cidade = '{cidade}' AND time BETWEEN '{inicio_dia}' AND '{fim_dia}'"
        logging.debug(f"Executing query: {query}")
        data = execute_query(query)

        if data is None:
            logging.error("Query returned None.")
            return jsonify({"error": "Query execution failed"}), 500
        
        if not data:
            logging.warning(f"No data found for city '{cidade}' today")
            return jsonify([]), 200  # Retorna uma lista vazia com status 200

        logging.info(f"Data returned for city '{cidade}': {data}")
        return jsonify(data), 200
    except Exception as e:
        logging.error(f"Error occurred in temperatura_dia_atual: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
# 3. Rota para temperatura com intervalo personalizado
@app.route('/api/temperatura_por_cidade')
def temperatura_por_cidade():
    cidade = request.args.get('cidade')
    datainicial = request.args.get('datainicial')
    datafinal = request.args.get('datafinal')

    if not cidade or not datainicial or not datafinal:
        logging.warning("Missing parameters in request.")
        return jsonify({"error": "Parâmetros 'cidade', 'datainicial' e 'datafinal' são obrigatórios"}), 400

    query = f"SELECT cidade, temperature, time FROM temperatura WHERE cidade = '{cidade}' AND time BETWEEN '{datainicial}' AND '{datafinal}'"
    logging.debug(f"Executing query: {query}")
    data = execute_query(query)

    if data is None:
        logging.error("Query returned None.")
        return jsonify({"error": "Query execution failed"}), 500

    if not data:
        logging.warning("No data found for the specified city and date range.")
        return jsonify([]), 200  # Retorna uma lista vazia com status 200

    logging.info(f"Data returned: {data}")
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
