#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import requests
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles

# import boto3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "ngx3fy" 

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.


# The zone apex is the 'default' page for a URL
# This will return a simple hello world via GET method.
@app.get("/")  # zone apex
def read_root():
    return {"Hello": "World"}

@app.get("/github/repos/{user}")
def github_user_repos(user):
    url = "https://api.github.com/users/" + user + "/repos"
    response = requests.get(url)
    body = json.loads(response.text)
    return {"repos": body}

# Endpoints and Methods
# /blah - endpoint
# GET/POST/DELETE/PATCH - methods
# 
# Simple GET method demo
# Adds two integers as PATH parameters
@app.get("/add/{number_1}/{number_2}")
def add_me(number_1: int, number_2: int):
    sum = number_1 + number_2
    return {"sum": sum}

# Let's develop a new one:
@app.get("/divide/{number_1}/{number_2}")
def divide_me(number_1: int, number_2: int):
    div = number_2 / number_1
    return {"quotient": div}

@app.get("/subtract/{number_1}/{number_2}")
def minus_me(number_1: int, number_2: int):
    difference = number_1 - number_2
    return {"difference": difference}

@app.get("/name")
def sample_message(name: str):
    Fname = name
    return {"Goodbye": Fname }

@app.get("/PEMDAS")
def divide_add_me(number_3: int, number_4: int, number_5:int):
    answer = (number_3 + number_5)/(number_4)
    return {"answer": answer}

@app.get("/meal")
def food_groups(veg1: str, fruit1: str, protein1: str, dairy1: str, grain1: str):
    meal = veg1 + ", " + fruit1 + ", " + protein1 + ", " + dairy1 + ", and " + grain1
    return {"A balanced meal could include": meal}

@app.get("/albums")
def find_albums():
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("""SELECT * FROM albums ORDER BY name""")
    results = c.fetchall()
    db.close()
    return results

@app.get("/albums/{id}")
def get_one_album(id):
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM albums WHERE id=" + id)
    results = c.fetchall()
    db.close()
    return results

## Parameters
# Introduce parameter data types and defaults from the Optional library
@app.get("/items/{item_id}")
def read_items(item_id: int, q: str = None, s: str = None):
    # to-do: could be used to read from/write to database, use item_id as query parameter
    # and fetch results. The q and s URL parameters are optional.
    # - database
    # - flat text
    # - another api (internal)
    # - another api (external)
    return {"item_id": item_id, "q": q, "s": s}


## Data Modeling
# Model data you are expecting.
# Set defaults, data types, etc.
#
# Imagine the JSON below as a payload via POST method
# The endpoint can then parse the data by field (name, description, price, tax)
# {
#     "name":"Trek Domaine 5000",
#     "description": "Racing frame",
#     "price": 7200,
#     "tax": 381
# }

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Start using the "Item" BaseModel
# Post / Delete / Patch methods
@app.post("/items/{item_id}")
def add_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    return {"action": "deleted", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    return {"action": "patch", "item_id": item_id}


# Use another library to make an external API request.
# An API within an API!
# https://api.github.com/users/garnaat/repos


# Incorporate with boto3: simpler than the `requests` library:
# @app.get("/aws/s3")
# def fetch_buckets():
#     s3 = boto3.client("s3")
#     response = s3.list_buckets()
#     buckets = response['Buckets']
#     return {"buckets": buckets}
