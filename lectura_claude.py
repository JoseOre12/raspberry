import time
import board
import adafruit_bmp280
import adafruit_ahtx0

# Initialize I2C
i2c = board.I2C()

# Initialize sensors
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
aht10 = adafruit_ahtx0.AHTx0(i2c)

# Set up BMP280
bmp280.sea_level_pressure = 1013.25  # Adjust this value based on your location

try:
    while True:
        # Read data from BMP280
        pressure = bmp280.pressure

        # Read data from AHT10MOD
        temperature = aht10.temperature
        humidity = aht10.relative_humidity

        # Print the data
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print("------------------------")

        # Wait for 1 second before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by user.")