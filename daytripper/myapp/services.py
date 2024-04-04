import requests
from daytripper import settings
# function for using text search function of google places api input text query
def text_search(query):
    endpoint = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.id,places.formattedAddress,places.location'  # Specify the fields you want to include
    }
    data = {
        'textQuery': query
    }
    response = requests.post(endpoint, json=data, headers=headers)
    return response.json()
# function to search nearby places input type of places, radius, latitude, and longitude
def nearby_search(type,radius,latitude,longitude):
    endpoint = 'https://places.googleapis.com/v1/places:searchNearby'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.id'  # Specify the fields you want to include
    }
    data = {
        'includedTypes':[type],
        'maxResultCount': 20,
        'locationRestriction':{
            'circle':{
                'center':{
                    'latitude': latitude,
                    'longitude': longitude},
                'radius': radius
                }
            }
        }

    response = requests.post(endpoint, json=data, headers=headers)
    return response.json()


#input place_id and return place detail
def get_place_details(place_id):
    GOOGLE_PLACES_API_KEY = 'AIzaSyDk00JlTOvjLidEHIwRue1ER9tD-4rjVvk'
    endpoint = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={settings.GOOGLE_PLACES_API_KEY}'
    response = requests.get(endpoint)
    return response.json()


def get_place_photos(photo_reference):
    photo_endpoint = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={settings.GOOGLE_PLACES_API_KEY}'
    return photo_endpoint