"""
__main__.py

This is the entry point for the White Background Remover application, designed
to be executed as a Python module. It initializes the PyQt5 application, sets
up the main application window (`ImageProcessorApp`), and starts the event loop.

Modules:
	- sys: For interacting with the Python runtime environment.
	- PyQt5.QtWidgets.QApplication: The core application class for PyQt5 GUI.
	- ui.ImageProcessorApp: The main application window class defined in `ui.py`.

Usage:
	Run this module to launch the White Background Remover application:
	```bash
	python3 -m WhiteBackgroundRemover
	```

	Where `WhiteBackgroundRemover` is the directory containing this `__main__.py` file.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui import WhiteBackgroundRemoverApp

if __name__ == "__main__":
	"""
	Main entry point for the White Background Remover application.

	Steps:
		1. Create a QApplication instance: Required for all PyQt5 applications.
		2. Initialize the main application window (`ImageProcessorApp`).
		3. Show the application window to the user.
		4. Start the PyQt5 event loop to process GUI events.

	Note:
		This script is executed when the module is run using the `-m` flag
		(e.g., `python3 -m WhiteBackgroundRemover`). It serves as the main entry point.
	"""
	# Initialize the application
	app = QApplication(sys.argv)

	# Create the main window
	window = WhiteBackgroundRemoverApp()

	# Display the main window
	window.show()

	# Execute the application's event loop
	sys.exit(app.exec_())