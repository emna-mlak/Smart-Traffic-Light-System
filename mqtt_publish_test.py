# scripts/mqtt_publish_test.py
import time
import random
from mqtt_service import connect, disconnect, publish_counts, publish_state

def main():
    connect()
    print("[PUB] Envoi de 5 messages de test...")

    try:
        for t in range(5):
            ns = max(0, int(random.gauss(5, 1.0)))
            ew = max(0, int(random.gauss(2, 0.7)))

            publish_counts(ns, ew, source="sim-dev")

            axis = "NS" if t % 2 == 0 else "EW"
            phase = "GREEN"
            ns_light, ew_light = ( "Vert", "Rouge" ) if axis == "NS" else ( "Rouge", "Vert" )

            publish_state(axis, phase, ns_light, ew_light)

            print(f"[PUB] t={t}s  ns={ns} ew={ew} axis={axis}")
            time.sleep(1)

    finally:
        disconnect()

if __name__ == "__main__":
    main()
