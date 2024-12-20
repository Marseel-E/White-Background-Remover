"""
utils.py

Utility functions for the White Background Remover project.

This module provides helper functions for image processing, configuration
management, and data conversion to support the main application.

Functions:
	- pil_image_to_pixmap: Convert a PIL image to a QPixmap for PyQt display.
	- save_image: Save a PIL image to a specified folder.
	- load_config: Load application settings from a JSON file.
	- save_config: Save application settings to a JSON file.
"""

import os
import json
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image


def pil_image_to_pixmap(pil_image):
	"""
	Convert a PIL image to a QPixmap for display in PyQt.

	Args:
		pil_image (PIL.Image.Image): The PIL image to convert.

	Returns:
		QPixmap: A QPixmap representation of the PIL image.
	"""
	pil_image = pil_image.convert("RGBA")  # Ensure image is in RGBA mode.
	data = pil_image.tobytes("raw", "RGBA")  # Extract raw RGBA data.
	qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
	return QPixmap.fromImage(qimage)


def save_image(image, output_folder, file_name):
	"""
	Save a PIL image to a specified folder.

	Args:
		image (PIL.Image.Image): The PIL image to save.
		output_folder (str): Path to the folder where the image will be saved.
		file_name (str): Name of the output file.

	Raises:
		OSError: If the file cannot be saved.
	"""
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)  # Create the folder if it doesn't exist.
	output_path = os.path.join(output_folder, file_name)
	try:
		image.save(output_path, "PNG")
	except OSError as e:
		raise OSError(f"Failed to save image at {output_path}: {e}")


def load_config(config_path):
	"""
	Load application settings from a JSON configuration file.

	Args:
		config_path (str): Path to the JSON configuration file.

	Returns:
		dict: A dictionary of settings loaded from the file. Returns an empty
			  dictionary if the file does not exist or cannot be loaded.
	"""
	if os.path.exists(config_path):
		try:
			with open(config_path, "r") as file:
				return json.load(file)
		except (json.JSONDecodeError, OSError) as e:
			print(f"Error loading config file at {config_path}: {e}")
			return {}
	return {}


def save_config(config_path, settings):
	"""
	Save application settings to a JSON configuration file.

	Args:
		config_path (str): Path to the JSON configuration file.
		settings (dict): Dictionary of settings to save.

	Raises:
		OSError: If the file cannot be written.
	"""
	try:
		with open(config_path, "w") as file:
			json.dump(settings, file, indent=4)
	except OSError as e:
		raise OSError(f"Failed to save config at {config_path}: {e}")