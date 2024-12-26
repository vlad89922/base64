
# Base64 Image Encoder

This Python script allows users to select an image file, encode it in Base64, and save the encoded content to a text file. The script uses Tkinter for file selection dialogs and stores configuration settings in an INI file.

## Features

- Allows users to select an image file through a graphical file dialog.
- Encodes the selected image in Base64 format.
- Saves the encoded content to a text file.
- Remembers the output directory for future runs using a configuration file.
- Displays a macOS notification upon successful encoding (if enabled).

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations on macOS)
- macOS (for the notification feature)

## Usage

1. Run the script.
2. Select an image file when prompted.
3. If running for the first time, select an output directory for saving the encoded text file.
4. The script will encode the image and save the Base64 content to a text file in the selected directory.
5. A macOS notification will be displayed upon successful encoding (if enabled).

```python
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

    print(f"Base64-encoded file saved: {output_file_path}")

    # Show notification if enabled
    if notifications_enabled:
        subprocess.run(["osascript", "-e", f'display notification "Base64-encoded file saved: {output_file_path}" with title "Notification"'])
```

### Example

Run the script and follow the prompts to select an image file and output directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Feel free to customize this description further based on your specific needs and preferences.
