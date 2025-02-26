import RPi.GPIO as GPIO
# import time

GPIO.setmode(GPIO.BCM)

dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac_pins, GPIO.OUT)

def dec2bin(num):
    return list( map(int, bin(num)[2:].zfill(8)) )

BASE_VOLTAGE = 3.3
MAX_NUMBER = 256

try:
    while (1):
        usr_input = input('Введите число от 0 до 255 либо q:')
        if usr_input[0] == 'q': #any input that starts with q is quit
            break

        number = 0
        try:
            number = int(usr_input)
        except ValueError:
            try:
                number = float(usr_input)
            except ValueError:
                print('Это не число. Попробуйте снова')
            else:
                print('Вещественные числа запрещены')
            continue

        if not (0 <= number <= 255 ):
            print('Введённое число не входит в нужный диапазон')
            continue

        print(f'Ожидаемое напряжение: {number / MAX_NUMBER * BASE_VOLTAGE:.3f}')
        GPIO.output(dac_pins, dec2bin(number))    
finally:
    GPIO.output(dac_pins, 0)
    GPIO.cleanup()

