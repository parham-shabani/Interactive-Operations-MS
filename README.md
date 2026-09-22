# Interactive Operations Microservice

Interactive Operations is a Django-based microservice responsible for managing user and entity interactions within the platform.

The service provides APIs for handling social and interactive actions such as following, liking, disliking, sharing, and scoring between different types of actors and targets.

## Features

- Follow and unfollow actors or entities
- Retrieve followers and followings
- Like and unlike content or entities
- Retrieve likers and likees
- Dislike and remove dislikes
- Retrieve dislikers and dislikees
- Share content across supported platforms
- Manage and retrieve interaction scores
- OAuth2-based authentication
- Role-based access control
- Actor identity validation based on authenticated users
- RESTful API endpoints
- Automatic database migrations
- OpenAPI / Swagger API documentation

## Technology Stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **OAuth2**
- **drf-spectacular**
- **Docker**
- **GitLab CI/CD**

## Project Structure

InteractiveoperationsMS/
├── InteractiveOperations/
│   ├── models/
│   ├── serializers/
│   ├── views/
│   ├── urls.py
│   └── ...
├── core/
├── ipc/
├── requirements/
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── ...
API Endpoints

The main API endpoints are available under the following prefix:

/interactive-ops/
Follow
POST /interactive-ops/follow
GET  /interactive-ops/follow/followers
GET  /interactive-ops/follow/followings
Like / Dislike
POST /interactive-ops/like
GET  /interactive-ops/like/likers
GET  /interactive-ops/like/likees
GET  /interactive-ops/like/dislikers
GET  /interactive-ops/like/dislikees
Share
POST /interactive-ops/share
Score
GET /interactive-ops/score
Authentication

The service uses OAuth2 Bearer Token authentication.

Authenticated requests must include an access token in the Authorization header:

Authorization: Bearer <access_token>

The authenticated actor is obtained from the Bearer Token rather than being trusted solely from request parameters.

For operations that contain actor_type and actor_id, the provided actor identity is validated against the authenticated user. This prevents an authenticated user from performing an operation on behalf of another actor.

Actor and Target Model

Interactive Operations supports interactions between different types of actors and targets.

Each interaction can contain information such as:

actor_type
actor_id
target_type
target_id

The actor represents the authenticated entity performing the operation, while the target represents the entity on which the operation is performed.

API Documentation

The service provides automatically generated OpenAPI documentation using drf-spectacular.

Swagger UI
/api/schema/swagger-ui/
OpenAPI Schema
/api/schema/
ReDoc
/api/schema/redoc/
Running the Project
Using Docker

Build and start the services with:

docker compose up --build

The application and PostgreSQL database are started as separate containers.

Running Django Locally

Install the required dependencies:

pip install -r requirements/development.txt

Apply database migrations:

python manage.py migrate

Start the development server:

python manage.py runserver
Database

The service uses PostgreSQL as its primary database.


This project is intended for internal use within the platform and is not currently distributed as a public open-source project.
