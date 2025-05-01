import requests

from flask import redirect, render_template, session
from functools import wraps

def geolocate(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address.upper()}&key=AIzaSyBepnl1d3i5Whh4lNlQWMgxFevEHEuAv4c"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json()

        # Check if we got results
        if data['status'] == 'OK':
            # Extract the first result's geometry location (latitude and longitude)
            location = data['results'][0]['geometry']['location']
            return {
                "lat": location['lat'],
                "lng": location['lng']
            }
        else:
            # Handle cases where the address couldn't be geocoded
            return {"error": data.get('status', 'Unknown error')}
    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors
        return {"error": str(e)}


def reverse_geocode(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=AIzaSyB*********vEHEuAv4c"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK' and data['results']:
            # Extract formatted address
            address_components = data['results'][0]['address_components']

            # Find the city/locality and state
            city = None
            state = None

            for component in address_components:
                if 'locality' in component['types']:  # City/locality
                    city = component['long_name']
                if 'administrative_area_level_1' in component['types']:  # State
                    state = component['short_name']

            if city and state:
                return f"{city}, {state}"
            elif city:
                return city
            elif state:
                return state
        else:
            return "Unknown location"
    except requests.exceptions.RequestException:
        return "Error retrieving location"



def nearest_major_location(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&rankby=distance&type=locality&key=AIzaSyBepnl1d3i5Whh4lNlQWMgxFevEHEuAv4c"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'OK':
            # Return the name of the nearest major location
            return data['results'][0].get('vicinity', "No vicinity information found")
        else:
            return "No major location found"
    except requests.exceptions.RequestException:
        return "Error retrieving major location"


