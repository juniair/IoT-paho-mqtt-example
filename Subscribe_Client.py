import paho.mqtt.client as mqtt


# Override on_connect.
def on_connect(client, userdata, flags, rc):
    #Check Connect Result.
    if rc == 0:
        print "Connect successful\n\n\n\n"

        # Client allows mutiple topic subscrptions.
        # List of string and interger tuples.
        # tuple first is topic and second is QoSa.
        client.subscribe([("environment/temperature", 0), ("environment/humidity", 0)])
    else:
        print "Connect refused"

# Override on_message.
def on_message(client, userData, message):
    #define T, RH, T_Changed and RH_Changed is gloabla value
    global T, RH, T_Changed, RH_Changed


    #Check Topic
    if message.topic == "environment/temperature":
        T = round(float(message.payload), 2)   # string to float & Second decimal place of rounding
        T_Changed = True #set 'T_Changed' is 'True'
    elif message.topic == "environment/humidity":
        RH = round(float(message.payload), 4)   # string to float & Second decimal place of rounding
        RH_Changed =  True #set 'RH_Changed' is 'True'
    else:
        pass
    #Check whether it has received all of the data
    if T_Changed and RH_Changed:
        # Calculation of the discomfort index & Second decimal place of rounding
        result = round( (((9.0/5.0) * T) - (0.55 * (1.0-RH) * (((9.0/5.0) * T) - 26.0)) + 32.0), 2)
        
        #print Data & Result
        print "Temperature : " + str(T)
        print "Heumidity : " + str(RH*100)
        print "Discomfort Index : " + str(result),
        #Check Level
        if result >= 80:
            print " (Very High)\n"
        elif (75 <= result) and (result < 85):
            print " (High)\n"
        elif (65 <=result) and (result < 75):
            print " (Normal)\n"
        else:
            print " (Low)\n"

        # set T_Changed and RH_Changed is False
        T_Changed = RH_Changed = False 

    else:
        pass


T = RH = 0 #Initialized to '0' the variable.
T_Changed = RH_Changed = False #Initialized to 'False' the variable.


# Create client
# Client name is Subscribe_Client
client = mqtt.Client("Subscribe_Client")
client.on_connect = on_connect
client.on_message = on_message
#client broker is localhost(127.0.0.1)
#client port is 1883
#Maximum of communication time that is acceptable to the broker is 60 seconds.
client.connect("localhost", 1883, 60)

client.loop_forever()
