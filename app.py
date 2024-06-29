# app.py

from flask import Flask, jsonify
from flask_cors import CORS
import random
#Import libraries for reading the sensor_data.csv file
import csv

app = Flask(__name__)
CORS(app)

#Function to get the last value from the sensor_data.csv file depending on the column
def get_last_value(column):
    with open('sensor_data.csv', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        values = last_line.split(',')
        return values[column]

@app.route('/api/temperatura', methods=['GET'])
def get_temperatura():
    data = {
        'description': 'Monitoreo de la temperatura ambiente en grados centígrados.',
        #Read the last temperature value from the database (sensor_data.csv)

        'valor': get_last_value("AHT10 Temperature (�C)") # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/humedad', methods=['GET'])
def get_humedad():
    data = {
        'description': 'Medición de la humedad relativa en el ambiente.',
        'valor': get_last_value("AHT10 Humidity (%)")   # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/viento', methods=['GET'])
def get_viento():
    data = {
        'description': 'Detección de la rapidez del viento con anemómetros.',
        'valor': get_last_value("Wind Speed (m/s)")  # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/luz', methods=['GET'])
def get_luz():
    data = {
        'description': 'Medición de la cantidad de luz ambiental para determinar si está soleado o nublado.',
        #Depending on the value of the last cloudy/sunny value from the database (sensor_data.csv) return the state
        'estado': 'Soleado' if get_last_value("Cloudy/Sunny") == '1' else 'Nublado'
    }
    return jsonify(data)

@app.route('/api/aire', methods=['GET'])
def get_aire():
    data = {
        'description': 'Monitoreo de los niveles de partículas y gases en el aire.',
        'estado': get_last_value("Air Quality (ppm)") # Simulando el estado
    }
    return jsonify(data)

@app.route('/api/presion', methods=['GET'])
def get_presion():
    data = {
        'description': 'Registro de la presión atmosférica para prever cambios climáticos.',
        'valor': get_last_value("BMP280 Pressure (hPa)")  # Simulando un valor aleatorio
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
