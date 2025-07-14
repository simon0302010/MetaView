import re

from geopy.geocoders import Nominatim


def convert_dms(dms):
    # Regex to extract degrees, minutes, seconds, and direction
    match = re.match(r"(\d+)\s*deg\s*(\d+)'[\s]*(\d+(?:\.\d+)?)\"?\s*([NSEW])", dms)
    if not match:
        raise ValueError(f"Invalid DMS format: {dms}")

    degrees, minutes, seconds, ref = match.groups()
    degrees = int(degrees)
    minutes = int(minutes)
    seconds = float(seconds)

    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ["S", "W"]:
        decimal = -decimal
    return decimal


latitude = "43 deg 28' 5.68\" N"
longitude = "11 deg 52' 48.62\" E"

geolocator = Nominatim(user_agent="MetaView")
location = geolocator.reverse(f"{convert_dms(latitude)}, {convert_dms(longitude)}")
print(location.address)
