# Smart Traffic Light – IoT Architecture Project

##  Project Context

This project was developed during the laboratory sessions of the course **IoT Architecture**.

### Developed by

* Emna Mlak *

Undergraduate students
**Bachelor in Embedded Systems and Internet of Things (IoT)**

### Supervised by

**Madame.Hanen KARAMTI**
Assistant Professor in Computer Science
Higher Institute of Multimedia Arts of Manouba (ISAMM)
University of Manouba, Tunisia

---

##  Project Title

**Smart Traffic Light: An IoT-Based Intelligent Traffic Management System**

---

##  Project Description

Smart Traffic Light is an intelligent traffic management system based on IoT and Artificial Intelligence principles.
The system aims to improve urban traffic flow by dynamically adapting traffic light phases according to real or simulated traffic conditions.

Using a camera-based perception system, vehicle detection and counting are performed locally on an embedded platform. The processed data are then used to make automatic decisions regarding traffic light control. A web-based dashboard allows supervision, visualization, and system monitoring.

The architecture is modular, scalable, and designed to support both real-time operation and simulation mode for testing and demonstration purposes.

---

##  Problem Statement and Objectives

### Problem Statement

Traditional traffic light systems rely on static timing cycles that do not consider real-time traffic conditions. This leads to:

* traffic congestion,
* increased waiting times,
* inefficient use of road infrastructure,
* higher pollution levels.

### Objectives

The main objectives of this project are:

* to monitor traffic conditions using IoT devices,
* to detect and count vehicles on each road axis,
* to dynamically adapt traffic light states,
* to apply Artificial Intelligence techniques for traffic analysis,
* to design a modular and extensible IoT architecture,
* to provide a supervision interface for monitoring and control.

---

##  System Architecture Overview

The system is structured according to an IoT layered architecture:

* **Perception Layer:** Camera for traffic observation
* **Processing Layer:** Embedded processing and vehicle detection
* **Transport Layer:** MQTT-based communication
* **Application Layer:** Web/Flutter dashboard for supervision
* **Business Layer:** Decision logic for traffic light control

---

##  Requirements

### Hardware Requirements

| Component                                 | Description                       |
| ----------------------------------------- | --------------------------------- |
| Raspberry Pi                              | Edge computing and system control |
| Camera (ESP32-CAM                         | Traffic image acquisition         |
| Traffic light LEDs                        | Simulation of traffic lights      |
| Network (Wi-Fi)                           | Communication between components  |

### Software Requirements

| Software                | Purpose                      |
| ----------------------- | ---------------------------- |
| Python 3                | Core system development      |
| OpenCV                  | Image processing             |
| YOLO (Ultralytics)      | Vehicle detection            |
| MQTT Broker (Mosquitto) | IoT communication            |
| Flutter Web             | Dashboard and user interface |

### Datasets

* Live camera stream (real mode)
* Synthetic or recorded traffic scenarios (simulation mode)

---

##  Instructions for Equipment Installation

### 1. Hardware Setup

* Connect the camera module to the Raspberry Pi.
* Connect LEDs to GPIO pins to simulate traffic lights.
* Ensure network connectivity (Wi-Fi or Ethernet).

### 2. Software Installation

* Install Linux OS on the Raspberry Pi.
* Install Python and required libraries (OpenCV, MQTT, YOLO).
* Set up the MQTT broker.
* Deploy the traffic control and vision scripts.
* Build and deploy the Flutter web dashboard.

### 3. Running the System

* Start the MQTT broker.
* Launch the traffic detection and decision modules.
* Access the dashboard via a web browser.
* Switch between real mode and simulation mode if required.

---

##  Features

* Vehicle detection using computer vision
* Dynamic traffic light control
* Real-time or simulated traffic analysis
* Web-based supervision dashboard
* Modular and scalable IoT architecture

---

##  Future Improvements

* Multi-intersection management
* Traffic prediction using machine learning
* Real-world deployment and validation
* Integration into smart city platforms

---

##  License

This project is developed for academic purposes only.
