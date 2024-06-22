import time
import board
import busio
import adafruit_bmp280
import adafruit_ahtx0

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BMP280 with I2C address 0x76
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Initialize AHT10MOD with I2C address 0x38
aht10 = adafruit_ahtx0.AHTx0(i2c, address=0x38)

# Optionally, set the sea level pressure for more accurate altitude measurements
bmp280.sea_level_pressure = 1013.25

# Open a file to write the data
with open('sensor_data.csv', 'w') as f:
    # Write the header
    f.write('Timestamp,Temperature (C),Humidity (%),Pressure (hPa)\n')
    
    while True:
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

        # Wait for 2 seconds before next reading
        time.sleep(2)
