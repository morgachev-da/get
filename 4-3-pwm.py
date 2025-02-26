import RPi.GPIO as GPIO
# import time

GPIO.setmode(GPIO.BCM)

# dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
pwm_pin = 21
led_pwm = 9
GPIO.setup([pwm_pin, led_pwm], GPIO.OUT)

def dec2bin(num):
    return list( map(int, bin(num)[2:].zfill(8)) )

BASE_VOLTAGE = 3.3
MAX_NUMBER = 256
PWM_FREQ = 1000

pwm_controller = GPIO.PWM(pwm_pin, PWM_FREQ)
led_controller = GPIO.PWM(led_pwm, PWM_FREQ)
pwm_controller.start(0)
led_controller.start(0)
try:
    while (1):
        duty = 0
        try:
            duty = float(input('Введите коэффициент заполнения 0-100: '))
        except ValueError:
            print('Неужели так сложно ввести число?')
            continue

        if not (0 <= duty <= 100.0):
            print('Не входит в диапазон')
            continue

        pwm_controller.ChangeDutyCycle(duty)
        led_controller.ChangeDutyCycle(duty)
        print(f'U_exp = {BASE_VOLTAGE * duty / 100:.2f} V')
finally:
    # GPIO.output(dac_pins, 0)
    GPIO.cleanup()