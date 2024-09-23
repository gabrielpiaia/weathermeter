from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Função para buscar os dados do MySQL
def get_temperatura_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="gabriel",
        password="Gabriel#12345!",
        database="weathermeter"
    )
    cursor = conn.cursor(dictionary=True)
    query = "SELECT cidade, temperature, time FROM temperatura"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Rota que retorna os dados de temperatura em formato JSON
@app.route('/api/temperatura')
def temperatura():
    data = get_temperatura_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)