import reverse_geocoder as rg
import re

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

def get_location(lat, lon):
    results = rg.search((lat, lon))
    if results:
        info = results[0]
        return info['name'], info['admin1'], info['cc']
    return None, None, None

latitude = "43 deg 28' 5.68\" N"
longitude = "11 deg 52' 48.62\" E"

city, region, country_code = get_location(convert_dms(latitude), convert_dms(longitude))
print(f"City: {city}, Region: {region}, Country: {country_code}")