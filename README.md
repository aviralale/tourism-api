# Django Tour & Event Management System

## Overview

This project is a Django-based web application designed for managing tours and events. It supports different user roles such as tourists, guides, and event managers, each with specific functionalities.

## Features

- User Registration and Authentication
- Profile Management for Users, Guides, and Event Managers
- Tour and Event Creation and Management
- Rating System for Guides and Event Managers
- Booking System for Tours and Events

## Setup

### Prerequisites

- Python 3.6+
- Django 3.0+
- PostgreSQL (or any preferred database)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/django-tour-event-management.git
    cd django-tour-event-management
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the database:**
    Update your `settings.py` to configure the database settings.
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'yourdbname',
            'USER': 'yourdbuser',
            'PASSWORD': 'yourdbpassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. **Run migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

8. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000/`.

## API Endpoints

### User Registration and Authentication

- **Signup:** `POST /api/users/signup/`
- **Login:** `POST /api/users/login/`
- **Logout:** `POST /api/users/logout/`

### User Profile

- **Get Profile:** `GET /api/users/profile/`
- **Update Profile:** `PUT /api/users/profile/`

### Tours

- **Create Tour:** `POST /api/tours/`
- **List Tours:** `GET /api/tours/`
- **Get Tour:** `GET /api/tours/{id}/`
- **Update Tour:** `PUT /api/tours/{id}/`
- **Delete Tour:** `DELETE /api/tours/{id}/`

### Events

- **Create Event:** `POST /api/events/`
- **List Events:** `GET /api/events/`
- **Get Event:** `GET /api/events/{id}/`
- **Update Event:** `PUT /api/events/{id}/`
- **Delete Event:** `DELETE /api/events/{id}/`

## Models

### User

- **CustomUser**
- **CustomUserProfile**
- **Tourist**
- **Guide**
- **EventManager**

### Tours

- **Tour**
- **TouristCompletedTour**

### Events

- **Event**
- **EventCompleted**

### Ratings

- **GuideRating**
- **EventManagerRating**

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes. Make sure to follow the code style and include tests for your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Django Rest Framework Documentation: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
