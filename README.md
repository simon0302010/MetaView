# MetaView

Viewer and Editor for Image Metadata

## Core Functionality

MetaView is a powerful tool for viewing and editing metadata embedded in image files. It provides:

- **Comprehensive metadata display**: View all metadata embedded in your images, organized by categories
- **Metadata editing**: Edit metadata fields with a simple double-click interface
- **Geocoding**: Automatically convert GPS coordinates to readable location information (city, region, country)
- **Image preview**: See a thumbnail of your image while viewing its metadata
- **Category organization**: Metadata is organized into logical categories for easier browsing

## How It Works

MetaView leverages several technologies to provide its functionality:

1. **ExifTool**: Uses the powerful ExifTool command-line application to read and write image metadata
2. **PyQt5**: Provides the graphical user interface with tabs for each metadata category
3. **Reverse Geocoder**: Converts GPS coordinates into human-readable location information
4. **Custom categorization**: Groups metadata fields into logical categories for easier navigation

## Installation

### Requirements

- Python 3.8 or higher
- ExifTool must be installed on your system

### Install from PyPI

```bash
pip install metaview
```

### Install ExifTool

On Debian/Ubuntu:
```bash
sudo apt install exiftool
```

On Fedora:
```bash
sudo dnf install perl-Image-ExifTool
```

On macOS:
```bash
brew install exiftool
```

## Usage

### Basic Usage

To launch MetaView:

```bash
python -m metaview
```

Or, to open a specific image directly:

```bash
python -m metaview /path/to/image.jpg
```

### Using the Interface

1. **Open an image**:
   - Select File → Open or press Ctrl+O
   - Choose an image file from the dialog

2. **View metadata**:
   - Metadata is organized into tabs by category
   - Scroll through each tab to explore different metadata fields

3. **Edit metadata**:
   - Double-click on any editable value to modify it
   - Press Enter to save the value
   - Some fields (like File Name, Image Size, etc.) are read-only and cannot be edited

4. **Save changes**:
   - Select File → Save or press Ctrl+S to save all metadata changes to the image file

## Features

- **Categorized Metadata**: Metadata is organized into logical groups (General, Camera, Exposure, Location, etc.)
- **In-place Editing**: Double-click to edit values directly within the interface
- **Location Display**: GPS coordinates are automatically converted to city, region, and country names
- **Image Preview**: See a thumbnail of the image while working with its metadata
- **Change Tracking**: Only modified values are written back to the image file

## Example

When examining a photograph taken with a digital camera, MetaView will display information such as:

- Camera manufacturer and model
- Exposure settings (aperture, shutter speed, ISO)
- Date and time the photo was taken
- GPS location data with human-readable location names
- Copyright and author information
- Software used to process the image
- Technical details about the image format

## License

MetaView is licensed under the GPL-3.0 License.