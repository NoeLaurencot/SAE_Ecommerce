from flask import g
from dotenv import load_dotenv
import os
import pymysql.cursors
import certifi

load_dotenv()
db_login = os.environ["DB_LOGIN"]
db_name = os.environ["DB_NAME"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = int(os.environ["DB_PORT"])

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_host,
            user=db_login,
            password=db_password,
            database=db_name,
            port=int(db_port),
            charset='utf8mb4',
            ssl_ca=certifi.where(),
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db
