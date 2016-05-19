import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

temp = wave = 0
isGetTemp = isGetWave = False
LED = (16, 20, 21)

def init_gpio():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    for pin in LED:
        gpio.setup(pin, gpio.OUT)

def select_led(distance):
    if distance >= 100.0:
        set_blink(LED, (True, False, False))
    elif 30.0 <= distance and distance < 100.0:
        set_blink(LED, (False, True, False))
    else:
        set_blink(LED, (False, False, True))


def set_blink(LED, pin):
    for index in range(0, 3):
        gpio.output(LED[index], pin[index])


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe( [("environment/temperature",0), ("environment/ultrasonic",0)] )
        print "Connect OK!"
    else:
        print "Connect fefused"

def on_message(client, userData, message):
    global temp, wave, isGetTemp, isGetWave
    
    if message.topic == 'environment/ultrasonic':     
        wave = float(message.payload)
        isGetWave = True
    elif message.topic == 'environment/temperature':
        temp = float(message.payload)
        isGetTemp = True
    else:
        pass

    if isGetWave:
        if isGetTemp: # True && True

            if temp < 20:
                select_led(wave)
            else: 
                set_Blink(LED, (False, False, False))
        else:
            if temp < 20:
                select_led(wave)
            else:
                set_Blink(LED, (False, False, False))

        print "utrasonic wave: ", wave
        print "Last vaild temperature: ", temp, " C"
        print
    isGetTemp = isGetWave = False


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

