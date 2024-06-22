import time
from smbus2 import SMBus

# I2C addresses
BMP280_ADDR = 0x76  # or 0x77, check with i2cdetect -y 1
AHT10_ADDR = 0x38

# Initialize I2C bus
bus = SMBus(1)  # 1 indicates /dev/i2c-1

def read_bmp280():
    # This is a simplified reading process and may need adjustment
    bus.write_byte_data(BMP280_ADDR, 0xF4, 0x27)
    data = bus.read_i2c_block_data(BMP280_ADDR, 0xF7, 8)
    pressure = ((data[0] << 16) | (data[1] << 8) | data[2]) / 256
    return pressure

def read_aht10():
    # Trigger measurement
    bus.write_i2c_block_data(AHT10_ADDR, 0xAC, [0x33, 0x00])
    time.sleep(0.1)
    
    # Read data
    data = bus.read_i2c_block_data(AHT10_ADDR, 0x00, 6)
    
    # Convert to temperature and humidity
    humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 0x100000
    temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200.0 / 0x100000 - 50
    
    return temperature, humidity

try:
    while True:
        pressure = read_bmp280()
        temperature, humidity = read_aht10()
        
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        print("------------------------")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Data collection stopped by user.")
finally:
    bus.close()