import os
import shutil
import requests
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_recent_versions(base_url, num_versions=3):
    """
    Fetches a list of recent driver versions from a given URL.
    This is an advanced feature and might require specific API knowledge.
    As a simpler alternative, we'll manually list a few recent versions.
    """
    # A simplified, reliable approach is to use the known version structure.
    # We can fetch the latest, then try a few decremented versions.
    try:
        latest_version = requests.get(f"{base_url}/LATEST_RELEASE").text.strip()
        versions = [latest_version]
        
        # Simple heuristic to get a few previous major versions
        # This is not guaranteed to work for all releases
        major_version = int(latest_version.split('.')[0])
        for i in range(1, num_versions):
            prev_major = major_version - i
            if prev_major > 0:
                try:
                    # Attempt to get the latest release for the previous major version
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
    Downloads the latest msedgedriver.exe and a few recent past versions.
    """
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
            
            # Copy the downloaded driver to the target location
            shutil.copy(driver_path, destination_filename)
            
            print(f"✅ Driver version {version} successfully copied to {destination_filename}")
            
        except Exception as e:
            print(f"❌ Failed to download driver for version {version}: {e}")
    
    print("Download process complete.")

if __name__ == "__main__":
    download_and_store_drivers()
