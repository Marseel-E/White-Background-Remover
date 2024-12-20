from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image
import numpy as np
import torch

class ImageProcessingThread(QThread):
    """Thread for processing a single image."""
    processing_done = pyqtSignal(list)

    def __init__(self, img_path, num_layers, strength, black_factor, device):
        """
        Initialize the image processing thread.

        Args:
            img_path (str): Path to the image file.
            num_layers (int): Number of layers to create.
            strength (float): The strength factor for processing.
            black_factor (float): Factor to adjust the black levels.
            device (torch.device): The device (CPU/GPU) for processing.
        """
        super().__init__()
        self.img_path = img_path
        self.num_layers = num_layers
        self.strength = strength
        self.black_factor = black_factor
        self.device = device
        self._is_running = True

    def run(self):
        """
        Run the image processing task in a separate thread.
        """
        try:
            img = Image.open(self.img_path).convert("RGBA")
            img_array = np.array(img, dtype=np.uint8)
            img_tensor = torch.from_numpy(img_array).to(self.device).float()

            gray = img_tensor[..., :3].mean(dim=-1) / self.black_factor
            layers = []
            step = 1.0 / self.num_layers

            for i in range(self.num_layers):
                if not self._is_running:
                    return
                low, high = step * i, step * (i + 1)
                mask = (gray >= low * 255 * self.strength) & (gray < high * 255 * self.strength)

                layer = torch.zeros_like(img_tensor)
                layer[..., :3][mask] = img_tensor[..., :3][mask]
                layer[..., 3][mask] = img_tensor[..., 3][mask]
                layer_img = Image.fromarray(layer.byte().cpu().numpy(), "RGBA")
                layers.append(layer_img)

            self.processing_done.emit(layers)
        except Exception:
            pass

    def stop(self):
        """
        Stop the processing thread.
        """
        self._is_running = False