![PyPI - Version](https://img.shields.io/pypi/v/MetaView)
![PyPI - License](https://img.shields.io/pypi/l/MetaView)
![](https://hackatime-badge.hackclub.com/U08HC7N4JJW/MetaView)

<div align="left">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>

# MetaView

**MetaView** is a modern, user-friendly application for viewing and editing image metadata. It supports advanced features like geocoding, weather lookup, and 3D Earth visualization, making it a powerful tool for photographers, archivists, and anyone working with digital images.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Metadata Categories](#metadata-categories)
- [Weather & Location Features](#weather--location-features)
- [3D Earth Visualization](#3d-earth-visualization)
- [Development & Testing](#development--testing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Comprehensive Metadata Display:** View all metadata embedded in your images, organized by logical categories.
- **In-place Metadata Editing:** Edit most metadata fields directly with a double-click.
- **Geocoding:** Automatically converts GPS coordinates to readable city, region, and country names.
- **Weather Lookup:** Fetches historical or forecast weather for the photo's time and location.
- **Image Preview:** See a thumbnail of your image alongside its metadata.
- **3D Earth Visualization:** Visualize the photo's location on a 3D globe.
- **Change Tracking:** Only modified values are written back to the image file.
- **Cross-platform:** Runs on Linux and macOS (Windows support may be limited).
- **Modern GUI:** Built with PyQt5 for a responsive and intuitive interface.

---

## Installation

### Requirements

- Python 3.8–3.14
- ExifTool (must be installed on your system)

### Install MetaView

From PyPI:
```bash
pip install metaview
```

### Install ExifTool

**Debian/Ubuntu:**
```bash
sudo apt install exiftool
```

**Fedora:**
```bash
sudo dnf install perl-Image-ExifTool
```

**macOS (Homebrew):**
```bash
brew install exiftool
```

## Usage

### Launching MetaView

To start the application:
```bash
python -m metaview
```

To open a specific image directly:
```bash
python -m metaview /path/to/image.jpg
```

### Using the Interface

1. **Open an Image:**  
   - Use `File → Open` or press `Ctrl+O` to select an image.

2. **View Metadata:**  
   - Metadata is organized into tabs by category.
   - Scroll through each tab to explore different fields.

3. **Edit Metadata:**  
   - Double-click on any editable value to modify it.
   - Press Enter to save the change.
   - Read-only fields (e.g., file name, image size) cannot be edited.

4. **Save Changes:**  
   - Use `File → Save` or press `Ctrl+S` to write changes to the image.
   - Use `File → Save to` to save metadata to another file.

5. **Delete Metadata:**  
   - Use `File → Delete Metadata` to remove all metadata from the image.

---

## Metadata Categories

MetaView organizes metadata into logical groups, including:

- **General:** File name, type, size, permissions, etc.
- **Camera:** Manufacturer, model, lens, shooting mode, etc.
- **Exposure:** ISO, exposure time, aperture, white balance, etc.
- **Image Processing:** Software, color space, compression, etc.
- **Date & Time:** Original date/time, modification date, etc.
- **Author & Rights:** Artist, copyright, source, etc.
- **Location:** GPS coordinates, altitude, direction, etc.
- **Editing History:** Software and actions used to edit the image.
- **XMP & IPTC:** Advanced metadata standards.
- **Advanced/Technical:** Exif version, orientation, color components, etc.

---

## Weather & Location Features

- **Geocoding:**  
  Converts GPS coordinates to city, region, and country using reverse geocoding.

- **Weather Lookup:**  
  Fetches weather conditions (temperature, description, icon) for the photo's time and location using the Open-Meteo API.  
  - If the photo is older than 7 days, historical weather is shown.
  - Otherwise, forecast data is used.

---

## 3D Earth Visualization

MetaView can display the photo's location on a 3D globe using VisPy.  
- The globe is textured with a realistic Earth map.
- The photo's location is marked in red.
- You can rotate and zoom the globe using mouse controls.

---

## License

MetaView is licensed under the **GPL-3.0 License**.

---

## Acknowledgements

- [ExifTool](https://exiftool.org/) by Phil Harvey
- [Open-Meteo](https://open-meteo.com/) for weather data
- [Reverse Geocoder](https://github.com/thampiman/reverse-geocoder)
- [VisPy](https://vispy.org/) for 3D visualization
- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro/)
- [imageio](https://imageio.readthedocs.io/)
- [country_converter](https://github.com/konstantinstadler/country_converter)