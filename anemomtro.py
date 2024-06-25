import RPi.GPIO as GPIO
import time

# Pin where the LM393 output is connected
ENCODER_PIN = 17

# Configuration variables
RADIUS = 0.03  # Radius of the anemometer in meters
PULSES_PER_REVOLUTION = 1  # Number of pulses per revolution
MEASURE_INTERVAL = 5  # Time interval for measuring wind speed (in seconds)

# Calculate the circumference
CIRCUMFERENCE = 2 * 3.14159 * RADIUS

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def calculate_wind_speed(pulses, interval):
    revolutions = pulses / PULSES_PER_REVOLUTION
    distance = CIRCUMFERENCE * revolutions
    wind_speed = distance / interval  # meters per second
    return wind_speed

try:
    while True:
        pulse_count = count_pulses(ENCODER_PIN, MEASURE_INTERVAL)
        
        wind_speed = calculate_wind_speed(pulse_count, MEASURE_INTERVAL)
        wind_speed_kmh = wind_speed * 3.6
        
        print(f"Pulses: {pulse_count}")
        print(f"Wind Speed: {wind_speed:.2f} m/s, {wind_speed_kmh:.2f} km/h")

except KeyboardInterrupt:
    print("Measurement stopped by user")
finally:
    GPIO.cleanup()