# config.py

# --- Source caméra (ESP32-CAM) ---
USE_ESP = True
ESP_URL = "http://10.42.0.50/capture"   # snapshot JPEG (image)
CAMERA_SOURCE = 0                       # utilisé seulement si USE_ESP = False

# --- Modèle IA ---
MODEL_PATH = "/home/emna/SmartTraffic/models/yolov8n.pt"
TARGET_CLASSES = None

# --- Durées feux (secondes) ---
MIN_GREEN = 8
MAX_GREEN = 25
YELLOW_TIME = 2
ALL_RED_TIME = 1

# --- 4 voies ---
LANES = ["north", "east", "south", "west"]

# GPIO (exemples -> tu modifies selon ton câblage)
LIGHTS = {
    "north": {"R": 17, "Y": 27, "G": 22},
    "east":  {"R": 5,  "Y": 6,  "G": 13},
    "south": {"R": 19, "Y": 26, "G": 21},
    "west":  {"R": 23, "Y": 24, "G": 25},
}

# ROIs (à calibrer selon l'image ESP)
# (x1, y1, x2, y2)
ROIS = {
    "north": (0,   0,   320, 240),
    "east":  (320, 0,   640, 240),
    "south": (0,   240, 320, 480),
    "west":  (320, 240, 640, 480),
}
