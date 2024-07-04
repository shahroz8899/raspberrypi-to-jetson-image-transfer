# Raspberrypi-to-jetson-nano-image-transfer
This repository contains a Python script that captures images using a webcam connected to a Raspberry Pi and transfers them to a specified directory on a Jetson Nano device over SSH using Paramiko.

Sure! Below is a detailed explanation on how to set up the system to capture images using a Raspberry Pi and transfer them to a Jetson Nano. This includes hardware and software setup, installation of necessary dependencies, and running the provided Python script.

### 1. Hardware Setup

#### Raspberry Pi
- A Raspberry Pi (any model with a USB port)
- A USB webcam compatible with the Raspberry Pi
- A microSD card with Raspberry Pi OS installed
- Power supply for the Raspberry Pi
- Network connection (Ethernet or Wi-Fi)

#### Jetson Nano
- A Jetson Nano
- A microSD card with the Jetson Nano OS installed
- Power supply for the Jetson Nano
- Network connection (Ethernet or Wi-Fi)

### 2. Software Setup

#### On the Raspberry Pi

1. **Install Raspberry Pi OS**:
   - Follow the official guide to install Raspberry Pi OS on your microSD card: [Raspberry Pi OS Installation Guide](https://www.raspberrypi.org/documentation/installation/installing-images/).

2. **Update and Upgrade the System**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Install `fswebcam`**:
   ```bash
   sudo apt install fswebcam
   ```

4. **Install Python and `paramiko`**:
   ```bash
   sudo apt install python3-pip
   pip3 install paramiko
   ```

5. **Ensure SSH is Enabled**:
   - You can enable SSH via `raspi-config`:
     ```bash
     sudo raspi-config
     ```
   - Navigate to `Interfacing Options` > `SSH` and enable it.

6. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/raspberrypi-to-jetson-image-transfer.git
   cd raspberrypi-to-jetson-image-transfer
   ```

#### On the Jetson Nano

1. **Install Jetson Nano OS**:
   - Follow the official guide to install Jetson Nano OS on your microSD card: [Jetson Nano Installation Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit).

2. **Ensure SSH is Enabled**:
   - SSH is usually enabled by default on the Jetson Nano, but you can ensure it's running with:
     ```bash
     sudo systemctl status ssh
     ```
   - If not running, enable and start the SSH service:
     ```bash
     sudo systemctl enable ssh
     sudo systemctl start ssh
     ```

### 3. Script Configuration

Modify the `image_capture.py` script with your specific configuration:

- `hostname` should be the IP address of the Jetson Nano.
- `username` should be the username on the Jetson Nano.
- `password` should be the password for the user on the Jetson Nano.
- `remote_directory` should be the path where you want to save the images on the Jetson Nano.

Here is the final script:

```python
import os
import paramiko
import time
import logging

def capture_image(image_path):
    try:
        os.system(f'fswebcam -r 1280x720 --no-banner {image_path}')
        logging.info(f"Image captured and saved to {image_path}")
    except Exception as e:
        logging.error(f"Failed to capture image: {e}")

def send_image(image_path, remote_directory, hostname, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        
        sftp = ssh.open_sftp()
        
        # Construct remote path without 'Raspberrypi5' in the filename
        filename = os.path.basename(image_path)
        remote_path = f"{remote_directory}/{filename}"
        
        sftp.put(image_path, remote_path)
        sftp.close()
        ssh.close()
        logging.info(f"Image sent to {hostname}:{remote_path}")
    except paramiko.AuthenticationException:
        logging.error("Authentication failed, please verify your credentials")
    except paramiko.SSHException as sshException:
        logging.error(f"Unable to establish SSH connection: {sshException}")
    except Exception as e:
        logging.error(f"Failed to send image: {e}")

def get_next_image_number(counter_file):
    try:
        with open(counter_file, 'r') as file:
            number = int(file.read().strip())
    except FileNotFoundError:
        number = 1
    return number

def update_image_number(counter_file, number):
    with open(counter_file, 'w') as file:
        file.write(str(number))

if __name__ == "__main__":
    logging.basicConfig(filename='image_capture.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')

    counter_file = "image_counter.txt"
    remote_directory = "/#/#/#/#/"  # Update to Jetson Nano's directory
    hostname = "####"  # Jetson Nano's IP address
    username = "##"
    password = "##@"  # Replace with your actual password
    
    while True:
        try:
            image_number = get_next_image_number(counter_file)
            image_path = f"image_{image_number:04d}.jpg"
            
            capture_image(image_path)
            send_image(image_path, remote_directory, hostname, username, password)
            
            image_number += 1
            update_image_number(counter_file, image_number)
            
            time.sleep(10)  # Take a picture every 10 seconds (for testing)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt detected. Stopping the script.")
            break
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            time.sleep(60)  # Wait before retrying after an error
```

### 4. Running the Script

1. **Navigate to the script directory**:
   ```bash
   cd raspberrypi-to-jetson-image-transfer
   ```

2. **Run the script**:
   ```bash
   python3 image_capture.py
   ```

### 5. Verifying the Setup

- Ensure the webcam is working and the Raspberry Pi can capture images.
- Ensure the SSH connection between the Raspberry Pi and Jetson Nano is working.
- Check the `image_capture.log` file for any errors or logs.

### 6. Pushing to GitHub

1. **Initialize the repository (if not done already)**:
   ```bash
   git init
   ```

2. **Add files to the repository**:
   ```bash
   git add .
   ```

3. **Commit the files**:
   ```bash
   git commit -m "Initial commit"
   ```

4. **Add the remote repository**:
   ```bash
   git remote add origin https://github.com/your-username/raspberrypi-to-jetson-image-transfer.git
   ```

5. **Push the changes to GitHub**:
   ```bash
   git push -u origin master
   ```

### Final Notes

- Ensure the Raspberry Pi and Jetson Nano are on the same network.
- Use a strong password for SSH connections.
- Adjust the image capture interval as needed (currently set to 10 seconds for testing).






