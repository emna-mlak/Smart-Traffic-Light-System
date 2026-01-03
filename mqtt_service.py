# scripts/mqtt_service.py
import json
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "10.42.0.1"   # plus tard: IP_du_Raspberry
BROKER_PORT = 1883

_client = None

def connect():
    """Connexion au broker MQTT + démarrage de la boucle réseau."""
    global _client
    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                          client_id="smarttraffic-dev",
                          clean_session=True)
    _client.connect(BROKER_HOST, BROKER_PORT, keepalive=30)
    _client.loop_start()

    # petit heartbeat
    publish("smarttraffic/heartbeat", {
        "ts": int(time.time()),
        "status": "online",
        "who": "dev-mac"
    }, retain=True)
    print("[MQTT] Connecté à", BROKER_HOST, BROKER_PORT)

def disconnect():
    """Arrêt propre."""
    global _client
    if _client is None:
        return
    publish("smarttraffic/heartbeat", {
        "ts": int(time.time()),
        "status": "offline",
        "who": "dev-mac"
    }, retain=True)
    time.sleep(0.2)
    _client.loop_stop()
    _client.disconnect()
    _client = None
    print("[MQTT] Déconnecté")

def publish(topic: str, payload, qos: int = 0, retain: bool = False):
    """Publie un dict ou une string sur un topic."""
    global _client
    if _client is None:
        raise RuntimeError("MQTT non connecté. Appelle connect() d'abord.")
    if not isinstance(payload, str):
        payload = json.dumps(payload, ensure_ascii=False)
    _client.publish(topic, payload=payload, qos=qos, retain=retain)

def publish_counts(ns: int, ew: int, source: str = "sim"):
    publish("smarttraffic/counts", {
        "ts": int(time.time()),
        "ns": ns,
        "ew": ew,
        "source": source,
    })

def publish_state(axis: str, phase: str, ns_light: str, ew_light: str):
    publish("smarttraffic/state", {
        "ts": int(time.time()),
        "axis": axis,
        "phase": phase,
        "ns_light": ns_light,
        "ew_light": ew_light,
    })
