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
