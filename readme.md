# Dependencies
This project depends on the following libraries:
"""
packaging
tkinter
customtkinter
binance-connector

pyinstaller
"""

# Packaging command
Use the following command to build the application once you have setup the config.ini file. Run it using the terminal, navigate to the src/main/ directory first:
```pyinstaller --onefile --noupx --clean --add-data "config.ini:." gui.pyw```

# Main class
gui.pyw