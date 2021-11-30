# car-rentals
CRUD APIs to search and rent a car on available dates

This repo contains APIs for following flows:
1. Add/Get cities
2. Add/Get rental zones in a city
3. Add/Get cars in a city
4. Search for cars in a city on any date
5. Book a car for rent on any of the available dates upto next 60 days

####Note: API specifications are present in the json file (shared on email)


Prerequisites - 
1. Postgres
2. Python version 3.6.8
3. virtualenv
4. redis


## Installation Steps
1. Clone the repo
2. Move to the repo
   1. `cd car-rental`
3. Create .env and test.env files
   1. create 2 database (`car-db`, `test-db`) and save the connection string in these files
   `DATABASE_URL`
   `REDIS_URL`
4. Create, activate virtualenv, install requirements
   1. `virtualenv -p /path/to/python_bin venv`
   2. `source venv/bin/activate`
   3. `pip install requirements.txt`
5. Migrate db_schema, pre-seed cities
   1. `python -m app.db_migration`
   2. `psql -d car-db < app/database/city.sql`
6. Start the API, CELERY Worker and Beat
   1. `honcho start web worker cron`


## Run tests
To run unit tests - test.env needs to be present in the repo
1. `APP_ENV=TEST pytest`


   
