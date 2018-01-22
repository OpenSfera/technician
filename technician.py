import os,signal,sys
import paho.mqtt.client as mqtt
import time
import json
import sferacommands as SC
import sferaconfig



def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
def on_exit(sig, func=None):
    print("exit handler triggered")
    sys.exit(1)
if __name__ == "__main__":
    set_exit_handler(on_exit)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("local/technician")


def on_message(client, userdata, msg):
    command = str(msg.payload.decode('UTF-8'))
    try:
        func = getattr(SC, command)
    except AttributeError:
        print ("command '"+command+"' not found")
    else:
        func()
        data = {
            "event": "sfera_commands",
            "data": command
        }
        client.publish("local/status", json.dumps(data))

def broadcast_status(client):
    data = {
        "event": "sfera_status",
        "data": {
            "lights": SC.lights_status(),
            "fan": SC.fan_status(),
            "t1": SC.t1_status(),
            "h1": SC.h1_status()
        }
    }
    client.publish("local/status", json.dumps(data))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        now=time.strftime("%Y-%m-%d %H:%M")
        print("Unexpected disconnection."+now)


SC.initialize()

client = mqtt.Client(client_id="technician")

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)

client.loop_start()
broadcast_time = sferaconfig.getConfig("technician_broadcast_time")
if broadcast_time == None:
    broadcast_time = 10
while True:
    broadcast_status(client)
    time.sleep( broadcast_time )
