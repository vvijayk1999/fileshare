import json
import paho.mqtt.client as mqtt
import sqlite3


#----------------------------------------------------------------------
broker_address= "192.168.31.15"
port = 1883 #portNumber
#user = "ymcnjbxy"
#password = "1pY8vciDPRor"
topic = "server"
#----------------------------------------------------------------------
    
filestatus = False
def connect():
    global conn
    conn = sqlite3.connect('parkingsystem.db')
    global c
    c = conn.cursor()
    
def Values(message):
    parsed_json =(json.loads(message))
    place=str(parsed_json[_]['place'])
    occupied=str(parsed_json[_]['occupied'])
    arrival_time=str(parsed_json[_]['arrival_time'])
    departure_time=str(parsed_json[_]['departure_time'])
    v_id=str(parsed_json[_]['v_id'])
    color=str(parsed_json[_]['color'])
    model=str(parsed_json[_]['model'])
    c.execute("INSERT INTO Data VALUES('"+place+"','"+occupied+"','"+arrival_time+"','"+departure_time+"','"+v_id+"','"+color+"','"+model+"')")
    print("row inserted") 

def CloseConnection():
    conn.close()

 # The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(message)
    Values(message)
    


if filestatus:
    connect()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client = mqtt.Client('parkingsystem')
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port, 60)
#client.username_pw_set(user,password)
client.loop_forever()


  