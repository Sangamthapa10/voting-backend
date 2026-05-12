import os
import dj_database_url
from decouple import config

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.onrender.com').split(',')
