import time
from config import MIN_GREEN, MAX_GREEN

class TrafficController:
    def __init__(self):
        self.current_lane = "north"
        self.last_switch = time.time()

    def choose_lane(self, counts: dict) -> str:
        # voie la plus chargée
        best = max(counts, key=counts.get)

        # si égalité → garder la voie actuelle (stabilité)
        if counts[best] == counts.get(self.current_lane, 0):
            return self.current_lane

        return best

    def can_switch(self) -> bool:
        return (time.time() - self.last_switch) >= MIN_GREEN

    def mark_switch(self):
        self.last_switch = time.time()
