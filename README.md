# IIITU Auto Wi-Fi Login (Sophos Captive Portal)

A lightweight, background Python automation script designed to handle the 30-minute Sophos captive portal timeout at the Indian Institute of Information Technology (IIIT) Una. 

Instead of relying on HTTP requests (which Sophos intercepts), this script uses native ICMP pings to accurately detect internet drops. When the portal disconnects you, the script launches a headless, completely invisible Edge browser to log you back in—without interrupting your work or popping up any black command windows.

## ✨ Features
* **100% Invisible:** Runs entirely in the background using a VBScript wrapper. No sudden terminal popups.
* **Smart Detection:** Uses ICMP ping (`8.8.8.8`) with TTL validation to bypass Sophos HTTP redirection traps.
* **Auto-Reconnect:** If the laptop drops the physical Wi-Fi connection (e.g., waking from sleep), it forces Windows to reconnect to `IIITU_WIRELESS` before attempting login.
* **Self-Cleaning Logs:** Includes a 24-hour maintenance routine that automatically wipes the log file to prevent storage bloat.
* **Graceful Error Handling:** Catches DHCP delays (`ERR_ADDRESS_UNREACHABLE`) and network hiccups without crashing.

## 📋 Prerequisites
* **OS:** Windows 10/11
* **Browser:** Microsoft Edge (Pre-installed on Windows)
* **Python:** Python 3.x installed and added to PATH
* **Dependencies:** Selenium WebDriver

Install the required Python package:
```bash
pip install selenium
```

## ⚙️ Setup & Configuration

### 1. Configure the Python Script
Open `wifi_login.py` and update the credentials section with your IIITU roll number and password:
```python

SOPHOS_URL = "YOUR_SOPHOS_URL"  
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
```

### 2. Prepare Windows Settings
For the script to monitor your Wi-Fi status properly, ensure the following Windows settings are correct:
* **Connect Manually Once:** Click the Windows Wi-Fi icon, connect to `IIITU_WIRELESS`, and check **"Connect automatically"**. Windows needs the profile saved.
* **Location Services MUST be ON:** Go to *Settings > Privacy & security > Location*. Ensure **Location services** and **Let desktop apps access your location** are ON. (Windows 11 blocks Python from reading the current Wi-Fi SSID if location is turned off).

### 3. Create the Invisible Launcher
To prevent the script from opening a black console window every 30 minutes, we use a VBScript to launch it silently.
1. Open Notepad and paste the following code:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe ""C:\Path\To\Your\wifi_login.py""", 0, False
```
2. Replace `C:\Path\To\Your\wifi_login.py` with the actual path to your script.
3. Save the file as `AutoWifi.vbs`.

### 4. Run on Startup
1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Move your `AutoWifi.vbs` file into this Startup folder.
3. Double-click the VBScript once to start it immediately. It will now launch automatically every time you turn on your laptop.

## 🛠️ Troubleshooting

You can monitor the script's activity by opening the `wifi_login_history.log` file generated in the same directory as the script.

| Log Message | Meaning / Fix |
| :--- | :--- |
| **`ERR_ADDRESS_UNREACHABLE`** | Normal. Windows just woke from sleep and hasn't acquired an IP address yet. The script will try again successfully in 50 seconds. |
| **`Windows failed to check Wi-Fi`** | Location Services are likely turned off. Windows blocks the script from reading the SSID. |
| **Silent / No logs** | The script is working perfectly. It only writes to the log when it detects a disconnection or runs its 24-hour cleanup. |
