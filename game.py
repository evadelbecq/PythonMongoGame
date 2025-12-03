import utils
import models
import random
import time

enemiesData = utils.getEnemies()
curent_wave = 1
bossData = utils.getBosses()

def pick_boss():
    # Pick the boss from the database data
    boss_info = bossData[0]
    boss = utils.convertToEntity(boss_info)
    return boss

def pick_enemies():
    # Create a pool of enemy from the database date, increase the max amount of enemy every 10 waves, switch to pick boss every 10 waves
    if curent_wave % 10 == 0:
        return [pick_boss()]
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
            f'   {"Boss Fight!" if curent_wave % 10 == 0 else ""} \n'
            '======================================')
        print(f"Ordre du tour :\n{'\n'.join(f'- {c.getInfo()}' for c in current_order)}\n")
        if not enemies.members_alive() or not player.team.members_alive():
            break
        if combatant.is_alive():
            if combatant.type == 1:  # Character
                target = random.choice([enemy for enemy in enemies.members if enemy.is_alive()])
                combatant.attack(target)
                if target.is_alive() == False:
                    print(f"{target.name} est mort!")
            else:  # Enemy
                if combatant.type == 3:
                    target = player.team
                else:
                    target = random.choice([member for member in player.team.members if member.is_alive()])

                print(target)
                combatant.attack(target)             
        else:
            continue
        time.sleep(2)

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
            if curent_wave % 10 == 0: 
                for member in player.team.members:
                        member.HP = member.maxHP
                print("Vague de boss terminée! l'Équipe a été soignée")
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
            curent_wave = 1
            break

