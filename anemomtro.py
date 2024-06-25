import RPi.GPIO as GPIO
import time

# Pin where the LM393 output is connected
ENCODER_PIN = 17

# Time interval for measuring wind speed (in seconds)
MEASURE_INTERVAL = 5

# Radius of the anemometer in meters (you'll need to measure this)
RADIUS = 0.03  # example radius

# Calculate the circumference
CIRCUMFERENCE = 2 * 3.14159 * RADIUS

# Pulses per revolution (depends on your anemometer setup)
PULSES_PER_REVOLUTION = 1  # example value, set according to your hardware

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global pulse counter
pulse_count = 0

def pulse_callback(channel):
    global pulse_count
    pulse_count += 1

# Add event detection on the encoder pin
GPIO.add_event_detect(ENCODER_PIN, GPIO.FALLING, callback=pulse_callback)

def calculate_wind_speed(pulses, interval):
    # Calculate revolutions
    revolutions = pulses / PULSES_PER_REVOLUTION
    # Calculate distance covered (circumference * revolutions)
    distance = CIRCUMFERENCE * revolutions
    # Wind speed (distance per time)
    wind_speed = distance / interval  # meters per second
    return wind_speed

try:
    while True:
        # Reset pulse count
        pulse_count = 0
        # Wait for the measurement interval
        time.sleep(MEASURE_INTERVAL)
        # Calculate wind speed
        wind_speed = calculate_wind_speed(pulse_count, MEASURE_INTERVAL)
        # Convert wind speed to a preferred unit if needed (e.g., km/h)
        wind_speed_kmh = wind_speed * 3.6
        print(f"Wind Speed: {wind_speed:.2f} m/s, {wind_speed_kmh:.2f} km/h")

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()
