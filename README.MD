# Coderr Backend

This is the backend of the Coderr project built with **Django** and **Django REST Framework**.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## Requirements

- Python 3.11+  
- pip (Python package manager)  
- Virtualenv (recommended)  
- SQLite (default) or PostgreSQL for production

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VeyselKaraali/Coderr_Backend.git
cd coderr-backend
```

### 2. Create a virtual environment
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Variables
Create a ```.env``` file in the root directory and add the following:
```bash
SECRET_KEY=<your_secret_key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=<comma_separated_list_of_allowed_origins>

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=coderrdb
DB_USER=coderr_user
DB_PASSWORD=<your_password>
DB_HOST=localhost
DB_PORT=5432
```
**Note:** If you plan to use PostgreSQL, update ```DB_ENGINE```, ```DB_NAME```, ```DB_USER```, ```DB_PASSWORD```, ```DB_HOST```, and ```DB_PORT``` accordingly.

## Database Setup
### 1. Make migrations
```bash
python manage.py makemigrations
```

### 2. Apply migrations
```bash
python manage.py migrate
```

### 3. (Optional) Create a superuser
```bash
python manage.py createsuperuser
```

## Running the Project
```bash
python manage.py runserver
```
The backend will be available at ```http://127.0.0.1:8000/```.

## Running Tests
To run all tests with pytest:
```bash
pytest
```

For code coverage:
```bash
pytest --cov=.
```

HTML report will be generated in ```htmlcov/```.

## License
This project is licensed under the MIT License.