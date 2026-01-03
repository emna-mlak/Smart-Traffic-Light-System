import os
import time

# OpenCV import (ok même en headless, tant qu'on n'utilise pas imshow)
import cv2

from scripts import gpio_controller as gpio
from scripts.vision_detector import run_detector


def is_headless() -> bool:
    v = os.getenv("SMARTTRAFFIC_HEADLESS", "").strip().lower()
    return v in ("1", "true", "yes", "y", "on")


def main():
    headless = is_headless()
    print(f"[CTRL] SMARTTRAFFIC_HEADLESS={headless}")

    # Setup GPIO (feux)
    gpio.setup()

    # Lancer vision (generator)
    # NOTE: run_detector() yield (annotated_frame, counts)
    try:
        for annotated, counts in run_detector():
            # Affichage console
            print(f"[COUNTS] {counts}")

            # Ici tu branches ta logique de décision (si tu as une fonction dédiée)
            # Exemple possible (à adapter selon ton gpio_controller.py):
            # gpio.apply_counts(counts)  # si tu l'as
            # Sinon tu gardes juste les prints pour l’instant.

            # Si pas headless, on affiche la fenêtre
            if not headless:
                try:
                    cv2.imshow("SmartTraffic - 4ways", annotated)
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27:  # ESC
                        print("[CTRL] ESC -> stop")
                        break
                except cv2.error as e:
                    print(f"[CTRL] OpenCV GUI error -> bascule headless: {e}")
                    headless = True

            # petit sleep pour éviter 100% CPU si besoin
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\n[CTRL] Ctrl+C -> stop")

    finally:
        # IMPORTANT: ne pas appeler destroyAllWindows en headless
        if not headless:
            try:
                cv2.destroyAllWindows()
            except cv2.error:
                pass

        # Optionnel: éteindre les feux à la fin si tu as une fonction
        try:
            gpio.all_red()  # si tu l'as
        except Exception:
            pass


if __name__ == "__main__":
    main()
