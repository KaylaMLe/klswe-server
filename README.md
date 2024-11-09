# Back end for [klswe.com](https://www.klswe.com)
My personal website is a centralized platform to display my professional portfolio, projects, and expertise, offering a comprehensive view of my skills and interests. With a strong emphasis on user experience, scalability, and maintainability, it provides an engaging way to explore my work and connect with me. I hope you have as much fun exploring the code as I have building it!

## Table of contents

1. [About this repository](#about-this-repository)
2. [Getting started](#getting-started)
      - [Prerequisites](#prerequisites)
      - [Installation](#installation)
      - [Running the project](#running-the-project)
      - [Testing](#testing)
3. [Project design](#project-design)
      - [Architecture](#architecture)
      - [Dependencies](#dependencies)
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
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html): used to securely access secrets. Authentication can be done via an attached IAM role if the application is run on an EC2 instances or an IAM user logged in to the CLI.

### Installation

### Running the project

### Testing

## Project design

### Architecture

### Dependencies

### File system
```
📁klswe-server/
├─📁.github/
│ └─📁workflows/
│   └─📜cicd.yml - GitHub Actions script for automated testing and deployment
└─📁.venv/
```

## License
This project is open-source and licensed under the MIT License. This license allows for free use, modification, and distribution with attribution to the original author. Please review `LICENSE.txt` for specific terms and conditions.
