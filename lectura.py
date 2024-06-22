import time
import board
import busio
import adafruit_bmp280
import adafruit_ahtx0

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BMP280
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
    bmp280.sea_level_pressure = 1013.25
    bmp280_initialized = True
    print("BMP280 initialized successfully")
except Exception as e:
    bmp280_initialized = False
    print(f"Failed to initialize BMP280: {e}")

# Initialize AHT10MOD
try:
    aht10 = adafruit_ahtx0.AHTx0(i2c, address=0x38)
    aht10_initialized = True
    print("AHT10 initialized successfully")
except Exception as e:
    aht10_initialized = False
    print(f"Failed to initialize AHT10: {e}")

if bmp280_initialized and aht10_initialized:
    # Open a file to write the data
    with open('sensor_data.csv', 'w') as f:
        # Write the header
        f.write('Timestamp,Temperature (C),Humidity (%),Pressure (hPa)\n')
        
        while True:
            try:
                # Read temperature, humidity, and pressure
                temp_aht10 = aht10.temperature
                humidity_aht10 = aht10.relative_humidity
                pressure_bmp280 = bmp280.pressure

                # Get current time
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                # Write data to file
                f.write(f'{timestamp},{temp_aht10:.2f},{humidity_aht10:.2f},{pressure_bmp280:.2f}\n')

                # Print data to console
                print(f'Time: {timestamp} - Temperature: {temp_aht10:.2f} C, Humidity: {humidity_aht10:.2f} %, Pressure: {pressure_bmp280:.2f} hPa')

            except Exception as e:
                print(f"Error reading sensor data: {e}")

            # Wait for 2 seconds before next reading
            time.sleep(2)
else:
    print("One or both sensors failed to initialize.")
