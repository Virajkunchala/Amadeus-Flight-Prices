# Pathfinder - Amadeus Flight Application

This application interacts with the Amadeus Travel API to fetch live flight prices. It is built using Django and Docker, and It features automatic token management and caching with Redis to enhance performance.


## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.11 or higher (for local development)
- Redis (Only if running locally without Docker)

## Assumptions Made in Development

1. **Environment Variables**: Sensitive data such as `AMADEUS_API_KEY` and `AMADEUS_API_SECRET` are assumed to be stored in a `.env` file located in the root directory.

2. **Django Version**: The application is developed with Django version 3.2 or higher.

3. **Redis**: Redis is used as a caching layer for managing API responses and access tokens.

4. **Docker**: Docker and Docker Compose are utilized for containerization and orchestration.



### Token Management with nocache=1
Whenever a user includes the nocache=1 parameter in the API request, the application fetches a new access token from the Amadeus API, regardless of whether the previous token has expired. This behavior ensures that users always receive the most up-to-date flight information, enhancing the reliability of the data provided by the application. The automatic token management feature allows for seamless interaction with the Amadeus API without requiring manual intervention.


### Access Token Management
The application automatically manages the OAuth2 access token required for the Amadeus API. The AmadeusAPI class handles fetching and refreshing the access token. It caches the token and its expiry time using Redis, ensuring that no manual token refresh is needed during testing. When a request is made to fetch flight offers, the application checks if the current token is still valid and fetches a new one if necessary.


### Installation
1. Create a .env file in the root directory and add your Amadeus API credentials.
 ``` bash
   AMADEUS_API_KEY=<your-amadeus-api-key>
   AMADEUS_API_SECRET=<your-amadeus-api-secret>

  ```

2. **Install requirements locally (if needed):**: 
 ```bash 
 pip install -r requirements.txt
  ```

### Running the Application
1. Build and start the containers.
 ``` bash
   docker-compose up --build

  ```

2. **Access the application:**: 
Open your browser and navigate to http://localhost:8000.

## Docker and Redis Setup
The Docker Compose setup automatically includes a Redis container, so there's no need to install Redis separately if you're running the application using Docker. This ensures that caching and token management work seamlessly out of the box. Simply follow the steps above to start the application, and Redis will be set up and ready to use.

Stopping the Application
To stop the application and remove the containers:
 ``` bash

docker-compose down

  ```
### Testing the Application
You can test the API using `curl` or a similar tool. Once the application is running, you can access the following endpoints:


Ping: http://localhost:8000/api/ping/

 ```bash

curl -X GET http://localhost:8000/api/flights/ping/

  ```


You should receive a response like this:

 ``` json

{
    "data": "pong"
}

```


Health Check: http://localhost:8000/api/flights/health/

```bash

curl -X GET http://localhost:8000/api/flights/health/

  ```

 ``` json

{
    "status": "healthy"
}

```



Fetching Flight Offers
To fetch live flight offers, use the following commands:

With caching:
 ``` bash


curl "http://localhost:8000/api/flights/price?origin=JFK&destination=LAX&departureDate=2024-12-01"

 ``` 

Without caching (using nocache=1):

 ``` bash


curl "http://localhost:8000/api/flights/price?origin=JFK&destination=LAX&departureDate=2024-12-01&nocache=1

 ``` 

Sample response:

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
 ``` json

{
    "data": {
        "originLocationCode": "JFK",
        "destinationLocationCode": "HYD",
        "departureDate": "2024-12-01",
        "price": "47574.00 INR"
    }
}

 ```

**Configuration**
The application requires specific API endpoint configurations for the Amadeus API. These settings can be found in the config/settings/base.py file:
Host URL: [Enter the specific host URL here, e.g., https://test.api.amadeus.com]
Token URL: [Enter the specific token URL here, e.g., https://test.api.amadeus.com/v1/security/oauth2/token]
Ensure these URLs are set correctly based on your environment and requirements.

**Local and Production Settings**
The application includes separate configuration files in the config/settings/ directory to cater to different environments. By default, the system uses the local environment configuration. Make sure to review and modify these files according to your deployment needs.