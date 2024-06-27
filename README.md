# EcoTrack

EcoTrack is a Django-based environmental data aggregation platform that fetches and processes air quality and weather data from various sources.

## Features

- Fetches data from OpenAQ and OpenWeatherMap APIs
- Stores environmental metrics, locations, and time series data
- Provides API endpoints for current, historical, and aggregated data
- Uses GeoDjango for spatial queries
- Implements Celery for task queuing and scheduling
- Utilizes Redis for caching
- Includes comprehensive API documentation using drf-yasg

## Setup

1. Clone the repository:
`git clone https://github.com/yourusername/ecotrack.git`
`cd ecotrack`

2. Create a `.env` file in the project root and add the necessary environment variables (see `.env` example above).

3. Build and run the Docker containers:
`docker-compose up --build`
4. Run migrations:
`docker-compose exec web python manage.py migrate`
5. Create a superuser:
`docker-compose exec web python manage.py createsuperuser`
## Usage

- Access the admin interface at `http://localhost:8000/admin/`
- View API documentation at `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`
- Use the provided API endpoints to fetch and analyze environmental data

## Running Tests

To run the tests, use the following command:
`docker-compose exec web python manage.py test`
## License

This project is licensed under the MIT License.