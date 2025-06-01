## Objectives

Deliver accurate subway stop information from API endpoints. Ensure all endpoints are easy to use and return accurate, structured responses.

## Scope

1. Integrate API endpoints with official MBTA API.
2. Only focus on (light and heavy trail) subway stop.

## Testing

### Unit Testing

1. Business logic validation

- Verify core functionalities, such as extracting GPS coordinates, mapping subway lines, and retrieving adjacent stops.
- Create test cases using mocked response to ensure the API returns expected results.
- Test edge cases, such as:
  - stops without adjacent stops
  - Deprecated or invalid routes/stops

2. MBTA API Integration

- Confirm that all MBTA endpoints used in the code are valid and return expected data.

### Integration Testing

1. API rate limiting

- Validate application behavior under MBTA API rate limiting conditions.
- Ensure error handling are in place.

### Data Integrity

- Cross-check and validate API responses against real MBTA data to ensure accuracy and consistency.

## Observability

1. Logging

   - Log API request/response status and relevant error messages
   - Ensure all error responses include appropriate HTTP status codes and clear messages.

2. Monitoring
   - Track key performance metrics such as:
     - Requests per second (RPS)
     - Response time
     - Failure rates
   - Set up alerts for:
   - API failure rates exceeding a defined threshold
   - Average response time exceeding acceptable limits

## Release Process

1. Follow a clear Git branching model using feature, main and release branch. All code changes go through PR reviews.

2. Set up Dev, QA, Staging, Production environment.
   - Developers push completed features to the QA environment.
   - QA validates endpoints. If issues are found:
   - QA files bug reports.
   - Developers fix issues and resubmit for QA.
   - Upon approval, code is promoted to staging, then to Production.
3. Build CI/CD pipeline.

- Set up automated pipelines for building, testing, and deploying code across environments.

## Stakeholders

1. Public users - Rely on the subway information for daily commutes.
2. QA - Validate API functionality, performance and accuracy.
3. Developers - Build and maintain the API and ensure long-term reliability and scalability.
