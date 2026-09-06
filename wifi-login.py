import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

# Replace with exact SSID
PREFERRED_SSID = "IIITU_WIRELESS"

# Save log in the exact folder where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(SCRIPT_DIR, "wifi_login_history.log")

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE_PATH, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

def get_current_ssid():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode != 0: return None
        for line in result.stdout.splitlines():
            if "SSID" in line and "BSSID" not in line:
                parts = line.split(":")
                if len(parts) > 1: return parts[1].strip()
    except:
        pass
    return None

def force_connect_wifi(ssid):
    try:
        log_message(f"Attempting to connect to Wi-Fi profile: {ssid}...")
        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={ssid}"],
            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0: time.sleep(5)
    except:
        pass

def is_internet_available():
    try:
        result = subprocess.run(
            ["ping", "8.8.8.8", "-n", "1", "-w", "2000"],
            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.returncode == 0 and "TTL=" in result.stdout
    except:
        return False

def login():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")

    # CRITICAL: This hides the msedgedriver.exe black console window
    service = Service()
    service.creation_flags = subprocess.CREATE_NO_WINDOW

    driver = webdriver.Edge(options=options, service=service)

    SOPHOS_URL = "YOUR_SOPHOS_URL"  
    USERNAME = "YOUR_USERNAME"
    PASSWORD = "YOUR_PASSWORD"

    try:
        log_message("Internet blocked. Performing login...")
        driver.get(SOPHOS_URL)

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))

        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(USERNAME)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(PASSWORD)

        try:
            driver.find_element(By.ID, "loginbutton").click()
        except:
            driver.find_element(By.CSS_SELECTOR, "div#loginbutton.button").click()

        time.sleep(5)  
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(2)
        except:
            pass 

        if is_internet_available():
            log_message("SUCCESS: Internet connectivity restored!")
        else:
            log_message("WARNING: Login submitted, but internet is still blocked.")
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
    finally:
        driver.quit()

def main():
    log_message("Auto-Login Monitor Started. (Running silently)")
    
    # Set the starting timer for the 24-hour log wipe
    last_log_clear_time = time.time()
    
    while True:
        # --- 24-HOUR LOG CLEANUP CHECK ---
        # 86400 seconds = 24 hours
        if time.time() - last_log_clear_time >= 86400:
            try:
                # Opening in 'w' mode overwrites and empties the existing file
                with open(LOG_FILE_PATH, "w") as f:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] Log file automatically wiped (24-hour maintenance routine).\n")
                last_log_clear_time = time.time()
            except:
                pass
        # ----------------------------------

        ssid = get_current_ssid()
        if ssid is None:
            force_connect_wifi(PREFERRED_SSID)
            time.sleep(5)
            ssid = get_current_ssid()

        if ssid and ssid.strip().lower() == PREFERRED_SSID.strip().lower():
            if not is_internet_available():
                login()
                
        time.sleep(50)

if __name__ == "__main__":
    main()
