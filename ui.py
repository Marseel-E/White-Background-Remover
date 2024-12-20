import os
import torch
from PyQt5.QtWidgets import (
	QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
	QTabWidget, QSlider, QLineEdit, QGraphicsScene, QGraphicsView,
	QHBoxLayout, QGroupBox, QSpinBox, QCheckBox, QFrame
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from threads import BatchProcessingThread, ImageProcessingThread
from utils import pil_image_to_pixmap, save_image, load_config, save_config


class WhiteBackgroundRemoverApp(QWidget):
	"""
	Main application class for the White Background Remover GUI.

	Allows users to process images by splitting them into multiple layers based
	on grayscale intensity. Users can adjust settings such as strength, number
	of layers, and black factor. The processed layers can be previewed and saved.

	Attributes:
		num_layers (int): Number of layers to divide the image into.
		strength (float): Global strength factor for layer processing.
		black_factor (float): Factor to adjust grayscale intensity.
		bg_hex_code (str): Hexadecimal code for background color in the preview.
		transparent_bg (bool): Whether to use a transparent background.
	"""

	def __init__(self):
		super().__init__()
		self.init_variables()
		self.init_ui()

	def init_variables(self):
		"""
		Initialize application variables and load user settings.
		"""
		self.settings = load_config("config.json")
		self.num_layers = self.settings.get("num_layers", 3)
		self.strength = self.settings.get("strength", 0.8)
		self.black_factor = self.settings.get("black_factor", 1.0)
		self.bg_hex_code = self.settings.get("bg_hex_code", "#00FFFF")
		self.transparent_bg = self.settings.get("transparent_bg", False)

		self.processing_thread = None
		self.batch_processing_thread = None
		self.layers = []  # Store processed layers for the current image
		self.current_image_path = None

	def init_ui(self):
		"""
		Set up the user interface for the application.
		"""
		self.setWindowTitle("White Background Remover")
		self.resize(1200, 800)

		main_layout = QVBoxLayout(self)
		self.label = QLabel("Select an image or folder to process.")
		main_layout.addWidget(self.label)

		# Separator line
		separator = QFrame()
		separator.setFrameShape(QFrame.HLine)
		separator.setFrameShadow(QFrame.Sunken)
		main_layout.addWidget(separator)

		# Tabbed view for displaying layers
		self.tab_widget = QTabWidget()
		main_layout.addWidget(self.tab_widget, 1)

		# Controls group
		controls_group = QGroupBox("Controls")
		controls_layout = QVBoxLayout(controls_group)

		# Strength slider and text input
		self.strength_slider, self.strength_text = self.create_slider(
			controls_layout, "Strength (0-100):", 0, 100, int(self.strength * 100), self.update_strength
		)

		# Number of layers spinbox
		self.create_spinbox(controls_layout, "Number of Layers:", 1, 20, self.num_layers, self.update_num_layers)

		# Black factor slider and text input
		self.black_factor_slider, self.black_factor_text = self.create_slider(
			controls_layout, "Black Factor (0.1-3.0):", 10, 300, int(self.black_factor * 100), self.update_black_factor
		)

		# Background settings
		bg_layout = QHBoxLayout()
		self.transparent_checkbox = QCheckBox("Transparent Background")
		self.transparent_checkbox.setChecked(self.transparent_bg)
		self.transparent_checkbox.stateChanged.connect(self.toggle_transparent_bg)
		bg_layout.addWidget(self.transparent_checkbox)

		self.bg_hex_input = QLineEdit(self.bg_hex_code)
		self.bg_hex_input.setFixedWidth(80)
		self.bg_hex_input.setEnabled(not self.transparent_bg)
		self.bg_hex_input.textChanged.connect(self.update_bg_color)
		bg_layout.addWidget(QLabel("Background Color (Hex):"))
		bg_layout.addWidget(self.bg_hex_input)
		controls_layout.addLayout(bg_layout)

		# Buttons for choosing images and saving results
		buttons_layout = QHBoxLayout()
		self.choose_image_button = QPushButton("Choose Image")
		self.choose_image_button.clicked.connect(self.open_file_dialog)
		buttons_layout.addWidget(self.choose_image_button)

		self.save_layer_button = QPushButton("Save Current Layer")
		self.save_layer_button.clicked.connect(self.save_current_layer)
		self.save_layer_button.setEnabled(False)
		buttons_layout.addWidget(self.save_layer_button)

		self.save_button = QPushButton("Save All Layers")
		self.save_button.clicked.connect(self.save_all_layers)
		self.save_button.setEnabled(False)
		buttons_layout.addWidget(self.save_button)

		controls_layout.addLayout(buttons_layout)
		main_layout.addWidget(controls_group)


	def create_slider(self, layout, label, min_val, max_val, initial_val, on_change):
		"""
		Create a slider with an associated text input for manual value entry.

		Args:
			layout (QVBoxLayout): The layout to add the slider to.
			label (str): The label for the slider.
			min_val (int): Minimum value for the slider.
			max_val (int): Maximum value for the slider.
			initial_val (int): Initial value for the slider.
			on_change (function): Function to call when the slider value changes.
		"""
		slider_layout = QHBoxLayout()
		slider_layout.addWidget(QLabel(label))

		# Create the slider
		slider = QSlider(Qt.Horizontal)
		slider.setRange(min_val, max_val)
		slider.setValue(initial_val)
		slider.valueChanged.connect(on_change)
		slider_layout.addWidget(slider)

		# Create the text input
		text_input = QLineEdit(str(initial_val))
		text_input.setFixedWidth(60)
		text_input.setAlignment(Qt.AlignCenter)

		# Sync text input and slider
		def update_slider_from_text():
			try:
				value = int(text_input.text())
				if min_val <= value <= max_val:
					slider.setValue(value)
			except ValueError:
				pass  # Ignore invalid input

		def update_text_from_slider(value):
			text_input.setText(str(value))

		text_input.textChanged.connect(update_slider_from_text)
		slider.valueChanged.connect(update_text_from_slider)

		slider_layout.addWidget(text_input)
		layout.addLayout(slider_layout)

		return slider, text_input

	def create_spinbox(self, layout, label, min_val, max_val, initial_val, on_change):
		"""
		Create a spinbox with a label.

		Args:
			layout (QVBoxLayout): The layout to add the spinbox to.
			label (str): The label for the spinbox.
			min_val (int): Minimum value for the spinbox.
			max_val (int): Maximum value for the spinbox.
			initial_val (int): Initial value for the spinbox.
			on_change (function): Function to call when the spinbox value changes.
		"""
		spinbox_layout = QHBoxLayout()
		spinbox_layout.addWidget(QLabel(label))
		spinbox = QSpinBox()
		spinbox.setRange(min_val, max_val)
		spinbox.setValue(initial_val)
		spinbox.valueChanged.connect(on_change)
		spinbox_layout.addWidget(spinbox)
		layout.addLayout(spinbox_layout)

	def update_strength(self, value):
		"""Update the global strength setting."""
		self.strength = value / 100.0
		self.start_processing()

	def update_num_layers(self, value):
		"""Update the number of layers for processing."""
		self.num_layers = value
		self.start_processing()

	def update_black_factor(self, value):
		"""Update the black factor for processing."""
		self.black_factor = value / 100.0
		self.start_processing()

	def toggle_transparent_bg(self, state):
		"""Toggle between a transparent and solid background."""
		self.transparent_bg = state == Qt.Checked
		self.bg_hex_input.setEnabled(not self.transparent_bg)
		self.start_processing()

	def update_bg_color(self):
		"""Update the background color for the preview."""
		self.bg_hex_code = self.bg_hex_input.text()
		self.start_processing()

	def open_file_dialog(self):
		"""Open a file dialog to select an image."""
		file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")
		if file_paths:
			self.current_image_path = file_paths[0]  # Focus on the first image for now
			self.start_processing()

	def start_processing(self):
		"""
		Start processing the current image with the specified settings.
		"""
		if not self.current_image_path:
			return

		# Track the current tab index
		current_tab_index = self.tab_widget.currentIndex()

		if self.processing_thread and self.processing_thread.isRunning():
			self.processing_thread.stop()
			self.processing_thread.wait()

		self.processing_thread = ImageProcessingThread(
			self.current_image_path, self.num_layers, self.strength, self.black_factor, torch.device("cpu")
		)
		self.processing_thread.processing_done.connect(lambda layers: self.on_processing_done(layers, current_tab_index))
		self.processing_thread.start()

	def on_processing_done(self, layers, current_tab_index=None):
		"""
		Handle completion of image processing.

		Args:
			layers (list): List of processed layers.
			current_tab_index (int): Previously selected tab index.
		"""
		self.layers = layers
		self.tab_widget.clear()

		for idx, layer_img in enumerate(layers):
			pixmap = pil_image_to_pixmap(layer_img)
			scene = QGraphicsScene(self)
			scene.setBackgroundBrush(Qt.transparent if self.transparent_bg else QColor(self.bg_hex_code))
			scene.addPixmap(pixmap)

			view = QGraphicsView(scene)
			self.tab_widget.addTab(view, f"Layer {idx + 1}")

		self.save_button.setEnabled(True)
		self.save_layer_button.setEnabled(True)

		# Restore the previously active tab
		if current_tab_index is not None and 0 <= current_tab_index < self.tab_widget.count():
			self.tab_widget.setCurrentIndex(current_tab_index)

	def save_all_layers(self):
		"""Save all processed layers to the output folder."""
		if not self.layers or not self.current_image_path:
			return

		output_folder = os.path.join(os.path.dirname(self.current_image_path), "Output")
		os.makedirs(output_folder, exist_ok=True)

		for idx, layer in enumerate(self.layers):
			save_image(layer, output_folder, f"layer_{idx + 1}.png")

	def save_current_layer(self):
		"""Save the currently selected layer to the output folder."""
		current_index = self.tab_widget.currentIndex()
		if current_index == -1 or not self.layers:
			return

		output_folder = os.path.join(os.path.dirname(self.current_image_path), "Output")
		os.makedirs(output_folder, exist_ok=True)

		save_image(self.layers[current_index], output_folder, f"layer_{current_index + 1}.png")