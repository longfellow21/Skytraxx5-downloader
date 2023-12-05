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
    except Exception as e:
        print(f"Error downloading or extracting the file: {e}")

def download_file(url, target_folder):
    try:
        # Download the file
        file_path, _ = urllib.request.urlretrieve(url, os.path.join(target_folder, os.path.basename(url)))
        print(f"Download successful to {file_path}")
    except Exception as e:
        print(f"Error downloading the file: {e}")
    
    
if __name__ == "__main__":
    device_label = "SKYTRAXX"
    drive_letter = find_drive_letter(device_label)

    if drive_letter:
        # Define target folders
        airspaces_folder = os.path.join(drive_letter, "airspaces")
        obstacles_folder = os.path.join(drive_letter, "obstacles")

        # Create folders if they don't exist
        os.makedirs(airspaces_folder, exist_ok=True)
        os.makedirs(obstacles_folder, exist_ok=True)

        # Download and extract the airspaces file
        airspaces_url = "https://www.skytraxx.org/skytraxx5/airspaces/world.zip"
        download_and_extract(airspaces_url, airspaces_folder)

        # Download the obstacles file
        obstacles_url = "https://www.skytraxx.org/skytraxx5/obstacles/world.oob"
        download_file(obstacles_url, obstacles_folder)
    else:
        print(f"{device_label} not found on any drive.")
