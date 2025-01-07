# 🎭 Theater API

Comprehensive theater management system - RESTful API service for managing performances, theater halls, plays, actors, and ticket reservations.

---

## 📋 Table of Contents
- [🌐 Overview](#-overview)
- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [💻 System Requirements](#-system-requirements)
- [🚀 Installation](#-installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [🔐 Environment Variables](#-environment-variables)
- [📚 API Documentation](#-api-documentation)
- [🗄 Database Structure](#-database-structure)
- [🧪 Testing](#-testing)
- [🔧 Troubleshooting](#-troubleshooting)
- [📝 API Examples](#-api-examples)

---

## 🌐 Overview

Theater API is a powerful theater management system that provides functionality for managing theaters, plays, performances, actors, and ticket reservations. This system is designed to handle ticket booking, performance scheduling, and user authentication, allowing seamless management of theater operations.

---

## ✨ Features

### Theater Hall Management
- Create and manage theater halls with seating capacity.
- View theater hall details, including rows, seats, and capacity.

### Performance Management
- Create and manage performances.
- Schedule performances with assigned theater halls and plays.
- Query performances based on showtime or play.

### Play Management
- Add and manage plays with descriptions, genres, and actors.
- Upload and manage play images.

### Ticket Reservation System
- Reserve tickets for specific performances.
- Ensure seat availability based on theater hall capacity.
- View user reservations.

### Actor and Genre Management
- Manage genres and actors involved in plays.
- List and retrieve detailed information about actors.

### Additional Features
- JWT Authentication for secure access.
- API throttling for rate-limiting.
- Swagger and Redoc API documentation for easy exploration.
- Automated testing for reliability.

---

## 🛠 Tech Stack

- **Backend**: Python 3.12, Django 5.1, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT
- **Documentation**: Swagger/Redoc

---

## 💻 System Requirements

- Python 3.12+
- PostgreSQL 15+
- Docker & Docker Compose

---

## 🚀 Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mshmygel/theater.git
   cd theater_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:
   ```bash
   cp .env.sample .env
   ```

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Load sample data (optional):
   ```bash
   python manage.py loaddata test_data.json
   ```

7. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Access the app at:
   - API: http://localhost:8000/api/theater/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/doc/swagger/

### Docker Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mshmygel/theater.git
   cd theater_api
   ```

2. Create .env file:
   ```bash
   cp .env.sample .env
   ```

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Create a superuser inside the Docker container:
   ```bash
   docker-compose exec app python manage.py createsuperuser
   ```

5. Access the app at:
   - API: http://localhost:8001/api/theater/
   - Admin Panel: http://localhost:8001/admin/
   - API Documentation (swagger): http://localhost:8001/api/doc/swagger/
   - API Documentation (redoc): http://localhost:8001/api/doc/redoc/

## 🔐 Environment Variables

Define the following variables in the .env file:

```env
# Database settings
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=theater
POSTGRES_USER=theater
POSTGRES_PASSWORD=theater
PGDATA=/var/lib/postgresql/data

# Django settings
DJANGO_SECRET_KEY=your-secret-key
ENVIRONMENT=local
DEBUG=True
```

## 📚 API Documentation

The API documentation is available at:
- Swagger: http://localhost:8000/api/doc/swagger/
- Redoc: http://localhost:8000/api/doc/redoc/

## 🗄 Database Structure

The project includes the following main models:

- User: Handles user accounts and authentication.
- TheaterHall: Stores theater hall details.
- Genre: Defines genres for plays.
- Actor: Stores actor information.
- Play: Manages play details, genres, and actors.
- Performance: Manages scheduled performances in theater halls.
- Reservation: Handles ticket reservations for performances. Each reservation contains a list of tickets.
- Ticket: Represents individual seat bookings but is managed internally through reservations.

## 🧪 Testing

Run tests using:

```bash
python manage.py test
```

## 🔧 Troubleshooting

### Common Issues

1. Database Connection Errors
   - Ensure PostgreSQL is running.
   - Verify database credentials in the .env file.
   - Apply migrations using `python manage.py migrate`.


## 📝 API Examples

### User Registration

#### Register a new user
```bash
curl -X POST http://localhost:8000/api/user/register/ \
    -H "Content-Type: application/json" \
    -d '{"email": "user@example.com", "password": "password"}'
```

### Authentication

#### Get an access token
```bash
curl -X POST http://localhost:8000/api/user/token/ \
    -H "Content-Type: application/json" \
    -d '{
        "email": "user@example.com",
        "password": "password"
    }'
```
#### Refresh a token
```bash
curl -X POST http://localhost:8000/api/user/token/refresh/ \
    -H "Content-Type: application/json" \
    -d '{
        "refresh": "<refresh_token>"
    }'
```

### Performances

Get a list of performances:

```bash
curl -X GET http://localhost:8000/api/theater/performances/ \
    -H "Authorization: Bearer <your_token>"
```

Reserve a ticket:

```bash
curl -X POST http://localhost:8000/api/theater/reservations/ \
    -H "Authorization: Bearer <your_token>" \
    -H "Content-Type: application/json" \
    -d '{
        "tickets": [
            {
                "performance": 1,
                "row": 1,
                "seat": 3
            },
            {
                "performance": 1,
                "row": 1,
                "seat": 4
            }
        ]
    }'
```