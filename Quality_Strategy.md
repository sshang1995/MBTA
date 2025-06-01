## Objectives

Deliver accurate subway stop information from API endpoints. Ensure all endpoints are easy to use and return accurate response.

## Scope

1. API endpoints integrated with MBTA API.
2. Only focus on (light and heavy trail) subway stop.

## Testing

### Unit Testing

1. Verify business logic for extracting GPS coordinates, subway line mapping, adjacent stops.
   1.1 Create test cases, making several json response to check if API response matches the test case.
   1.2 Test edge cases, eg. a subway stop does not have adjacent stops or deprecated routes or stops.

2. Verify MBTA APIs used in the code are correct and working.

### Integration Testing

1. Testing rate limits for MBTA API used in the code

### Data Integrity

- Validate API response with real MBTA data.

## Observability

1. Logging
   1.1 Log API status and error message
   1.2 Return proper error messages and status code

2. Monitoring
   2.1 Monitor performance metics like RPS (request per second), Response Time, Number of failed requests, etc.
   2.2 Set up alert on API failures above certain threshold, or average response time above certain limit.

## Release Process

1. Branching and code review: feature, main branch. PR review.
2. Set up Dev, QA, Staging, Production environment.
   Developer finishes development and pushes code to QA, QA verify the API endpoints. If no issue found, code can be pushed to Staging env and waiting for production deployment. If found any issues, QA notifies developer and creates bug ticket for developer.
3. CI/CD pipeline.

## Stakeholders

1. Public user who will use this information for commute.
2. QA who will validate the information.
3. Developers who will use API endpoints to develop software
