import paho.mqtt.client as mqtt
import dht11
import RPi.GPIO as gpio
import time
import datetime

instance = dht11.DHT11(pin = 12)
result = None

def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

def run():
    global result
    result = instance.read()

    if result.is_valid():
        print "Last valid input: " + str(datetime.datetime.now())
        print "Temperature: %d C" % result.temperature
        print
        return True
    else:
        return False

client = mqtt.Client("temp_publish")
client.connect("127.0.0.1", 1883)

try:
    init_gpio()
    client.loop_start()
    while True:
        if run():
            client.publish("environment/temperature", result.temperature)
            time.sleep(1)

except KeyboardInterrupt:
    client.loop_stop()
    gpio.cleanup()
