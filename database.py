import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
