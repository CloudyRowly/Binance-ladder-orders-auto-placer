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
Use the following command to build the application once you have setup the config.ini file. Run it using the terminal from the repo's root directory first:
```pyinstaller -i src/resource/assets/icon.ico -n "Cloudy LTC isolated Broker" --onefile --noupx --clean --add-data "src/main/config.ini:." src/main/gui.pyw```

# Main class
gui.pyw