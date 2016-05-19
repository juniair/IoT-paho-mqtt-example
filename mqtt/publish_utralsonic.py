import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time

distance = None
trig_pin = 13
echo_pin = 19

# GPIO 핀 초기화
def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(trig_pin, gpio.OUT)
    gpio.setup(echo_pin, gpio.IN)

# 초음파 센서 처리 함수
# 예제와 동일
def run():
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

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
 
    print "Distance : ", distance, "cm"


client = mqtt.Client("temp_publish")
client.connect("127.0.0.1", 1883)
client.loop_start()
try:
    init_gpio()
    while True:
        run()
        """
             초음파 거리를 'environment.ultrasonic'이라는 topic으로
             데이터를 전송한다.
        """
        client.publish('environment/ultrasonic', distance)
        
        # 0.5동안 대기한다.
        time.sleep(0.5)
        
except KeyboardInterrupt:
    client.loop_stop()
    gpio.cleanup()
