import time

import mariadb
from fastapi import FastAPI

from . import models
from .database import engine
from .routes import post, user, auth

# Create all SQL Models
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Connect to MariaDB
while True:
    try:
        conn = mariadb.connect(
            host="localhost",
            database="fcc_fastapitut",
            user="admin",
            password="root",
        )
        # Setting dictionary true to see column names
        cursor = conn.cursor(dictionary=True)
        print("Connected to MariaDB")
        break

    except Exception as e:
        print("Error connecting to database")
        print("Error: ", e)
        time.sleep(2)


# * Routes * #
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
