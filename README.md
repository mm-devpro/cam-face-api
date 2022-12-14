# cam-face-api
# Backend authentication module

###Description
It's an authentication module made with FLASK / SQLALCHEMY / MARSHMALLOW in order to manage 
login/logout/submit from front.
It checks if user is in the database and if credentials are good, then sends a token (handle with 
werkzeug.security for the hash, and jwt for the token) to cookie.


### Prerogatives
1) Create a virtual env from command line 
```python
python -m venv venv
```
2) Activate the environment
```python
.\venv\Scripts\activate
```
3) Install the required package from command line
```python
pip install -r .\requirements.txt
```
4) Create a .env file at root of the project and set variables
```python
DB_USER="root"
DB_PWD=""
SECRET_KEY="put_your_own_secret_key"
JWT_SECRET_KEY="put_your_own_jwt_secret_key"
MYSQL_URL="url_to_your_db_127.0.0.1"
MYSQL_DB="cam_db"
MYSQL_PORT='3306'
```
5) Create a database inside mysql (with PHPMYADMIN for example, 
DB_USER and DB_PASSWORD must be your credentials to access it)
6) From command line set FLASK environment variables
```python
$env:FLASK_ENV="development"
$env:FLASK_APP="api.py"
```
7) Set your database collections from command line

```python
python
from database import db
from app import create_app

db.create_all(app=create_app())
```
8) You are ready to play with your cam api