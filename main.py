# Importing necessary libraries
import base64
import os
import configparser
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess

# Initialize Tkinter and hide the main window
Tk().withdraw()

# Open Finder/File Explorer for file selection
image_path = askopenfilename(title="Выберите изображение для кодирования", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])

# Check if a file was selected
if not image_path:
    print("Файл не выбран!")
else:
    # Define the config directory and file path
    config_dir = os.path.expanduser('~/.config/base64')
    config_file_path = os.path.join(config_dir, 'image_encoder_config.ini')
    config = configparser.ConfigParser()

    # Create config directory if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Check if config file exists
    if os.path.exists(config_file_path):
        config.read(config_file_path)
        output_dir = config['Settings']['output_dir']
        notifications_enabled = config.getboolean('Settings', 'notifications_enabled', fallback=True)
    else:
        # Ask user to select the output directory
        output_dir = askdirectory(title="Выберите папку для сохранения закодированного файла")
        if not output_dir:
            print("Папка не выбрана!")
            exit()

        # Save the selected directory to config file
        config['Settings'] = {'output_dir': output_dir, 'notifications_enabled': 'true'}
        with open(config_file_path, 'w') as config_file:
            config.write(config_file)
        notifications_enabled = True

    # Get the base name of the image file and create the output file path
    image_name = os.path.basename(image_path)
    output_file_name = os.path.splitext(image_name)[0] + '.txt'
    output_file_path = os.path.join(output_dir, output_file_name)

    # Read and encode the image file in Base64
    with open(image_path, 'rb') as image_file:
        encoded_content = base64.b64encode(image_file.read()).decode('utf-8')

    # Save the Base64 content to a .txt file in the selected directory
    with open(output_file_path, 'w') as output_file:
        output_file.write(encoded_content)

    print(f"Base64-кодированный файл сохранен: {output_file_path}")

    # Show notification if enabled
    if notifications_enabled:
        subprocess.run(["osascript", "-e", f'display notification "Base64-кодированный файл сохранен: {output_file_path}" with title "Уведомление"'])
