import reverse_geocoder as rg

def get_location(lat, lon):
    results = rg.search((lat, lon))
    if results:
        info = results[0]
        return info['name'], info['admin1'], info['cc']
    return None, None, None

city, region, country_code = get_location(52.52, 13.405)
print(f"City: {city}, Region: {region}, Country: {country_code}")