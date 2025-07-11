import subprocess
import json

def get_exif_with_exiftool(filename):
    result = subprocess.run(
        ["exiftool", "-j", filename],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data[0] if data else {}

exif_data = get_exif_with_exiftool("Xbox360.png")
for key, value in exif_data.items():
    print(f"{key}: {value}")