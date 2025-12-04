from constants import TYPE_BOSS, TYPE_CHARACTER
import utils
import models
import random
import time

enemiesData = utils.getEnemies()
current_wave = 1
bossData = utils.getBosses()

def pick_boss():
    # Pick the boss from the database data
    boss_info = bossData[0]
    boss = utils.convertToEntity(boss_info)
    return boss

def pick_enemies():
    # Create a pool of enemy from the database date, increase the max amount of enemy every 10 waves, switch to pick boss every 10 waves
    if current_wave % 10 == 0:
        return [pick_boss()]
    enemiesPool = [utils.convertToEntity(enemy) for enemy in enemiesData]
    max_enemies = 3 + (current_wave // 10)
    nb_enemies = random.randint(1, max_enemies)
    return random.sample(enemiesPool, nb_enemies)

def turn_order(enemies, team):
    # Randomly assign turn order between all combatants
    all_combatants = enemies.members + team.members
    all_combatants.sort(key=lambda x: x.SPD,  reverse=True)
    return all_combatants

def combat_loop(enemies, player, current_order):
    for combatant in current_order:
        if not enemies.members_alive() or not player.team.members_alive():
            break
        if combatant.is_alive():
            if combatant.type == TYPE_CHARACTER:  # Character
                target = utils.choose_target(enemies)
                combatant.attack(target)
            else:  # Enemy
                if combatant.type == TYPE_BOSS:
                    boss_turn(combatant, player)
                else:
                    target = utils.choose_target(player.team)
                    combatant.attack(target)            
        else:
            continue
        time.sleep(2)

def game_loop(player): 
    while True:
        enemies = models.Team(pick_enemies())
        while enemies.members_alive() and player.team.members_alive():
            current_order = turn_order(enemies, player.team)
            combat_loop(enemies, player, current_order)
        if not enemies.members_alive():
            wave_won(player)
        else:
            wave_lost(player)
            break

def print_turn_info(current_order, effect=None):
    global current_wave
    utils.clear_screen()
    if effect:
        effect(
            '======================================\n'
            f'             Vague n {current_wave}!\n'
            f'              {"Boss Fight!" if current_wave % 10 == 0 else ""} \n'
            '======================================'
        )
    print('======================================\n'
        f'             Vague n {current_wave}!\n'
        f'              {"Boss Fight!" if current_wave % 10 == 0 else ""} \n'
        '======================================')
    print(f"Ordre du tour :\n{'\n'.join(f'- {c.getInfo()}' for c in current_order)}\n")

def wave_won(player):
    global current_wave
    utils.clear_screen()
    utils.print_effect(f"\n ============================================================================ \n"
            f"                   Vague n {current_wave} terminée! Votre équipe a gagné.\n"
            " ============================================================================")
    if current_wave % 10 == 0: 
        for member in player.team.members:
                member.HP = member.maxHP
        print("Vague de boss terminée! l'Équipe a été soignée")
    print(f"État de l'équipe : {player.team.getTeamInfo()}")
    player.score += current_wave * 10
    current_wave += 1
    time.sleep(3)

def wave_lost(player):
    global current_wave
    utils.clear_screen()
    print("Votre équipe a été vaincue. Fin du jeu.")
    utils.print_effect(f"\n ============================================================================\n"
                       f"                   Score final de {player.username} : {player.score}\n"
                        "============================================================================")
    utils.saveScore(player)
    current_wave = 0

def boss_turn(boss, player):
    target = player.team
    boss.attack(target)