import smbus2
import time

# I2C address of Arduino
ARDUINO_ADDRESS = 0x08

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

def read_arduino_data():
    # Read 4 bytes of data from Arduino
    data = bus.read_i2c_block_data(ARDUINO_ADDRESS, 0, 4)
    
    # Convert the data to sensor values
    sensor_value0 = (data[0] << 8) | data[1]
    sensor_value1 = (data[2] << 8) | data[3]
    
    return [sensor_value0, sensor_value1]

try:
    while True:
        sensor_values = read_arduino_data()
        print(f"Sensor Values: {sensor_values}")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    bus.close()
