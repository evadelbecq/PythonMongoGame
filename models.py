class Entity:
    def __init__(self, name, ATK, HP, DEF, SPD):
        self.name = name
        self.ATK = ATK
        self.HP = HP
        self.maxHP = HP
        self.DEF = DEF
        self.SPD = SPD

    def attack(self, other):
        damage = self.ATK - other.DEF
        damage = max(damage, 0)
        other.HP -= damage
        return damage
    
    def is_alive(self):
        if  self.HP > 0:
            return True
        self.HP = 0 
        return False
    
    def getInfo(self):
        if self.is_alive():  
            return f"{self.name} - ATK: {self.ATK}, HP: {self.HP}/{self.maxHP}, DEF: {self.DEF}, SPD: {self.SPD}"
        return f"{self.name} - MORT"
    
    
class Character(Entity):
    def __init__(self, name, ATK, HP, DEF, SPD):
        super().__init__(name, ATK, HP, DEF, SPD)
        self.type = 1

class Enemy(Entity):
    def __init__(self, name, ATK, HP, DEF, SPD):
        super().__init__(name, ATK, HP, DEF, SPD)
        self.type = 2

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