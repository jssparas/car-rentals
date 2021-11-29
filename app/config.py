from dotenv import find_dotenv, load_dotenv
from os import environ as env


app_env = env.get('APP_ENV')
if app_env:
    if app_env.upper() == 'TEST':
        env_file = '../test.env'
else:
    env_file = '.env'

env_file = find_dotenv(env_file)
load_dotenv(env_file)

DATABASE_URL = env.get('DATABASE_URL')
