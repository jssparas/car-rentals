from dotenv import find_dotenv, load_dotenv
from os import environ as env

env_file = find_dotenv('.env')
load_dotenv(env_file)

DATABASE_URL = env.get('DATABASE_URL')
