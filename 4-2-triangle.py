import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac_pins, GPIO.OUT)

def dec2bin(num):
    return list( map(int, bin(num)[2:].zfill(8)) )

BASE_VOLTAGE = 3.3
MAX_NUMBER = 256

PERIOD = 10
try:
    PERIOD = float(input('Введите период треугольного сигнала: '))
except ValueError:
    print(f'Неужели так сложно ввести число? Используем значение по умолчанию: {PERIOD}')
    
timer = time.process_time() 

current_voltage = 0
direction = 1
try:
    while(1):
        if ((time.process_time() - timer) > (PERIOD / (2*MAX_NUMBER))):
            timer = time.process_time()

            current_voltage += direction
            if (current_voltage == MAX_NUMBER or current_voltage == -1):
                direction = -direction
                current_voltage += 2*direction

            GPIO.output(dac_pins, dec2bin(current_voltage))    

        else:
            continue
finally:
    GPIO.output(dac_pins, 0)
    GPIO.cleanup()