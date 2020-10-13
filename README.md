# Flask Boilerplate

[![Flask--RESTPlus](https://img.shields.io/badge/Flask--RESTPlus-0.13.8-green)](https://flask-restplus.readthedocs.io/en/stable/) [![Flask-JWT-Extended
](https://img.shields.io/badge/Flask--JWT--Extended-3.24.1-orange)](https://flask-jwt-extended.readthedocs.io/en/stable/)

Flask Boilerplate is a starting point for Rest API. This project is configured with Flask-RestPlus ( include Swagger), SQLAlchemy and Flask-JWT-Extended.

<p float="left">
<a href='https://flask.palletsprojects.com/en/1.1.x/'><img src='https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png' height='60' alt='Flask' aria-label='Flask' /></a>
<a href='https://swagger.io/'><img src='https://static1.smartbear.co/swagger/media/assets/images/swagger_logo.svg' height='60' alt='Swagger' aria-label='Swagger' /></a>
<a href='https://flask-jwt-extended.readthedocs.io/en/stable/'><img src='https://res.cloudinary.com/djeghcumw/image/upload/v1562125444/blog/authentication-jwt-nodejs-logo.png' height='60' alt='Flask-JWT-Extended' aria-label='Flask-JWT-Extended' /></a>

</p>

### 1. Install packages

```bash
pip install -r requirements.txt
```

### 2. Initiate a migration folder using `init` command for alembic to perform the migrations.

```bash
python manage.py db init
```

### 3. Create a migration script from the detected changes in the model using the `migrate` command. This doesn’t affect the database yet.

```bash
python manage.py db migrate --message 'initial database migration'
```

### 4. Apply the migration script to the database by using the `upgrade` command

```bash
python manage.py db upgrade
```

### Config ENV in file `config.ini`
