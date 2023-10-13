#!/usr/bin/python3

import os
import time
from datetime import datetime
import pyautogui
import keyboard
import hashlib  

# Prompt user to set a save path
save_path = input("Please specify the save path (e.g., '~/Desktop/screenshots'): ")

# Check and create the save path if it doesn't exist
if not os.path.exists(os.path.expanduser(save_path)):  # Make sure to expand the user path
    os.makedirs(os.path.expanduser(save_path))

# Establish initial screenshot timestamp
last_screenshot_time = 0 

# Function to generate MD5 hash
def generate_md5(file_path): 
    hash_md5 = hashlib.md5()  
    with open(file_path, "rb") as f:  
        for chunk in iter(lambda: f.read(4096), b""): 
            hash_md5.update(chunk)  
    return hash_md5.hexdigest() 

def take_screenshot():
    global last_screenshot_time

    current_time = time.time()

    if current_time - last_screenshot_time >= 30:
        for i in range(3, 0, -1):
            print(f"Screenshot capture in {i} seconds")
            time.sleep(1)

        now = datetime.now()
        foldername = now.strftime('%A, %B %d %Y')
        filename = f"{now.strftime('%H%M')}.png"
        file_path = os.path.join(os.path.expanduser(save_path), "screenshots", foldername, filename)

        day_folder_path = os.path.dirname(file_path)
        if not os.path.exists(day_folder_path):
            os.makedirs(day_folder_path)

        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"Screenshot saved at {file_path}")

        md5_hash = generate_md5(file_path)
        hash_filename = f"{now.strftime('%H%M')}.txt"

        # Save hash in a nested 'hashes' folder inside the day folder
        hash_folder_path = os.path.join(day_folder_path, 'hashes')  ###
        if not os.path.exists(hash_folder_path):  ###
            os.makedirs(hash_folder_path)  ###

        hash_file_path = os.path.join(hash_folder_path, hash_filename)  ###
        with open(hash_file_path, 'w') as f:  
            f.write(md5_hash)  
        print(f"MD5 hash saved at {hash_file_path}")  

        last_screenshot_time = current_time 

    else:
        print(f"Wait for at least {30 - (current_time - last_screenshot_time):.2f} seconds before taking another screenshot.")

keyboard.add_hotkey('enter', take_screenshot)
print("Press Enter to take a screenshot. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
