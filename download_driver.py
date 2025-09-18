import os
import shutil
import requests
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_recent_versions(base_url, num_versions=3):
    """
    Fetches a list of recent driver versions from a given URL.
    """
    try:
        latest_version = requests.get(f"{base_url}/LATEST_RELEASE").text.strip()
        versions = [latest_version]
        
        major_version = int(latest_version.split('.')[0])
        for i in range(1, num_versions):
            prev_major = major_version - i
            if prev_major > 0:
                try:
                    prev_version = requests.get(f"{base_url}/LATEST_RELEASE_{prev_major}").text.strip()
                    versions.append(prev_version)
                except requests.exceptions.RequestException:
                    continue
        return versions
    except Exception as e:
        print(f"Error fetching versions: {e}")
        return []

def download_and_store_drivers():
    """
    Downloads the latest msedgedriver.exe and a few recent past versions
    into a dedicated 'webdrivers' folder.
    """
    webdrivers_folder = "webdrivers"
    # Create the folder if it doesn't exist
    os.makedirs(webdrivers_folder, exist_ok=True)
    
    base_url = "https://msedgedriver.azureedge.net"
    versions_to_download = get_recent_versions(base_url, num_versions=3)
    
    if not versions_to_download:
        print("Could not retrieve driver versions. Exiting.")
        return

    print(f"Attempting to download the following versions: {', '.join(versions_to_download)}")
    
    for version in versions_to_download:
        try:
            print(f"Downloading msedgedriver version {version}...")
            # Use EdgeChromiumDriverManager with a specific version
            driver_path = EdgeChromiumDriverManager(version=version).install()
            
            # Create a new filename with the version number embedded
            destination_filename = f"msedgedriver_{version}.exe"
            
            # Define the full destination path inside the new folder
            destination_path = os.path.join(webdrivers_folder, destination_filename)
            
            # Copy the downloaded driver to the target location
            shutil.copy(driver_path, destination_path)
            
            print(f"✅ Driver version {version} successfully copied to {destination_path}")
            
        except Exception as e:
            print(f"❌ Failed to download driver for version {version}: {e}")
    
    print("Download process complete.")

if __name__ == "__main__":
    download_and_store_drivers()
