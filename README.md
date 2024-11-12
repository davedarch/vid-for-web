# Video Converter

A user-friendly Python GUI application for converting video files to various formats using `ffmpeg`.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Select Multiple Video Files**: Easily choose multiple video files for batch conversion.
- **Flexible Output Options**: Select from predefined conversion scripts or customize your own.
- **Dynamic Configuration**: Options adjust based on the selected conversion script.
- **Output Directory Management**: Automatically sets output directory or allows manual selection.
- **Real-time Status Updates**: Monitor the progress of your conversions in real-time.
- **Error Handling**: Informative messages for any issues encountered during processing.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.x**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **ffmpeg**: This application relies on `ffmpeg` for video processing. Download and install it from [ffmpeg.org](https://ffmpeg.org/download.html) and ensure it's added to your system's PATH.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/video-converter.git
   cd video-converter
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   This project uses standard Python libraries. However, ensure that `tkinter` is installed, which usually comes pre-installed with Python. If not, install it using your package manager.

   - **For Debian/Ubuntu:**

     ```bash
     sudo apt-get install python3-tk
     ```

   - **For macOS:**

     `tkinter` is included with the Python installer from [python.org](https://www.python.org/downloads/mac-osx/).

   - **For Windows:**

     `tkinter` is included with the standard Python installer.

## Usage

1. **Run the Application**

   Navigate to the project directory and execute the main script:

   ```bash
   python vid-for-web.py
   ```

2. **Select Input Files**

   - Click on the **"Select Input Files"** button.
   - Choose one or multiple video files (`.mp4`, `.avi`, `.mov`, `.webm`, `.gif`, `.webp`, etc.) you wish to convert.

3. **Select Output Directory**

   - Click on the **"Select Output Directory"** button.
   - Choose the folder where you want the converted files to be saved.
   - *Optional:* Reset to the default directory using the **"Reset Output Directory"** button.

4. **Choose Conversion Script**

   - Use the dropdown menu to select a conversion script (e.g., WebP, GIF).
   - Configure any available options that appear based on the selected script.

5. **Process Files**

   - Click on the **"Process Files"** button to start the conversion.
   - Monitor the status in the **Status Label**.
   - Upon completion, a notification will inform you that processing is done.

## Configuration

The application uses a `settings.json` file to define available conversion scripts and their options. Ensure that this file is present in the root directory of the project.

### Example `settings.json`

```json:path/to/settings.json
{
    "scripts": [
        {
            "name": "WebP",
            "command": "ffmpeg -i {input_file} -vcodec libwebp {options} {output_file}",
            "options": {
                "quality": [10, 80],
                "preset": ["default", "picture", "photo", "drawing", "icon", "text"]
            }
        },
        {
            "name": "GIF",
            "command": "ffmpeg -i {input_file} -vf palettegen {palette_file} && ffmpeg -i {input_file} -i {palette_file} -filter_complex paletteuse {output_file}",
            "options": {}
        }
    ]
}
```

- **name**: The display name of the conversion script.
- **command**: The `ffmpeg` command template. Placeholders like `{input_file}`, `{output_file}`, and `{palette_file}` will be replaced dynamically.
- **options**: Configurable options for the script. These will appear as widgets in the GUI for user customization.

## Logging

The application logs its operations to an `app.log` file in the project directory. This includes debug information, errors, and info messages that can help in troubleshooting.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure that your code adheres to the project's coding standards and includes relevant tests.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.

---

*Feel free to reach out for any questions or support regarding this project!*