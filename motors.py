from time import sleep

sleep(10)

f = open("/boot/tempreadings.txt", "w")

f.write("Starting rover program\n")


import RPi.GPIO as GPIO

motor1f = 21
motor1r = 22
motor2f = 23
motor2r = 24

led = 25

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1f, GPIO.OUT)
GPIO.setup(motor1r, GPIO.OUT)
GPIO.setup(motor2f, GPIO.OUT)
GPIO.setup(motor2r, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)


GPIO.output(motor1f, GPIO.LOW)
GPIO.output(motor1r, GPIO.LOW)
GPIO.output(motor2f, GPIO.LOW)
GPIO.output(motor2r, GPIO.LOW)
GPIO.output(led, GPIO.LOW)


sleep(5)


import os
import glob

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def temperature():
    f.write("Getting temperature\n")
    c = read_temp()
    a = 22
    if c > a:
        GPIO.output(led, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.LOW)
    f.write("Temperature is: " + str(c) + "\n")


def forwards():
    f.write("Moving forwards\n")
    GPIO.output(motor1f, GPIO.HIGH)
    GPIO.output(motor2f, GPIO.HIGH)
    sleep(3)
    GPIO.output(motor1f, GPIO.LOW)
    GPIO.output(motor2f, GPIO.LOW)
    temperature()
    sleep(0.5)


def turnLeft():
    f.write("Turning Left\n")
    GPIO.output(motor1f, GPIO.HIGH)
    GPIO.output(motor2r, GPIO.HIGH)
    sleep(3)
    GPIO.output(motor2r, GPIO.LOW)
    GPIO.output(motor1f, GPIO.LOW)
    sleep(0.5)


def turnRight():
    f.write("Turning Right\n")
    GPIO.output(motor1r, GPIO.HIGH)
    GPIO.output(motor2f, GPIO.HIGH)
    sleep(3)
    GPIO.output(motor2f, GPIO.LOW)
    GPIO.output(motor1r, GPIO.LOW)
    sleep(0.5)


f.write("Motor control\n")
for i in range(10):

    for x in range(10):
        forwards()

    turnLeft()
    forwards()
    turnLeft()

    for z in range(10):
        forwards()

    turnRight()
    forwards()
    turnRight()


turnRight()
turnRight()


for v in range(20):
    forwards()


f.write("Finished\n")


GPIO.output(motor1f, GPIO.LOW)
GPIO.output(motor1r, GPIO.LOW)
GPIO.output(motor2f, GPIO.LOW)
GPIO.output(motor2r, GPIO.LOW)
GPIO.output(led, GPIO.LOW)


f.close()
