# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
import random
#Import libraries for reading the sensor_data.csv file
import csv

#Threading
import threading

app = Flask(__name__)
CORS(app)

#Function to get the last value from the sensor_data.csv file depending on the column
def get_last_value(column):
    with open('sensor_data.csv', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        values = last_line.split(',')
        return values[column]
    
#Declare global variables for the sensor values
temperatura = 0
humedad = 0
viento = 0
aire = 0
presion = 0
luz = 0

#Function to get the last value from the sensor_data.csv and update the global variables
def update_values():
    global temperatura
    global humedad
    global viento
    global aire
    global presion
    global luz
    with open('sensor_data.csv', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        values = last_line.split(',')
        temperatura = values[2]
        humedad = values[3]
        viento = values[4]
        aire = values[5]
        presion = values[1]
        luz = values[6]
    #Sleep for 5 seconds
    threading.Timer(5, update_values).start()

#Start the thread to update the values
threading.Thread(target=update_values).start()


@app.route('/api/temperatura', methods=['GET'])
def get_temperatura():
    global temperatura
    data = {
        'description': 'Monitoreo de la temperatura ambiente en grados centígrados.',
        #Read the last temperature value from the database (sensor_data.csv)

        'valor': temperatura # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/humedad', methods=['GET'])
def get_humedad():
    data = {
        'description': 'Medición de la humedad relativa en el ambiente.',
        'valor': get_last_value(3)   # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/viento', methods=['GET'])
def get_viento():
    data = {
        'description': 'Detección de la rapidez del viento con anemómetros.',
        'valor': get_last_value(4)  # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/luz', methods=['GET'])
def get_luz():
    data = {
        'description': 'Medición de la cantidad de luz ambiental para determinar si está soleado o nublado.',
        #Depending on the value of the last cloudy/sunny value from the database (sensor_data.csv) return the state
        'estado': 'Soleado' if get_last_value(6) == '1' else 'Nublado'
    }
    return jsonify(data)

@app.route('/api/aire', methods=['GET'])
def get_aire():
    data = {
        'description': 'Monitoreo de los niveles de partículas y gases en el aire.',
        'estado': get_last_value(5) # Simulando el estado
    }
    return jsonify(data)

@app.route('/api/presion', methods=['GET'])
def get_presion():
    data = {
        'description': 'Registro de la presión atmosférica para prever cambios climáticos.',
        'valor': get_last_value(1)  # Simulando un valor aleatorio
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
