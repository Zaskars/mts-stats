import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'postgresql+psycopg2://postgres:72metra@localhost:5432/mts'

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
