import utils
import models

def initialize_database():
    print("===================================== Initializing database. =====================================")

    try:
        utils.cleanEntities()
        print("Cleared existing entities from the database.")

        characters = [
            models.Character(name="Johnny Silverhand", ATK=55, HP=140, DEF=15),
            models.Character(name="V", ATK=52, HP=160, DEF=12),
            models.Character(name="Judy Alvarez", ATK=48, HP=155, DEF=10),
            models.Character(name="Viktor Vektor", ATK=58, HP=135, DEF=16),
            models.Character(name="Panam Palmer", ATK=50, HP=150, DEF=14),
            models.Character(name="Kerry", ATK=45, HP=170, DEF=18),
            models.Character(name="River Ward", ATK=56, HP=145, DEF=13),
            models.Character(name="Rogue Amendiares", ATK=54, HP=150, DEF=12),
            models.Character(name="David Martinez", ATK=51, HP=155, DEF=15),
            models.Character(name="Rebecca", ATK=57, HP=140, DEF=14),
        ]

        enemies = [
            models.Enemy(name="Corpo-rat", ATK=18, HP=20, DEF=3),
            models.Enemy(name="Merc", ATK=15, HP=25, DEF=2),
            models.Enemy(name="Robot", ATK=12, HP=50, DEF=5),
            models.Enemy(name="Thug", ATK=15, HP=30, DEF=1),
            models.Enemy(name="Policier", ATK=13, HP=40, DEF=3),
            models.Enemy(name="Netrunner", ATK=20, HP=20, DEF=5),
            models.Enemy(name="Drone", ATK=24, HP=45, DEF=4),
            models.Enemy(name="MaxTac", ATK=30, HP=150, DEF=10),
            models.Enemy(name="Assassin", ATK=50, HP=40, DEF=2),
            models.Enemy(name="Cyberpsycho", ATK=35, HP=150, DEF=5),
        ]


        utils.insertMany('entities', [entity.__dict__ for entity in [*characters, *enemies]])
        print("Populated entities into the database.")
        print("Characters : \n",utils.getCharacters())
        print("Enemies : \n", utils.getEnemies())
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")
        raise e
    

initialize_database()
print("=============================== Database initialization complete. ===============================")