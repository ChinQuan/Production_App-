
import psycopg2
from decouple import config

def get_connection():
    conn = psycopg2.connect(
        host=config("DB_HOST"),
        database=config("DB_NAME"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        port=config("DB_PORT")
    )
    return conn

