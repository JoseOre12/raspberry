import threading
import time
import board
import busio
import adafruit_bmp280
import adafruit_ahtx0

# Global variables to store sensor data
bmp280_temperature = None
bmp280_pressure = None
aht10_temperature = None
aht10_humidity = None

# Lock for thread-safe access to shared data
data_lock = threading.Lock()

# Function to read BMP280 sensor data
def read_bmp280_data():
    global bmp280_temperature, bmp280_pressure
    i2c = busio.I2C(board.SCL, board.SDA)
    try:
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
        bmp280.sea_level_pressure = 1013.25
        while True:
            with data_lock:
                bmp280_temperature = bmp280.temperature
                bmp280_pressure = bmp280.pressure
            time.sleep(2)
    except Exception as e:
        print(f"Failed to initialize BMP280: {e}")

# Function to read AHT10 sensor data
def read_aht10_data():
    global aht10_temperature, aht10_humidity
    i2c = busio.I2C(board.SCL, board.SDA)
    try:
        aht10 = adafruit_ahtx0.AHTx0(i2c, address=0x38)
        while True:
            with data_lock:
                aht10_temperature = aht10.temperature
                aht10_humidity = aht10.relative_humidity
            time.sleep(2)
    except Exception as e:
        print(f"Failed to initialize AHT10: {e}")

# Create and start threads for each sensor
bmp280_thread = threading.Thread(target=read_bmp280_data)
aht10_thread = threading.Thread(target=read_aht10_data)

bmp280_thread.start()
aht10_thread.start()

# Main thread to print sensor data
try:
    while True:
        with data_lock:
            if bmp280_temperature is not None and bmp280_pressure is not None:
                print(f"BMP280 - Temperature: {bmp280_temperature:.2f} °C, Pressure: {bmp280_pressure:.2f} hPa")
            if aht10_temperature is not None and aht10_humidity is not None:
                print(f"AHT10 - Temperature: {aht10_temperature:.2f} °C, Humidity: {aht10_humidity:.2f} %")
        time.sleep(5)  # Adjust sleep time as needed
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully to stop threads
    bmp280_thread.join()
    aht10_thread.join()
    print("\nThreads stopped.")
