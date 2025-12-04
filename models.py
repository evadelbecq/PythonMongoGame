import random
from constants import TYPE_BOSS, TYPE_CHARACTER, TYPE_ENEMY
import utils

class Entity:
    def __init__(self, name, ATK, HP, DEF, SPD, CRT):
        self.name = name
        self.ATK = ATK
        self.HP = HP
        self.maxHP = HP
        self.DEF = DEF
        self.SPD = SPD
        self.CRT = CRT

    def attack(self, other):
        is_critical = random.randint(1, 100) <= self.CRT
        damage = self.ATK * (2 if is_critical else 1) - other.DEF
        damage = max(damage, 0)
        if is_critical:
            print("Coup critique!")
        print(f"{self.name} attaque {other.name} et inflige {damage} points de dégâts.")
        other.HP -= damage
        if other.HP <= 0:
            print(f"{other.name} est mort!")
        return damage
    
    def is_alive(self):
        if  self.HP > 0:
            return True
        self.HP = 0 
        return False
    
    def getInfo(self):
        if self.is_alive():  
            return f"{self.name} - ATK: {self.ATK}, HP: {self.HP}/{self.maxHP}, DEF: {self.DEF}, SPD: {self.SPD}, CRT: {self.CRT}"
        return f"{self.name} - MORT"
    
    
class Character(Entity):
    def __init__(self, name, ATK, HP, DEF, SPD, CRT):
        super().__init__(name, ATK, HP, DEF, SPD, CRT)
        self.type = TYPE_CHARACTER

class Enemy(Entity):
    def __init__(self, name, ATK, HP, DEF, SPD, CRT):
        super().__init__(name, ATK, HP, DEF, SPD, CRT)
        self.type = TYPE_ENEMY

class Boss(Entity):
    def __init__(self, name, ATK, HP, DEF, SPD, CRT):
        super().__init__(name, ATK, HP, DEF, SPD, CRT)
        self.type = TYPE_BOSS

class Team:
    def __init__(self, members):
        self.members = members
    
    def __len__(self):
        return len(self.members)

    def append(self, member):
        self.members.append(member)
    
    def getTeamInfo(self):
        return f"[\n{', \n'.join([member.getInfo() for member in self.members])}\n]"
    
    def members_alive(self):
        return any(member.is_alive() for member in self.members)

class Player:
    def __init__(self, username, team):
        self.username = username
        self.team = team
        self.score = 0
    
    def __getstate__(self):
        return {
            "username": self.username,
            "team": [member.__dict__ for member in self.team.members],
            "score": self.score
        }
    

class AdamSmasher(Boss):
    def __init__(self, ATK, HP, DEF, SPD, CRT):
        super().__init__(name="Adam Smasher", ATK=ATK, HP=HP, DEF=DEF, SPD=SPD, CRT=CRT)
    
    def missileLaunch(self, team):
        print(f"{self.name} utilise Lancement de Missiles!")
        utils.laser_print(f"Bouffez ça bandes de sacs a viande!")
        for member in team.members:
            if member.is_alive():
                self.ATK //= len(team.members)
                super().attack(member)
                self.ATK *= len(team.members)
    
    def sandevistanOverdrive(self, team):
        print(f"{self.name} active Sandevistan Overdrive! Sa vitesse et sa précision augmentent.")
        utils.laser_print(f"Meurs tas de chair!")
        self.SPD += 10
        self.CRT += 5
        team.members.sort(key=lambda x: x.HP)
        super().attack(team.members[0])

    def attack(self, team):
        randomPick = random.randint(1, 10)
        if randomPick <= 3:
            self.missileLaunch(team)
        elif randomPick <= 5:
            self.sandevistanOverdrive(team)
        else:
            utils.laser_print(f"Viens par la espèce de rat!")
            target = utils.choose_target(team)
            super().attack(target)

#en cours de dev
# class YorinobuArasaka(Boss):
#     def __init__(self, ATK, HP, DEF, SPD, CRT):
#         super().__init__(name="Yorinobu Arasaka", ATK=ATK, HP=HP, DEF=DEF, SPD=SPD, CRT=CRT)
    
#     def summonGuards(self, team):
#         print(f"{self.name} invoque des gardes du corps!")
#         utils.beam_print(f"Je vous paye pour ça tuez-les!")
#         team.append(Enemy(name="Garde du corps", ATK=25, HP=60, DEF=5, SPD=10, CRT=5))
#         team.append(Enemy(name="Garde du corps", ATK=25, HP=60, DEF=5, SPD=10, CRT=5))
