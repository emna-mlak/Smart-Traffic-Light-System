import os
import time
import cv2
import numpy as np
import requests
from ultralytics import YOLO

# IMPORTANT:
# - Lance ce module avec: python3 -m scripts.vision_detector
# - Sinon les imports peuvent casser (ModuleNotFoundError: config)
try:
    from config import MODEL_PATH, ESP_URL, TARGET_CLASSES, ROIS, USE_ESP, CAMERA_SOURCE
except Exception:
    # fallback si ton config n'a pas USE_ESP / CAMERA_SOURCE
    from config import MODEL_PATH, ESP_URL, TARGET_CLASSES, ROIS
    USE_ESP = True
    CAMERA_SOURCE = None


# -----------------------------
# Utils ROI
# -----------------------------
def point_in_roi(cx: int, cy: int, roi):
    x1, y1, x2, y2 = roi
    return x1 <= cx <= x2 and y1 <= cy <= y2


def draw_rois(img, rois: dict):
    # Dessiner ROIs pour debug (sur image annotée)
    for lane, (x1, y1, x2, y2) in rois.items():
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)
        cv2.putText(
            img,
            lane,
            (x1 + 5, y1 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
    return img


# -----------------------------
# Capture frame (ESP ou caméra USB)
# -----------------------------
def fetch_esp_frame(timeout=2.0):
    r = requests.get(ESP_URL, timeout=timeout)
    r.raise_for_status()
    data = np.frombuffer(r.content, dtype=np.uint8)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return frame


def open_local_camera(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la caméra source={source}")
    return cap


# -----------------------------
# Core detector generator
# -----------------------------
def run_detector(
    show_window: bool = True,
    force_size=(640, 480),          # IMPORTANT: ROIs sont en 640x480
    print_every: float = 0.5,       # afficher counts toutes les X secondes
    save_debug: bool = False,       # sauver des frames annotées
    save_every_n: int = 30          # 1 image toutes les N itérations
):
    """
    Generator: yield (annotated_frame, counts)
    - annotated_frame: image BGR annotée
    - counts: dict par voie (north/east/south/west)
    """

    # Headless: si SMARTTRAFFIC_HEADLESS=1 => show_window = False
    headless_env = os.getenv("SMARTTRAFFIC_HEADLESS", "0").strip()
    if headless_env in ("1", "true", "True", "yes", "YES"):
        show_window = False

    os.makedirs("logs", exist_ok=True)
    if save_debug:
        os.makedirs("logs/frames", exist_ok=True)

    print("[VISION] Démarrage vision_detector (ESC pour quitter)")
    print(f"[VISION] USE_ESP={USE_ESP}")
    print(f"[VISION] ESP_URL={ESP_URL if USE_ESP else None}")
    print(f"[VISION] CAMERA_SOURCE={CAMERA_SOURCE if not USE_ESP else None}")
    print(f"[VISION] MODEL_PATH={MODEL_PATH}")
    print(f"[VISION] TARGET_CLASSES={TARGET_CLASSES}")
    print(f"[VISION] ROIS={ROIS}")
    print(f"[VISION] show_window={show_window}")
    print(f"[VISION] force_size={force_size}")

    # Charger modèle
    model = YOLO(MODEL_PATH)

    cap = None
    if not USE_ESP:
        cap = open_local_camera(CAMERA_SOURCE if CAMERA_SOURCE is not None else 0)

    last_print = 0.0
    i = 0

    try:
        while True:
            # 1) Lire une frame
            try:
                if USE_ESP:
                    frame = fetch_esp_frame()
                else:
                    ok, frame = cap.read()
                    if not ok:
                        frame = None
            except Exception as e:
                print(f"[VISION][FRAME ERR] {e}")
                time.sleep(0.3)
                continue

            if frame is None:
                time.sleep(0.1)
                continue

            # 2) Normaliser taille (SUPER IMPORTANT pour que ROIs soient corrects)
            if force_size is not None:
                try:
                    frame = cv2.resize(frame, force_size)
                except Exception as e:
                    print(f"[VISION][RESIZE ERR] {e}")
                    continue

            # 3) Inference YOLO
            if TARGET_CLASSES is None:
                results = model(frame, verbose=False)
            else:
                results = model(frame, classes=TARGET_CLASSES, verbose=False)


            # 4) Comptage par ROI
            counts = {k: 0 for k in ROIS.keys()}

            if boxes is not None and len(boxes) > 0:
                for b in boxes:
                    x1, y1, x2, y2 = b.xyxy[0].tolist()
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    lane_found = None
                    for lane, roi in ROIS.items():
                        if point_in_roi(cx, cy, roi):
                            counts[lane] += 1
                            lane_found = lane
                            break

            # 5) Image annotée
            try:
                annotated = results[0].plot()
            except Exception:
                annotated = frame.copy()

            annotated = draw_rois(annotated, ROIS)

            # 6) Affichage / Headless
            now = time.time()
            if now - last_print >= print_every:
                print(f"[COUNTS] {counts}")
                last_print = now

            if show_window:
                # Ne marche PAS en headless, donc show_window=False sinon crash
                cv2.imshow("SmartTraffic - Vision", annotated)
                if (cv2.waitKey(1) & 0xFF) == 27:
                    print("[VISION] ESC détecté -> arrêt")
                    break

            # 7) Debug save
            if save_debug and (i % save_every_n == 0):
                ts = int(time.time() * 1000)
                cv2.imwrite(f"logs/frames/frame_{ts}.jpg", annotated)

            i += 1

            # 8) Yield vers run_controller
            yield annotated, counts

    finally:
        if cap is not None:
            cap.release()
        if show_window:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass


# -----------------------------
# CLI / test direct
# -----------------------------
def main():
    # main = test local, sans controller
    # headless possible via SMARTTRAFFIC_HEADLESS=1
    for _annotated, _counts in run_detector(show_window=True):
        pass


if __name__ == "__main__":
    main()
