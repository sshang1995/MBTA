# MBTA

## Install library

- pip install fastapi
- pip install uvicorn
- pip install python-dotenv asyncio requests logging pydantic
- pip install pytest httpx pytest-asyncio

create a .env file to store API key:
MBTA_KEY="Your API Key"

## Run code in local

uvicorn main:app --reload
(API is running on http://127.0.0.1:8000)

## Documentation of API

http://127.0.0.1:8000/docs

## Design decisions

1. Fetch stop information

- Use the MBTA stops API to retrieve basic information about all available stops.

2. Retrieve routes for a stop

- Use the stop_id to fetch all route IDs that server this stop.

3. Get Route Patterns and Representative Trips

- For each route, retrieve the route patterns and extract a list of representation_trip_id. These trips IDs are essential to determining adjacent stops.

4. Retrieve Trip Schedules

- Use each trip_id to get the full schedule, which includes an ordered list of stops. These can then be used to determine the adjacent stops for a given stop.

## Problems and Limitations

### Problem with data

1. Duplicate stop names

- Some stop names may correspond to multiple unqiue stop IDs.

2. Real time schedules

- If a trip_id has no schedule data at the moment, you cannot determine its adjacent stops.

### API testing challenges

1. Slow fetching of all stops

- The /stops endpoint returns a large dataset and is slow to respond
  Solution:
  - 1.  Implement pagination to fetch a limited number of stops per request.
  - 2.  Provide an endpoint to search for a stop by name, returning a single stop object.

2. Special characters in stop names (e.g. '/')

- These can break URL parsing or route matching
  Solution:
  - 1.  Strip or encode special characters from stop names when passing as URL paramters.
  - 2.  Normalize stop names in both incoming requests and internal comparisons.

3. Duplicate Adjacent Stops

- When aggregating adjacent stops from multiple trips, duplicates may occur.
  Solution:
- Use a set and deduplication logic to ensure adjacent stops are unique.

4. Edge case - Stop at start or End of trip

- A stop that is first or last in a trip will have only one adjacent stop.
- Handle this gracefully in logic to avoid index error.

## Future work

1. Add caching to save API response
2. Add rate limiting for the API
