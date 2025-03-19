import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

settings = open("settings.txt", "w")

troyka_pin     = 13
comparator_pin = 14
dac_pins       = [8, 11, 7, 1, 0, 5, 12, 6]
led_pins       = [2, 3, 4, 17, 27, 22, 10, 9]


GPIO.setup(dac_pins, GPIO.OUT)
GPIO.setup(led_pins, GPIO.OUT)

GPIO.setup(comparator_pin, GPIO.IN)
GPIO.setup(troyka_pin, GPIO.OUT, initial = 0)

def number_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

BASE_VOLTAGE = 3.3
SLEEP_TIME   = 0.003
# reads analog voltage and returns voltage in scale of 0..255
def adc():
    # binary search algorithm
    exponent = 128
    number = 0
    while (exponent > 0):
        # print(number, exponent)
        number += exponent

        GPIO.output(dac_pins, number_to_bin(number))
        
        #time to get stable voltage 
        time.sleep(SLEEP_TIME)

        # comparator returns 0 if voltage < DAC
        if GPIO.input(comparator_pin) == 1:
            number -= exponent

        exponent //= 2

    return number

# Get float voltage value from troyka voltage pin
def getVoltage():
    return adc() / 256 * BASE_VOLTAGE

# Show voltage in scale from 0 to BASE_VOLTAGE on LED pins
def showVoltage(voltage : float):
    voltage_int = int(voltage * 256 / BASE_VOLTAGE)
    GPIO.output(led_pins, number_to_bin(voltage_int))


data_voltage = []
data_time    = []

MAX_CAPACITOR_VOLTAGE = 2.6
CHARGED_VOLTAGE    = 0.97 * MAX_CAPACITOR_VOLTAGE 
DISCHARGED_VOLTAGE = 0.20 * MAX_CAPACITOR_VOLTAGE

# while (1):
#     GPIO.output(dac_pins, number_to_bin(255))

try:
    print("Charging capacitor...")
    start_time = time.time()
    GPIO.output(troyka_pin, 1) # charging capacitor
    
    voltage = getVoltage()
    # GPIO.output(dac_pins, 0)

    while (voltage < CHARGED_VOLTAGE):
        # print(voltage)
        data_time.append(time.time() - start_time)
        data_voltage.append(voltage)
        showVoltage(voltage)
        time.sleep(0.01)
        voltage = getVoltage()
        # GPIO.output(dac_pins, 0)

    charge_points = len(data_voltage)
    print("Capacitor is charged. Discharding...")
    print(f'Current time: {data_time[-1]}')
    print(f'T = {data_time[-1] / charge_points}, f = {charge_points / data_time[-1]}')
    settings.write(f'T = {data_time[-1] / charge_points:.2f}, f = {charge_points / data_time[-1]:.2f}\n')
    settings.write(f'Points on charge: {charge_points}\n')
    print(f'Points on charge: {charge_points}')

    GPIO.output(troyka_pin, 0)

    while (voltage > DISCHARGED_VOLTAGE):
        # print(voltage)

        data_time.append(time.time() - start_time)
        data_voltage.append(voltage)
        showVoltage(voltage)
        time.sleep(0.2)

        voltage = getVoltage()
        GPIO.output(dac_pins, 0)


    print(f'Experiment ended. Total time: {data_time[-1]:.2f}')
    discharge_points = len(data_time) - charge_points
    settings.write(f'T = {data_time[-1] / discharge_points}, f = {discharge_points / data_time[-1]}\n')
    settings.write(f'Points on discharge: {discharge_points}\n')
    print(f'T = {data_time[-1] / discharge_points}, f = {discharge_points / data_time[-1]}')
    print(f'Points on charge: {discharge_points}')

finally:
    GPIO.output(led_pins, 0)
    GPIO.output(dac_pins, 0)
    GPIO.output(troyka_pin, 0)
    GPIO.cleanup()

    
totalPoints = len(data_voltage)

settings.write(f"ADC precision: {BASE_VOLTAGE/256} V\n")

settings.close()

with (open("data.txt", "w") ) as file:
    for i in range(totalPoints):
        file.write(f'{data_time[i]} {data_voltage[i]}\n')

plt.plot(data_time, data_voltage)
plt.show()