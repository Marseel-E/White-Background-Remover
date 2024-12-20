import os
import json
from PyQt5.QtGui import QPixmap, QImage

def save_image(image, output_folder, file_name):
	"""
	Save an image to the specified folder with the given file name.

	Args:
		image (PIL.Image): The image to save.
		output_folder (str): The folder to save the image in.
		file_name (str): The name of the saved image file.
	"""
	os.makedirs(output_folder, exist_ok=True)
	output_path = os.path.join(output_folder, file_name)
	image.save(output_path, "PNG")
	return output_path

def load_config(config_path):
	"""
	Load settings from a JSON configuration file.

	Args:
		config_path (str): The path to the JSON configuration file.

	Returns:
		dict: The loaded configuration, or an empty dictionary if loading fails.
	"""
	if os.path.exists(config_path):
		try:
			with open(config_path, "r") as file:
				return json.load(file)
		except (json.JSONDecodeError, OSError):
			pass
	return {}

def save_config(config_path, settings):
	"""
	Save settings to a JSON configuration file.

	Args:
		config_path (str): The path to the JSON configuration file.
		settings (dict): The settings to save.
	"""
	try:
		with open(config_path, "w") as file:
			json.dump(settings, file, indent=4)
	except OSError:
		pass

def pil_image_to_pixmap(image):
	"""
	Convert a PIL Image to a QPixmap.

	Args:
		image (PIL.Image): The image to convert.

	Returns:
		QPixmap: The converted QPixmap.
	"""
	if image.mode != "RGBA":
		image = image.convert("RGBA")
	image_data = image.tobytes("raw", "RGBA")
	qimage = QImage(image_data, image.width, image.height, QImage.Format_RGBA8888)
	return QPixmap.fromImage(qimage)