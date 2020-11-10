rm -rf migrations ;
rm -rf flask_boilerplate_main.db;
python manage.py db init;
python manage.py db migrate;
python manage.py db upgrade;
