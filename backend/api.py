from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import os
import logging

app = Flask(__name__)

# Função para conectar ao banco de dados e buscar dados
def execute_query(query):
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
        return result
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
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
            return jsonify({"error": "No data found"}), 404

        logging.info(f"Data returned: {data}")
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

# 2. Rota para temperatura do dia atual
@app.route('/api/temperatura_dia_atual')
def temperatura_dia_atual():
    hoje = datetime.now().strftime('%Y-%m-%d')
    inicio_dia = f"{hoje} 00:00:00"
    fim_dia = f"{hoje} 23:59:59"
    query = f"SELECT cidade, temperature, time FROM temperatura WHERE time BETWEEN '{inicio_dia}' AND '{fim_dia}'"
    data = execute_query(query)
    return jsonify(data) if data else jsonify({"error": "Erro ao buscar dados"}), 500

# 3. Rota para temperatura com intervalo personalizado
@app.route('/api/temperatura_por_cidade')
def temperatura_por_cidade():
    # Obter parâmetros da URL
    cidade = request.args.get('cidade')
    datainicial = request.args.get('datainicial')
    datafinal = request.args.get('datafinal')

    if not cidade or not datainicial or not datafinal:
        return jsonify({"error": "Parâmetros 'cidade', 'datainicial' e 'datafinal' são obrigatórios"}), 400

    # Query para intervalo de tempo personalizado
    query = f"SELECT cidade, temperature, time FROM temperatura WHERE cidade = '{cidade}' AND time BETWEEN '{datainicial}' AND '{datafinal}'"
    data = execute_query(query)
    return jsonify(data) if data else jsonify({"error": "Erro ao buscar dados"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
