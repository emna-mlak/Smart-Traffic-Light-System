# scripts/mqtt_subscribe.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("[SUB] Connecté au broker, rc =", rc)
    client.subscribe("smarttraffic/#")

def on_message(client, userdata, msg):
    try:
        print(f"[SUB] {msg.topic}: {msg.payload.decode()}")
    except Exception:
        print(f"[SUB] {msg.topic}: <payload binaire {len(msg.payload)} octets>")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="smarttraffic-sub")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 30)
client.loop_forever()
