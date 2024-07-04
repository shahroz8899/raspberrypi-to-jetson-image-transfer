# Raspberrypi-to-jetson-nano-image-transfer
This repository contains a Python script that captures images using a webcam connected to a Raspberry Pi and transfers them to a specified directory on a Jetson Nano device over SSH using Paramiko.

**1. Hardware Setup**
**Raspberry Pi**
A Raspberry Pi (any model with a USB port)
A USB webcam compatible with the Raspberry Pi
A microSD card with Raspberry Pi OS installed
Power supply for the Raspberry Pi
Network connection (Ethernet or Wi-Fi)
**Jetson Nano**
A Jetson Nano
A microSD card with the Jetson Nano OS installed
Power supply for the Jetson Nano
Network connection (Ethernet or Wi-Fi)
**2. Software Setup**
**On the Raspberry Pi**
Install Raspberry Pi OS:

Follow the official guide to install Raspberry Pi OS on your microSD card: Raspberry Pi OS Installation Guide.
Update and Upgrade the System:

bash
Copy code
sudo apt update
sudo apt upgrade -y
**Install fswebcam:**

bash
Copy code
sudo apt install fswebcam
**Install Python and paramiko:**

bash
Copy code
sudo apt install python3-pip
pip3 install paramiko
Ensure SSH is Enabled:

You can enable SSH via raspi-config:
bash
Copy code
sudo raspi-config
Navigate to Interfacing Options > SSH and enable it.

**Clone the Repository:**

bash
Copy code
git clone https://github.com/your-username/raspberrypi-to-jetson-image-transfer.git
cd raspberrypi-to-jetson-image-transfer
**On the Jetson Nano**
**Install Jetson Nano OS:**

Follow the official guide to install Jetson Nano OS on your microSD card: Jetson Nano Installation Guide.
Ensure SSH is Enabled:

SSH is usually enabled by default on the Jetson Nano, but you can ensure it's running with:
bash
Copy code
sudo systemctl status ssh
If not running, enable and start the SSH service:
bash
Copy code
sudo systemctl enable ssh
sudo systemctl start ssh
**3. Script Configuration**
Modify the image_capture.py script with your specific configuration:

hostname should be the IP address of the Jetson Nano.
username should be the username on the Jetson Nano.
password should be the password for the user on the Jetson Nano.
remote_directory should be the path where you want to save the images on the Jetson Nano.
