import subprocess
import json
import sys

def get_exif_with_exiftool(filename):
    result = subprocess.run(
        ["exiftool", "-j", filename],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data[0] if data else {}

try:
    exif_data = get_exif_with_exiftool(sys.argv[1])
except IndexError:
    print("Please provide the path to an image file")
    sys.exit(1)

print(exif_data)
for key, value in exif_data.items():
    if key == "Model":
        print(f"{key}: {value}")
    #print(f"{key}: {value}")