# MBTA

## install library

pip install fastapi
pip install uvicorn
pip install python-dotenv asyncio requests logging pydantic
pip install pytest httpx pytest-asyncio

create a .env file to store API key:
MBTA_KEY="Your API Key"

## run code in local

uvicorn main:app --reload
(API is running on http://127.0.0.1:8000)

## Documentation of API

http://127.0.0.1:8000/docs

## Design decisions

1. Get stop information from MBTA stops api
2. Use stop_id get route information for that stop
3. Use route_id get route patterns for that route, this step I will get a list of representative_trip_id. And those ids can be used to retrieve adjacent stops.
4. use trip_id to get shedules for that trip. And I will get a list of ordered stops which I can use stop_id to get adjacent stops.

## Problems and Limitations

### Problem with data

1. Same stop name might have different stop Id.
2. If there is no schedule for specific trip, then I am not able to get adjacent stops.

### Problem when testing API

1. To fetch all stops information, the API is slow and take long time to load
   Solution:
   - 1. Create pagnation, fetch limit numbers of stops at a time
   - 2. Create a api to fetch stop by stop name, only one stop information is returned
2. Some stop names have specical characters, like '/',
   Solution:
   - 1. When pass stop name to api endpoint as a paramter, remove special characters
   - 2. In the code, remove special characters from stop name when comparing it with parameter name.
3. When comebining adjacent stops from each trips, some adjacent stops are duplicate, remove duplicate adjacent stops.
4. Edge case when get adjacent stops:
   If stop is the first/last stop in the trip, this stop will only have one adjacent stop.

## Future work

1. add caching to save API response
2. add rate limiting for the API
