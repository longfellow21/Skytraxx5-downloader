import tkinter as tk
from tkinter import ttk, messagebox
import win32api
import os
import urllib.request
import zipfile


def find_drive_letter(device_label):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # Split and remove the empty string at the end

    for drive in drives:
        try:
            volume_info = win32api.GetVolumeInformation(drive)
            if volume_info[0] == device_label:
                return drive
        except Exception as e:
            print(f"Error getting information for drive {drive}: {e}")

    return None

def download_and_extract(url, target_folder):
    try:
        # Download the file
        file_path, _ = urllib.request.urlretrieve(url)

        # Extract the contents to the target folder
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)

        print(f"Download and extraction successful to {target_folder}")
        return True
    except Exception as e:
        print(f"Error downloading or extracting the file: {e}")
        return False

def download_file(url, target_folder):
    try:
        # Download the file
        file_path, _ = urllib.request.urlretrieve(url, os.path.join(target_folder, os.path.basename(url)))
        print(f"Download successful to {file_path}")
        return True
    except Exception as e:
        print(f"Error downloading the file: {e}")
        return False

def start_download_airspaces():
    device_label = "SKYTRAXX"
    drive_letter = find_drive_letter(device_label)

    if drive_letter:
        # Define target folder
        airspaces_folder = os.path.join(drive_letter, "airspaces")

        # Create folder if it doesn't exist
        os.makedirs(airspaces_folder, exist_ok=True)

        # Download airspaces file and extract (if it's a zip file)
        airspaces_url = "https://www.skytraxx.org/skytraxx5/airspaces/world.zip"
        airspaces_success = download_and_extract(airspaces_url, airspaces_folder)

        if airspaces_success:
            messagebox.showinfo("Download Complete", "Airspaces download completed successfully.")
        else:
            messagebox.showerror("Download Error", "An error occurred during the airspaces download.")
    else:
        messagebox.showwarning("Device Not Found", "SKYTRAXX device not found on any drive.")

def start_download_obstacles():
    device_label = "SKYTRAXX"
    drive_letter = find_drive_letter(device_label)

    if drive_letter:
        # Define target folder
        obstacles_folder = os.path.join(drive_letter, "obstacles")

        # Create folder if it doesn't exist
        os.makedirs(obstacles_folder, exist_ok=True)

        # Download obstacles file (no extraction needed)
        obstacles_url = "https://www.skytraxx.org/skytraxx5/obstacles/world.oob"
        obstacles_success = download_file(obstacles_url, obstacles_folder)

        if obstacles_success:
            messagebox.showinfo("Download Complete", "Obstacles download completed successfully.")
        else:
            messagebox.showerror("Download Error", "An error occurred during the obstacles download.")
    else:
        messagebox.showwarning("Device Not Found", "SKYTRAXX device not found on any drive.")

# Create the main window
root = tk.Tk()
root.title("SKYTRAXX Download Tool")
root.geometry("400x200")  # Set the initial size of the window

# Configure a style for the buttons
button_style = ttk.Style()
button_style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10)

# Create and configure the download buttons
download_airspaces_button = ttk.Button(root, text="Download Airspaces", command=start_download_airspaces, style='TButton')
download_airspaces_button.pack(pady=10)

download_obstacles_button = ttk.Button(root, text="Download Obstacles", command=start_download_obstacles, style='TButton')
download_obstacles_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
