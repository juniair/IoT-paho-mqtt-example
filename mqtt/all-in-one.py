import RPi.GPIO as gpio
import dht11
import time
import datetime

trig_pin = 13
echo_pin = 19
LED = (16, 20, 21)
instance = dht11.DHT11(pin = 12)
#define distance
distance = 0
temperature = 0
def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(trig_pin, gpio.OUT)
    for pin in LED:
        gpio.setup(pin, gpio.OUT)
    gpio.setup(echo_pin, gpio.IN)

def set_blink(LED, pin):    
    for index in range(0, 3):
        gpio.output(LED[index], pin[index]);
        
def select_led(distance):
    if distance >= 100.0:
        set_blink(LED, (True, False, False))
    elif 30.0 <= distance and distance < 100.0:
        set_blink(LED, (False, True, False))
    else:
        set_blink(LED, (False, False, True))
def is_temp(temp):
    return temp < 22

def run_wave():
    global distance
    gpio.output(trig_pin, False)
    time.sleep(1)
    gpio.output(trig_pin, True)
    time.sleep(0.00001)
    gpio.output(trig_pin, False)
        
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()
        
    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_dration = pulse_end - pulse_start
    distance = pulse_dration * 17000
    distance = round(distance, 2)

def run_temp():
    global temperature
    result = instance.read()
    if result.is_valid():
        print "Last valid input: " + str(datetime.datetime.now())
        print "Temperature: %d C" % result.temperature
        
        
        temperature = result.temperature

        if is_temp(temperature):
            return True
        else:
            return False
    else:
        if is_temp(temperature):
            return True
        else:
            return False

        

init_gpio()

try:
    while True:
        run_wave()
        if run_temp():
            print "Distance:", distance, "cm"
            select_led(distance)
        else:
            set_blink(LED, (False, False, False))
except KeyboardInterrupt:
    gpio.cleanup()
