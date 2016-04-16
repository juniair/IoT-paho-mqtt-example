import paho.mqtt.client as mqtt
import random, time

client = mqtt.Client("humidity_publish")
client.connect("127.0.0.1", 1883)
client.loop_start()


while True:
    humidity = random.uniform(0.3, 0.95)
    print "Humidity : " + str(round(humidity*100, 2))
    client.publish("environment/humidity", humidity)
    time.sleep(2)
