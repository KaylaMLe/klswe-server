# Back end for [klswe.com](https://www.klswe.com)
My personal website is a centralized platform to display my professional portfolio, projects, and expertise, offering a comprehensive view of my skills and interests. With a strong emphasis on user experience, scalability, and maintainability, it provides an engaging way to explore my work and connect with me. I hope you have as much fun exploring the code as I have building it!

## Table of contents

1. [About this repository](#about-this-repository)
2. [Getting started](#getting-started)
      - [Prerequisites](#prerequisites)
      - [Set up](#set-up)
      - [Running the project](#running-the-project)
        - [Development server](#development-server)
        - [Gunicorn](#gunicorn)
      - [Testing](#testing)
3. [Project design](#project-design)
      - [Architecture](#architecture)
      - [Dependencies](#dependencies)
        - [Core framework](#core-framework)
        - [Database and deployment](#database-and-deployment)
        - [Cloud services](#cloud-services)
      - [File system](#file-system)
4. [License](#license)

## About this repository
This Django project is designed to support dynamic and secure interactions with my personal website. It includes apps for CSRF token management and traffic tracking, along with dedicated apps to manage data and functionality for various projects displayed on the frontend.

## Getting started
This section provides an overview of the process to run the project, including installation steps and running/testing instructions.

### Prerequisites
Before setting up the project, ensure you have the following installed on your machine:
- [Python ^3.10](https://www.python.org/downloads/): required for compatibility with Django 5.0 and various other dependencies
- [pip ^21.3](https://packaging.python.org/en/latest/tutorials/installing-packages/):  required to install the dependencies
- [PostgreSQL 17](https://www.postgresql.org/docs/17/tutorial-install.html): the database used in production. If you want to run the project with the Django default database, SQLite, change the `DATABASES` setting in `mysite\mysite\settings.py` to the following.
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Set up
1. Clone the repository.
```
git clone https://github.com/KaylaMLe/klswe-server.git
cd klswe-server
```
2. Set up a virtual environment.
```
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```
3. Install the required packages listed in the `.venv/requirements.txt` file.
```
pip install -r .venv/requirements.txt
```
4. Create a `.env` file in the root directory.
```
vim .env # Use your preferred text editor to open a new document.
```
5. Add the following environment variables to the `.env` file.
- `AWS_REGION=<AWS region code (e.g., us-east-1, eu-west-2)>`
    - specifies region where the authenticated AWS Secrets Manager is located
- `DEBUG=<"True" or "False">`
    - enables more detailed error messages from Django
- `DEV_MODE=<"True" or "False">`
    - toggles between production and development secrets values and GCP authentication methods
- `GCP_REGION=<GCP region code (e.g., us-central1, europe-west1)>`
    - determines the GCP region used for Vertex AI
- `HOST=<comma-separated list of IP addresses and/or domain names>`
    - restricts servers responses to specific approved hosts
- `LOG_PATH=<file path>`
    - defines location of AWS Secrets Manager ClientError logs
- `MODEL_ID=<Model Garden model resource name>`
    - specifies the model to use for prompting
6. Configure secrets management. If you choose to use AWS Secrets Manager, secret names and keys throughout the repository should match the secrets you create.
7. (Optional) Set up the database if you use PostgreSQL. Add the database name, user, password, and port to your chosen secret management method.

### Running the project
1. Activate the virtual environment.
```
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```
2. Change directories to the project folder to simplify later commands.
```
cd mysite
```
3. Ensure all database migrations are applied before starting the server.
```
python manage.py migrate
```
The project can now be run with Django's built-in server for testing during development or with Gunicorn for production.

#### Development server
Start the development server. The terminal output will specify the port at which the server can be accessed.
```
python manage.py runserver
```

#### Gunicorn
Use Gunicorn with the provided gunicorn_config.py file to start the server.
```
gunicorn --config gunicorn_config.py mysite.wsgi
```

### Testing
1. Activate the virtual environment and change directories to the project folder.
```
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
cd mysite
```
2. Run tests.
- Use the below command to run all tests.
```
python manage.py test
```
- To test a specific Django app, specify the app's name as defined in its `apps.py`.
```
python manage.py test <app name>
```

## Project design

### Architecture
This backend application uses RESTful API endpoints to receive inputs from the frontend and return processed data, ensuring that core processing, authentication, and data validation are handled server-side. Each Django app is designed for specific functionality, such as CSRF token management, traffic tracking, or supporting project-specific data, enabling modular and maintainable development. This architecture allows the frontend to delegate complex tasks to the backend, ensuring efficient, scalable data processing and secure interaction handling.

### Dependencies
All dependencies and the appropriate version numbers are listed in `.venv\requirements.txt` and are installed during virtual environment setup. Below are key dependencies categorized by functionality, with the official package names in parentheses.

#### Core framework
- Django (`Django`): the primary framework for building and managing this backend
- Django Rest Framework (`djangorestframework`): extends Django with additional support for building RESTful APIs

#### Database and deployment
- PostgreSQL Adapter (`psycopg2-binary`): provides PostgreSQL database connectivity
- Gunicorn (`gunicorn`): a WSGI server for deploying the Django application in production
- Django CORS Headers (`django-cors-headers`): manages Cross-Origin Resource Sharing (CORS) policies, allowing secure cross-origin requests only from trusted frontend domains

#### Cloud services
- AWS SDK for Python (`boto3`): used to interact with AWS Secrets Manager for securely managing sensitive information
- Google Cloud AI Platform (`google-cloud-aiplatform`): enables interactions with Google Cloud’s Vertex AI for generative AI usage
- Google Cloud Storage (`google-cloud-storage`): supports Google Cloud Storage interactions, allowing storage and retrieval of large files or model artifacts
- Google API Client (`google-api-python-client`): a core library for making requests to Google APIs
- Google Auth (`google-auth`): provides authentication support for accessing Google APIs securely

### File system
This file structure section highlights the essential directories and files needed to understand the project’s core functionality, omitting standard Django files and temporary or auto-generated files for simplicity. Directories that contain numerous files serving a single purpose are summarized to maintain clarity. Additionally, specialized apps for specific frontend features are grouped under “various apps” to distinguish them from general utility apps.
```
📁klswe-server/
├─📁.github/
│ └─📁workflows/
│   └─📜cicd.yml - GitHub Actions script for automated testing and deployment
├─📁.venv/ - virtual environment files
│ └─📜requirements.txt - lists necessary dependencies
└─📁mysite/ - primary Django project folder
  ├─📁csrf_setter/ - app for providing CSRF tokens to the frontend
  ├─📁mysite/ - core configuration folder for the Django project, containing essential settings, routing, and deployment files
  ├─📁traffic_tracker/ - app for incrementing page visit and form submission counts
  ├─📁utils/ - shared utility functions across apps
  ├─📁various apps - provide backend functionality for specific frontend pages
  ├─📜gunicorn_config.py - configuration file for Gunicorn in production
  └─📜manage.py - Django command-line utility
```

## License
This project is open-source and licensed under the MIT License. This license allows for free use, modification, and distribution with attribution to the original author. Please review `LICENSE.txt` for specific terms and conditions.
