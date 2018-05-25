import json


def db():
    f = open("database.json", "r")
    token = json.load(f)
    f.close()
    return token


def get_json():
    collection = open('WEBPAGES_RAW/bookkeeping.json')
    j = json.load(collection)
    collection.close()
    return j


def idf_db():
    f = open("idf.json", "r")
    i = json.load(f)
    f.close()
    return i
