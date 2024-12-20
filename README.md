# White Background Remover
*This program does not use AI, which is ironic because AI was utilized in creating it lol.*
## Description
**White Background Remover** is a powerful and user-friendly desktop application designed to process images by removing white or white-like backgrounds and splitting them into distinct grayscale intensity layers. It supports batch processing, real-time previews, and GPU acceleration to ensure fast and efficient performance. The application is built to run seamlessly on Windows, macOS, and Linux.

# Features
- **Layer Splitting**: Divide an image into multiple layers based on grayscale intensity.
- **Adjustable Parameters**: Customize the strength, number of layers, and black factor for fine-tuned results.
- **Real-Time Previews**: Instantly see changes as you adjust the parameters.
- **Batch Processing**: Process multiple images in one go.
- **GPU Acceleration**: Leverages GPU for faster image processing where supported.
- **Flexible Background Options**: Choose between transparent or solid color backgrounds for previews.
- **Save Results**: Export individual layers or the entire processed set.
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux.

## Setup Guide
1. **Python Version**:
Ensure Python 3.8 or later is installed on your system. [Download Python](https://www.python.org/downloads/)
2. **Dependencies**:
Install the required libraries using pip:
```bash
python3 -m pip install -r requirements.txt
```
3. **Clone the Repository**:
```bash
git clone https://github.com/Marseel-E/White-Background-Remover.git
```
4. **Verify GPU Support**: (optional)
To ensure GPU acceleration is available:
  - For NVIDIA GPUs, install the required CUDA toolkit.
  - for MacOS (Apple Silicon), ensure Metal Performance Shaders (MPS) is enabled.
5. **Run the application**:
```bash
python3 White-Background-Remover
```

### How to Use
1. **Load an Image**:
  - Click on the **"Choose Image"** button in the sidebar to select a single image.
2. **Adjust Parameters**:
  - **Strength**: Use the slider or text input to adjust the removal intensity.
  - **Number of Layers**: Use the spinbox to define how many layers you want to generate.
  - **Black Factor**: Fine-tune the grayscale intensity mapping.
3. **Preview Results**:
  - Use the tabbed view to switch between individual layers.
  - Adjust the background settings (solid color or transparent) for better visualization.
4. **Save Results**:
  - **Save Current Layer**: Click the **"Save Current Layer"** button to export the selected layer.
  - **Save All Layers**: Use the **"Save All Layers"** button to export all layers into a designated `Output` folder.

### Exiting
Click the close button or press `Ctrl + C` in the terminal to exit the application.

## License
[Mit](https://en.wikipedia.org/wiki/MIT_License)

## Support
For issues, feature requests, or contributions, feel free to create an issue or pull request in the repository.
