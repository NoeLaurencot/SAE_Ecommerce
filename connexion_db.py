from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from dotenv import load_dotenv
import os
import pymysql.cursors

load_dotenv()
db_login = os.environ["DB_LOGIN"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_host,
            user=db_login,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db