"""
threads.py

This module contains thread classes for processing images in the White Background
Remover project. It supports single image processing, batch processing, and real-time
processing with GPU acceleration.

Classes:
	- ImageProcessingThread: Handles processing of a single image.
	- BatchProcessingThread: Handles batch processing of multiple images.
	- RealTimeProcessingThread: Extends ImageProcessingThread for real-time updates.
"""

import os
from PIL import Image
import numpy as np
import torch
from PyQt5.QtCore import QThread, pyqtSignal


class ImageProcessingThread(QThread):
	"""
	Handles single image processing on a separate thread.

	Processes an image by splitting it into multiple layers based on grayscale intensity.
	Uses GPU acceleration (if available) for faster computations.

	Signals:
		processing_done (list): Emitted when processing is complete, with a list of processed layers.

	Args:
		img_path (str): Path to the image file to be processed.
		num_layers (int): Number of layers to divide the image into.
		strength (float): Global strength factor for layer processing.
		black_factor (float): Factor to adjust grayscale intensity.
		device (torch.device): Device to use for processing (CPU or GPU).
	"""

	processing_done = pyqtSignal(list)  # Signal to emit processed layers

	def __init__(self, img_path, num_layers, strength, black_factor, device):
		super().__init__()
		self.img_path = img_path
		self.num_layers = num_layers
		self.strength = strength
		self.black_factor = black_factor
		self.device = device
		self._is_running = True

	def run(self):
		"""Perform image processing and split the image into layers."""
		try:
			img = Image.open(self.img_path).convert("RGBA")
			img_array = np.array(img, dtype=np.uint8)
			h, w, _ = img_array.shape
			img_tensor = torch.from_numpy(img_array).to(self.device).float()
			rgb, alpha = img_tensor[..., :3], img_tensor[..., 3]
			gray = rgb.mean(dim=-1) * (1.0 / self.black_factor)

			layers = []
			step = 1.0 / self.num_layers
			for i in range(self.num_layers):
				if not self._is_running:
					return  # Exit if thread is stopped
				low, high = step * i, step * (i + 1)
				low_val, high_val = low * 255 * self.strength, high * 255 * self.strength
				mask = (gray >= low_val) & (gray < high_val)

				layer = torch.zeros_like(img_tensor)
				layer[..., :3][mask] = rgb[mask]
				layer[..., 3][mask] = alpha[mask]

				layer_img = Image.fromarray(layer.byte().cpu().numpy(), mode="RGBA")
				layers.append(layer_img)

			self.processing_done.emit(layers)  # Emit processed layers
		except Exception as e:
			print(f"Error in processing thread: {e}")

	def stop(self):
		"""Stop the processing thread."""
		self._is_running = False
		self.wait()


class BatchProcessingThread(QThread):
	"""
	Handles batch processing of multiple images on a separate thread.

	Processes each image in the batch by splitting it into layers based on grayscale intensity.
	Saves the processed layers to an output folder.

	Signals:
		processing_done (): Emitted when batch processing is complete.

	Args:
		file_paths (list): List of image file paths to process.
		num_layers (int): Number of layers to divide each image into.
		strength (float): Global strength factor for layer processing.
		black_factor (float): Factor to adjust grayscale intensity.
		device (torch.device): Device to use for processing (CPU or GPU).
	"""

	processing_done = pyqtSignal()  # Signal emitted when batch processing is complete

	def __init__(self, file_paths, num_layers, strength, black_factor, device):
		super().__init__()
		self.file_paths = file_paths
		self.num_layers = num_layers
		self.strength = strength
		self.black_factor = black_factor
		self.device = device

	def run(self):
		"""Perform batch processing of multiple images."""
		try:
			for img_path in self.file_paths:
				img = Image.open(img_path).convert("RGBA")
				img_array = np.array(img, dtype=np.uint8)
				h, w, _ = img_array.shape
				img_tensor = torch.from_numpy(img_array).to(self.device).float()
				rgb, alpha = img_tensor[..., :3], img_tensor[..., 3]
				gray = rgb.mean(dim=-1) * (1.0 / self.black_factor)

				step = 1.0 / self.num_layers
				output_folder = os.path.join(os.path.dirname(img_path), "Output")
				os.makedirs(output_folder, exist_ok=True)

				for i in range(self.num_layers):
					low, high = step * i, step * (i + 1)
					low_val, high_val = low * 255 * self.strength, high * 255 * self.strength
					mask = (gray >= low_val) & (gray < high_val)

					layer = torch.zeros_like(img_tensor)
					layer[..., :3][mask] = rgb[mask]
					layer[..., 3][mask] = alpha[mask]

					layer_img = Image.fromarray(layer.byte().cpu().numpy(), mode="RGBA")
					output_path = os.path.join(output_folder, f"{os.path.basename(img_path)}_layer{i + 1}.png")
					layer_img.save(output_path)

			self.processing_done.emit()  # Emit signal when batch processing is complete
		except Exception as e:
			print(f"Error in batch processing thread: {e}")


class RealTimeProcessingThread(ImageProcessingThread):
	"""
	Handles real-time updates for single image processing.

	Extends the functionality of ImageProcessingThread to allow for interactive,
	real-time updates based on user adjustments.

	Note:
		This class currently inherits all behavior from ImageProcessingThread
		and can be extended further for real-time specific features.
	"""
	pass  # Inherits all behavior from ImageProcessingThread