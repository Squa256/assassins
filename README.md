# Assassins

## Setting up the project

### Database setup

```
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev
sudo su - postgres
createdb assassinsdb
createuser -P assassin
(follow prompts)
psql
GRANT ALL PRIVILEGES ON DATABASE assassinsdb TO assassin;
```

Now you have a PostgreSQL database named 'assassinsdb' and a user named 'assassin' with full privileges.

### Django project & environment setup

Make sure you have Python 3.4 and virtualenv installed.
Run the following commands from the project's root directory.

```
virtualenv -p /usr/bin/python3.4 env
source env/bin/activate
pip install -r requirements.txt
```

Now make a Django settings file for your development environment.

```
cd assassins/assassins
cp default_settings.py settings.py
```

In the new settings file, change the DATABASES password to match the one you made above.
Other settings would need to be changed for the production server (SECRET_KEY, ALLOWED_HOSTS, DEBUG), but they're fine as they are for development.

To test if it's working, run the following commands then go to 127.0.0.1:8000 in your browser.

```
cd ..
python manage.py migrate
python manage.py runserver
```

Wooooo
