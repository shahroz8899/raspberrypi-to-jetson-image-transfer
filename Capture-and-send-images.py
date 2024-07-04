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
    remote_directory = "/#/#/#/##/"  # Update to Jetson Nano's directory
    hostname = "#####"  # Jetson Nano's IP address
    username = "shahroz" # Jetson Nano's username
    password = "####"  # Replace with your actual password
    
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
