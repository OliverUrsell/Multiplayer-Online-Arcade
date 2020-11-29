import paho.mqtt.client as mqtt
import random

from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("check/player")
    client.subscribe("check/player/" + str(name) +str(ranid))
    print("subscribed")
    send_message(client, "check/server", str(name)+str(ranid))

def send_message(client, topic, payload):
    client.publish(topic, payload=payload, qos=1, retain=False)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Convert bits to string and remove b''
    payload = str(msg.payload)[2:-1]
    if msg.topic == "check/player/"+str(name)+str(ranid):
        if payload == "n":
            print("Name Failed")
        else:
            game = payload
            client.subscribe("move/player")
            client.subscribe("move/player/" + str(name))
            print("got name")
            print(name)
            timer = RepeatTimer(1,repeat,args=("bar",))
            timer.start()

def repeat(self):
    send_message(client, "move/server", str(name)+"f")

name = random.randint(100,999)
ranid = random.randint(100,999)

client = mqtt.Client()
client.on_connect = mqtt_on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
