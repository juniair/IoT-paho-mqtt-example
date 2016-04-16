import paho.mqtt.client as mqtt
import random, time

client = mqtt.Client("temperature_publish")
client.connect("127.0.0.1", 1883)
client.loop_start()


while True:
    temperature = random.uniform(20.0, 35.0)
    print "Temperature : " + str(round(temperature,2))
    client.publish("environment/temperature", temperature)
    time.sleep(2)
