# car-rentals
CRUD APIs to search and rent a car on available dates

This repo contains APIs for following flows:
1. Add/Get cities
2. Add/Get rental zones in a city
3. Add/Get cars in a city
4. Search for cars in a city on any date
5. Book a car for rent on any of the available dates upto next 60 days


Prerequisites - 
1. Postgres
2. Python version 3.6.8
3. virtualenv
4. redis


## Installation Steps
1. Clone the repo
2. Creeate .env file and test.env files with following lines
    `DATABASE_URL=postgresql://paras:postgres@localhost:5432/<db-name>`
    `REDIS_URL=redis://localhost:6379/1`
  Note: db-name should be different for both files
3. 
