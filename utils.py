import pymongo
import os 
import models
from terminaltexteffects.effects.effect_laseretch import LaserEtch
from terminaltexteffects.effects.effect_print import Print
from terminaltexteffects.utils.graphics import Gradient, Color


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gameDB"]

# Database functions
def get_collection(collection_name):
    return db[collection_name]

def insertMany(collection_name, entities_data):
    collection = get_collection(collection_name)
    collection.insert_many(entities_data)

# Score functions
def saveScore(player):
    collection = get_collection('players')
    collection.insert_one(player.__getstate__())

def showScores(top):
    collection = get_collection('players')
    scores = collection.find().sort("score", -1).limit(top)
    for idx, score in enumerate(scores):
        print(f"{idx + 1}. {score['username']} - Score: {score['score']}")

# Entity management functions
def getCharacters():
    collection = get_collection('entities')
    characters = collection.find({"type": 1})
    return [char for char in characters]

def getEnemies():
    collection = get_collection('entities')
    enemies = collection.find({"type": 2})
    return [enemy for enemy in enemies]

def getBosses():
    collection = get_collection('entities')
    bosses = collection.find({"type": 3})
    return [boss for boss in bosses]

def cleanEntities():
    db.drop_collection('entities')

def convertToEntity(data):
    if (data['type'] == 2):
        return models.Enemy(
            name=data['name'],
            ATK=data['ATK'],
            HP=data['HP'],
            DEF=data['DEF'],
            SPD=data['SPD'],
            CRT=data['CRT']
        )
    elif (data['type'] == 3):
        class_name = data['name'].replace(" ", "")
        boss_class = getattr(models, class_name, models.Boss)
        if boss_class != models.Boss:
            return boss_class(
                ATK=data['ATK'],
                HP=data['HP'],
                DEF=data['DEF'],
                SPD=data['SPD'],
                CRT=data['CRT']
            )
        return models.Boss(
            name=data['name'],
            ATK=data['ATK'],
            HP=data['HP'],
            DEF=data['DEF'],
            SPD=data['SPD'],
            CRT=data['CRT']
        )
    return models.Character(
        name=data['name'],
        ATK=data['ATK'],
        HP=data['HP'],
        DEF=data['DEF'],
        SPD=data['SPD'],
        CRT=data['CRT']
    )

# Screen functions (purely esthetic)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def laser_print(text):
    text = f"\n{text}\n\n\n"
    laser = LaserEtch(text)
    laser.effect_config.etch_speed = 2
    laser.effect_config.etch_delay = 2
    laser.effect_config.final_gradient_direction = Gradient.Direction.HORIZONTAL
    laser.effect_config.final_gradient_stops = [Color("#FF3D12"), Color("#FFB412")]

    with laser.terminal_output() as terminal:
        for frame in laser:
            terminal.print(frame)

def print_effect(text): 
    effect = Print(text)
    effect.effect_config.print_speed = 4
    effect.effect_config.print_head_return_speed = 3
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)