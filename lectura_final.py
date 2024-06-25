import threading
import csv
import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_bmp280
import adafruit_ahtx0
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Global variables to store sensor data
bmp280_pressure = None
aht10_temperature = None
aht10_humidity = None
wind_speed = None
cloudy_sunny = None
air_quality = None

# Lock for thread-safe access to shared data
data_lock = threading.Lock()

# Pin where the LM393 output is connected
ENCODER_PIN = 17

# Pin where the cloudy/sunny sensor is connected
CLOUDY_SUNNY_PIN = 27

# Configuration variables for wind speed measurement
RADIUS = 0.03  # Radius of the anemometer in meters
PULSES_PER_REVOLUTION = 20  # Number of pulses per revolution
MEASURE_INTERVAL = 5  # Time interval for measuring wind speed (in seconds)

# Calculate the circumference
CIRCUMFERENCE = 2 * 3.14159 * RADIUS

# Function to read BMP280 pressure data
def read_bmp280_pressure():
    global bmp280_pressure
    while True:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
            bmp280.sea_level_pressure = 1013.25
            print("BMP280 initialized successfully")
            while True:
                with data_lock:
                    bmp280_pressure = bmp280.pressure
                time.sleep(2)
        except Exception as e:
            print(f"Failed to initialize BMP280: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Function to read AHT10 temperature and humidity data
def read_aht10_data():
    global aht10_temperature, aht10_humidity
    while True:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            aht10 = adafruit_ahtx0.AHTx0(i2c, address=0x38)
            print("AHT10 initialized successfully")
            while True:
                with data_lock:
                    aht10_temperature = aht10.temperature
                    aht10_humidity = aht10.relative_humidity
                time.sleep(2)
        except Exception as e:
            print(f"Failed to initialize AHT10: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Function to read air quality data from ADS1115
def read_air_quality():
    global air_quality
    while True:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS.ADS1115(i2c)
            chan = AnalogIn(ads, ADS.P0)
            print("ADS1115 initialized successfully")
            while True:
                with data_lock:
                    air_quality = chan.voltage * 1000  # Convert to ppm, adjust as necessary
                time.sleep(2)
        except Exception as e:
            print(f"Failed to initialize ADS1115: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Function to count pulses for wind speed measurement
def count_pulses(pin, duration):
    pulse_count = 0
    start_time = time.time()
    
    while time.time() - start_time < duration:
        if GPIO.input(pin) == GPIO.LOW:
            pulse_count += 1
            # Wait for the signal to go high again
            while GPIO.input(pin) == GPIO.LOW:
                pass
    
    return pulse_count

# Function to calculate wind speed
def calculate_wind_speed(pulses, interval):
    revolutions = pulses / PULSES_PER_REVOLUTION
    distance = CIRCUMFERENCE * revolutions
    wind_speed = distance / interval  # meters per second
    return wind_speed

# Function to measure wind speed
def measure_wind_speed():
    global wind_speed
    while True:
        pulse_count = count_pulses(ENCODER_PIN, MEASURE_INTERVAL)
        with data_lock:
            wind_speed = calculate_wind_speed(pulse_count, MEASURE_INTERVAL)
        print(f"Wind Speed: {wind_speed:.2f} m/s")

# Function to read cloudy/sunny sensor data
def read_cloudy_sunny():
    global cloudy_sunny
    while True:
        with data_lock:
            cloudy_sunny = 1 if GPIO.input(CLOUDY_SUNNY_PIN) else 0
        time.sleep(2)

# Function to write sensor data to CSV file
def write_to_csv():
    csv_filename = "sensor_data.csv"
    fieldnames = ["Timestamp", "BMP280 Pressure (hPa)", "AHT10 Temperature (°C)", "AHT10 Humidity (%)", "Wind Speed (m/s)", "Cloudy/Sunny", "Air Quality (ppm)"]

    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with data_lock:
            data_row = {
                "Timestamp": timestamp,
                "BMP280 Pressure (hPa)": f"{bmp280_pressure:.2f}" if bmp280_pressure is not None else "",
                "AHT10 Temperature (°C)": f"{aht10_temperature:.2f}" if aht10_temperature is not None else "",
                "AHT10 Humidity (%)": f"{aht10_humidity:.2f}" if aht10_humidity is not None else "",
                "Wind Speed (m/s)": f"{wind_speed:.2f}" if wind_speed is not None else "",
                "Cloudy/Sunny": cloudy_sunny if cloudy_sunny is not None else "",
                "Air Quality (ppm)": f"{air_quality:.2f}" if air_quality is not None else ""
            }

        # Write data to CSV file
        try:
            with open(csv_filename, mode='a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if csv_file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data_row)
        except Exception as e:
            print(f"Error writing to CSV: {e}")

        time.sleep(5)  # Adjust sleep time as needed

# Setup GPIO for the encoder and cloudy/sunny sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLOUDY_SUNNY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create threads for sensor readings and CSV writing
bmp280_thread = threading.Thread(target=read_bmp280_pressure)
aht10_thread = threading.Thread(target=read_aht10_data)
wind_speed_thread = threading.Thread(target=measure_wind_speed)
cloudy_sunny_thread = threading.Thread(target=read_cloudy_sunny)
air_quality_thread = threading.Thread(target=read_air_quality)
csv_thread = threading.Thread(target=write_to_csv)

# Start threads
bmp280_thread.start()
aht10_thread.start()
wind_speed_thread.start()
cloudy_sunny_thread.start()
air_quality_thread.start()
csv_thread.start()

# Main thread to print sensor data
try:
    while True:
        with data_lock:
            if bmp280_pressure is not None:
                print(f"BMP280 - Pressure: {bmp280_pressure:.2f} hPa")
            if aht10_temperature is not None and aht10_humidity is not None:
                print(f"AHT10 - Temperature: {aht10_temperature:.2f} °C, Humidity: {aht10_humidity:.2f} %")
            if wind_speed is not None:
                print(f"Wind Speed: {wind_speed:.2f} m/s")
            if cloudy_sunny is not None:
                print(f"Weather Condition: {cloudy_sunny}")
            if air_quality is not None:
                print(f"Air Quality: {air_quality:.2f} ppm")
        time.sleep(5)  # Adjust sleep time as needed
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully to stop threads
    GPIO.cleanup()
    print("\nThreads stopped.")