import pymongo
import os 
import models

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gameDB"]

def get_collection(collection_name):
    return db[collection_name]

def insertMany(collection_name, entities_data):
    collection = get_collection(collection_name)
    collection.insert_many(entities_data)

def saveScore(player):
    collection = get_collection('players')
    collection.insert_one(player.__getstate__())

def showScores(top):
    collection = get_collection('players')
    scores = collection.find().sort("score", -1).limit(top)
    for idx, score in enumerate(scores):
        print(f"{idx + 1}. {score['username']} - Score: {score['score']}")

def getCharacters():
    collection = get_collection('entities')
    characters = collection.find({"type": 1})
    return [char for char in characters]

def getEnemies():
    collection = get_collection('entities')
    enemies = collection.find({"type": 2})
    return [enemy for enemy in enemies]

def cleanEntities():
    db.drop_collection('entities')

def convertToEntity(data):
    if (data['type'] == 2):
        return models.Enemy(
            name=data['name'],
            ATK=data['ATK'],
            HP=data['HP'],
            DEF=data['DEF']
        )
    return models.Character(
        name=data['name'],
        ATK=data['ATK'],
        HP=data['HP'],
        DEF=data['DEF']
    )

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')