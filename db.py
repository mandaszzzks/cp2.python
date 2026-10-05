import os

import mysql.connector
from pymongo import MongoClient


def mysql_conn():
    con = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
    )
    con.cursor().execute("CREATE DATABASE IF NOT EXISTS lab")
    con.database = "lab"
    return con


def mongo_db():
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(uri, serverSelectionTimeoutMS=3000)["lab"]