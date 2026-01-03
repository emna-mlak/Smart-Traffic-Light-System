from time import sleep
from gpiozero import LED

from ..config import LIGHTS, YELLOW_TIME, ALL_RED_TIME

_leds = {}

def setup():
    global _leds
    for lane, pins in LIGHTS.items():
        _leds[lane] = {
            "R": LED(pins["R"]),
            "Y": LED(pins["Y"]),
            "G": LED(pins["G"]),
        }
    all_red()

def all_red():
    for lane in _leds:
        _leds[lane]["R"].on()
        _leds[lane]["Y"].off()
        _leds[lane]["G"].off()

def set_lane_state(lane: str, state: str):
    all_red()
    sleep(ALL_RED_TIME)

    if state == "GREEN":
        _leds[lane]["R"].off()
        _leds[lane]["Y"].off()
        _leds[lane]["G"].on()
    elif state == "YELLOW":
        _leds[lane]["R"].off()
        _leds[lane]["G"].off()
        _leds[lane]["Y"].on()
    else:
        _leds[lane]["R"].on()
        _leds[lane]["Y"].off()
        _leds[lane]["G"].off()

def demo():
    setup()
    print("ALL_RED")
    sleep(1)

    print("north -> GREEN")
    set_lane_state("north", "GREEN")
    sleep(2)

    print("north -> YELLOW")
    set_lane_state("north", "YELLOW")
    sleep(YELLOW_TIME)

    print("east -> GREEN")
    set_lane_state("east", "GREEN")
    sleep(2)

    print("east -> YELLOW")
    set_lane_state("east", "YELLOW")
    sleep(YELLOW_TIME)

    print("ALL_RED")
    all_red()
    print("Fin du test.")

if __name__ == "__main__":
    demo()
