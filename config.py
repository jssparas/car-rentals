# # config variables are specified in .env according to environment.
# from distutils.util import strtobool
# from os import environ as env
# from datetime import datetime
# import os
# # from pathlib import Path
# from dotenv import load_dotenv, find_dotenv
#
#
# app_env = env.get('APP_ENV')
# if app_env:
#     if app_env.upper() == 'TEST':
#         env_file = 'test.env'
# else:
#     env_file = '.env'
#
# # load config from .env file
# load_dotenv(find_dotenv(env_file), override=True)
#
# DATABASE_URL = base64.b64decode(env.get('DATABASE_URL')).decode()