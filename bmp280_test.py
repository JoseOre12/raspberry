import time
import board
import busio
import adafruit_bmp280

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BMP280 with I2C address 0x76
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Optionally, set the sea level pressure for more accurate altitude measurements
bmp280.sea_level_pressure = 1013.25

while True:
    pressure = bmp280.pressure
    print(f'Pressure: {pressure:.2f} hPa')
    time.sleep(2)
