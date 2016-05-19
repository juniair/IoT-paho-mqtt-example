import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

temp = wave = 0
isGetTemp = isGetWave = False
"""
    GREEN LED: GPIO #16
    YELLOW LED: GPIO #20
    RED LED: GPIO #21
"""
LED = (16, 20, 21)

# GPIO 초기화
def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    for pin in LED:
        gpio.setup(pin, gpio.OUT)

def select_led(distance):
    """
        LED 값 결정 함수
        해당 함수의 인자인 distance를 활용하여
        100cm 이상이면 GREEN LED를 ON, 나머지 OFF
        30cm 이상 100cm 미만이면 YELLOW LED를 ON, 나머지 OFF
        30cm 미만이면 RED LED를 ON, 나머지 OFF
        로 결정한다.
    """
    if distance >= 100.0:
        set_blink(LED, (True, False, False))
    elif 30.0 <= distance and distance < 100.0:
        set_blink(LED, (False, True, False))
    else:
        set_blink(LED, (False, False, True))


def set_blink(LED, values):
    """
        LED ON/OFF 함수
        인자인 LED를 해당 value와 매칭 시켜서 On/Off를 함
    """
    for index in range(0, 3):
        gpio.output(LED[index], values[index])


def on_connect(client, userdata, flags, rc):
    """
        subscribe를 broket에 연결하는 함수
        해당 subscribe는 연결에 성공하면
        'environment/temperature' 와 'environment/ultrasonic'를 topic으로
        보내는 publish의 메시지만 받는다.
    """
    if rc == 0:
        client.subscribe( [("environment/temperature",0), ("environment/ultrasonic",0)] )
        print "Connect OK!"
    else:
        print "Connect fefused"

def on_message(client, userData, message):
    global temp, wave, isGetTemp, isGetWave
    
    """
        message.topic에 따라 값을 각각에 맞는 변수에 저장을 하고
        해당 topic이 왔다는 것을 기억해주는 변수에 True로 설정한다.
    """
    if message.topic == 'environment/ultrasonic':     
        wave = float(message.payload)
        isGetWave = True
    elif message.topic == 'environment/temperature':
        temp = float(message.payload)
        isGetTemp = True
    else:
        pass
    
    """
        초음파센서에대한 topic 왔을 경우
        온도 센서에 대한 topic이 왔는지 확인을 한다.
        온도 센서에 데이터 값이 20도 이하인 경우 wave 값에 대한 LED 상태를 바꿔준다.
        20도를 넘는 경우 모든 LED를 OFF한다.
        만약 온도센서 데이터가 안왔을 경우 이전 온도데이터로 위에와 동일하게 처리한다.
    """
    if isGetWave:
        if isGetTemp: # True && True
        
            if temp <= 20:
                select_led(wave)
            else: 
                set_Blink(LED, (False, False, False))
            isGetTemp = False
        else:
            if temp <= 20:
                select_led(wave)
            else:
                set_Blink(LED, (False, False, False))

        print "utrasonic wave: ", wave
        print "Last vaild temperature: ", temp, " C"
        print
        
        isGetWave = False
    


try:
    init_gpio()
    client = mqtt.Client("Subscribe_Client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()
except KeyboardInterrupt:
    client.loop_stop()
    gpio.cleanup()

