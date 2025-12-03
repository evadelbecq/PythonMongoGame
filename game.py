import utils
import models
import random
import time

enemiesData = utils.getEnemies()
curent_wave = 1

def pick_enemies():
    # Create a pool of enemy from the database date, increment the max amount of enemy every 10 waves
    enemiesPool = [utils.convertToEntity(enemy) for enemy in enemiesData]
    max_enemies = 3 + (curent_wave // 10)
    nb_enemies = random.randint(1, max_enemies)
    return random.sample(enemiesPool, nb_enemies)

def turn_order(enemies, team):
    # Randomly assign turn order between all combatants
    all_combatants = enemies.members + team.members
    all_combatants.sort(key=lambda x: x.SPD,  reverse=True)
    return all_combatants

def combat_loop(enemies, player, current_order):
    for combatant in current_order:
        utils.clear_screen()
        print('======================================\n'
            f'             Vague n {curent_wave}!\n'
            '======================================')
        print(f"Ordre du tour :\n{'\n'.join(f'- {c.getInfo()}' for c in current_order)}\n")
        if not enemies.members_alive() or not player.team.members_alive():
            break
        if combatant.is_alive():
            if combatant.type == 1:  # Character
                target = random.choice([enemy for enemy in enemies.members if enemy.is_alive()])
                damage = combatant.attack(target)
                print(f"{combatant.name} attaque {target.name} et inflige {damage} points de dégâts.")
                if target.is_alive() == False:
                    print(f"{target.name} est mort!")
            else:  # Enemy
                target = random.choice([member for member in player.team.members if member.is_alive()])
                damage = combatant.attack(target)
                print(f"{combatant.name} attaque {target.name} et inflige {damage} points de dégâts.")
                if target.is_alive() == False:
                    print(f"{target.name} est mort!")
        time.sleep(1)

def game_loop(player): 
    while True:
        global curent_wave

        enemies = models.Team(pick_enemies())
        while enemies.members_alive() and player.team.members_alive():
            current_order = turn_order(enemies, player.team)
            combat_loop(enemies, player, current_order)
        if not enemies.members_alive():
            utils.clear_screen()
            print(f"\n ============================================================================ \n"
                  f"                   Vague n {curent_wave} terminée! Votre équipe a gagné.\n"
                  " ============================================================================")
            print(f"État de l'équipe : {player.team.getTeamInfo()}")
            player.score += curent_wave * 10
            curent_wave += 1
            time.sleep(3)
        else:
            utils.clear_screen()
            print("Votre équipe a été vaincue. Fin du jeu.")
            print(f"\n ============================================================================ \n"
                  f"                   Score final de {player.username} : {player.score}\n"
                  " ============================================================================")
            utils.saveScore(player)
            break

