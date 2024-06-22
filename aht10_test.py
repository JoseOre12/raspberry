import time
import board
import busio
import adafruit_ahtx0

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize AHT10MOD with I2C address 0x38
aht10 = adafruit_ahtx0.AHTx0(i2c, address=0x38)

while True:
    temperature = aht10.temperature
    humidity = aht10.relative_humidity
    print(f'Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %')
    time.sleep(2)
