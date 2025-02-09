# 🚗 Brain-Computer Interface (BCI) Controlled Car  

## 📌 Overview  
The **BCI-Controlled Car** is an innovative project that enables users to control a car using brain signals. By utilizing **Electroencephalography (EEG) data**, machine learning, and IoT integration, this project demonstrates a hands-free approach to driving automation.  

## 🎯 Features  
✅ **Mind-Controlled Navigation** – Use EEG signals to control the car's movement.  
✅ **Real-Time Signal Processing** – Process and analyze brain waves in real-time.  
✅ **Wireless Communication** – Send commands to the car over Bluetooth/Wi-Fi.  
✅ **ML-Based Signal Interpretation** – Classify EEG signals for accurate control.  
✅ **Obstacle Detection** – Prevent collisions using ultrasonic or LiDAR sensors.  

## 🛠️ Tech Stack  
- **Hardware:** EEG Headset (e.g., OpenBCI, Muse, Neurosky), Raspberry Pi / Arduino, Motor Driver  
- **Software:** Python, OpenBCI SDK, TensorFlow / PyTorch, Flask, Bluetooth / Wi-Fi Communication  
- **ML Models:** SVM, CNNs, or LSTMs for brainwave classification  
- **Protocols:** MQTT / WebSockets for data transmission  

## ⚙️ System Architecture  
1️⃣ **EEG Headset** captures brain signals.  
2️⃣ **Signal Processing** extracts relevant features.  
3️⃣ **ML Model** classifies brain signals into control commands.  
4️⃣ **Microcontroller** (Raspberry Pi / Arduino) sends signals to motors.  
5️⃣ **Car Moves** based on the decoded brain signals.  

## 🚀 Installation & Setup  
### **1. Clone the Repository**  
```sh
git clone https://github.com/Ishita-2611/NeuroDrive_Project.git
cd NeuroDrive_Project
