# Offline Data Entry Portal

A lightweight, standalone Windows application built with Python and Tkinter that allows users to securely add, view, update, and delete data completely offline. All data is saved automatically to a hidden local database directory.

## Prerequisite: Installing Python on Windows

Before you can run the source code or compile it into an executable, you must install Python on your machine.

1. **Download Python:** Visit the official download page at [python.org/downloads](https://python.org) and click the yellow download button.
2. **Run Installer:** Open the downloaded installer file.
3. **CRITICAL STEP:** At the bottom of the installer window, check the box that says **"Add python.exe to PATH"**. If you skip this step, your system terminal will not recognize Python commands.
4. **Complete Setup:** Click **Install Now**. Close the setup window once complete.

---

## Technical Project Setup

Open your Windows **PowerShell** or **Command Prompt**, navigate to your project directory (e.g., `cd C:\code`), and follow these development steps:

### 1. Test the Code Locally
To verify that the application interface runs correctly without errors, launch the script directly using Python:
```powershell
python app.py
```
*(If your machine uses the standard launcher shortcut, use `py app.py` instead).*

### 2. Install the Packaging Tool
To bundle this script into an executable that runs on any client computer without requiring Python, install the `PyInstaller` package:
```powershell
python -m pip install pyinstaller
```

### 3. Generate the Standalone `.exe` File
Run the following build command to compile your source code into a clean production package:
```powershell
python -m PyInstaller --noconsole --onefile --clean app.py
```

#### Command Breakdown:
* `--onefile`: Compresses all dependencies, scripts, and libraries into a single executable.
* `--noconsole`: Hides the black terminal background window, showing only your clean user interface.
* `--clean`: Clears out old build caches before compiling to prevent software corruption.

---

## Distribution & File Management

### Where is the generated file?
Once the compilation finishes successfully, navigate into your project folder. You will find a brand new directory named **`dist`**. Inside this folder is your completed application: **`app.exe`**. This is the only file you need to send to your clients.

### Database Location (Hidden)
To prevent accidental deletions or data tempering by clients, the local SQLite database file (`client_database.db`) is hidden from the project directory. It is safely isolated inside the native Windows system storage path:
`C:\Users\<Username>\AppData\Local\OfflineDataPortal\`

You can access it at any time for support by pressing `Win + R`, typing `%localappdata%\OfflineDataPortal`, and hitting Enter.

---

## Client Run Instructions
When your client downloads and launches `app.exe` for the first time, Windows SmartScreen may display a warning popup saying *"Windows protected your PC / Unknown Publisher"*. 

Because this is a custom-made offline application, they simply need to click **"More info"** and select **"Run anyway"** to open the portal.
