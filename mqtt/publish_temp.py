import paho.mqtt.client as mqtt
import dht11
import RPi.GPIO as gpio
import time
import datetime

instance = dht11.DHT11(pin = 12)
result = None

#GPIO 핀 설정
def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

#온도 센서 실행
def run():
    global result
    result = instance.read()
    """"
         유효한 값이 들어온 경우 해당 온도를 출력하고 True를 반환하고
         유효한 값이 없으면 False를 반환한다.
    """"
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
