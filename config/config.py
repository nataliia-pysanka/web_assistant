import pathlib
from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).parent.parent
config = dotenv_values(".env")

DB = config['POSTGRES_DB']
DB_USER = config['POSTGRES_USER']
DB_PASSWORD = config['POSTGRES_PASSWORD']
DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']


class Config:
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@' \
                              f'{DB_HOST}/{DB}'
    SECRET_KEY = config['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = True