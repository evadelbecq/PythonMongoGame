import models
import utils
import game

def print_menu():
    utils.clear_screen()
    utils.print_effect('============================================================================\n'
              '                          Bienvenue dans CyberPynk !\n'
              '                         1. Commencer une nouvelle partie\n'
              '                         2. Consulter le classement\n'
              '                         3. Quitter le jeu\n'
              '============================================================================',
              )

def start_game():
    print("Starting the game...")
    print_menu()

    while True:

        choice = input('Entrez votre choix (1-3): \n')
        match choice:
            case '1':
                team_selection()
            case '2':
                leaderboard()
            case '3':
                print("Merci d'avoir joué à CyberPynk ! À bientôt.")
                break
            case _:
                print("Choix invalide. Veuillez réessayer.")
def leaderboard():
    utils.clear_screen()
    print("Top 10 des joueurs :")
    utils.showScores(10)
    input("Appuyez sur Entrée pour revenir au menu principal...")

def team_selection():
    username = choose_username()
    team = choose_characters()
    utils.clear_screen()
    print(f"Équipe finale : {team.getTeamInfo()}")
    player = models.Player(username=username, team=team)
    game.game_loop(player)

def choose_username():
    utils.clear_screen()
    while True:
        username = input('Entrez votre pseudo: \n')
        if not username:
            print("Veillez entrer un pseudo valide.")
            continue
        break
    print(f"Bienvenue, {username}!")
    return username

def choose_characters():
    print("Choisissez votre équipe de 3 pour partir a l'aventure :")
    team = models.Team(members=[])
    characterData = utils.getCharacters()
    characters = [utils.convertToEntity(char) for char in characterData]
    selection_loop(characters, team)
    return team

def selection_loop(characters, team):
    while len(team) < 3:
        utils.clear_screen()
        if len(team) > 0:
            print(team.getTeamInfo())
        list_available_characters(characters)
        choice = input(f"Sélectionnez un personnage: \n")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(characters):
            print("Choix invalide. Veuillez réessayer.")
            continue
        selected_char = characters[int(choice) - 1]
        team.append(selected_char)
        characters.pop(int(choice) - 1)
        print(f"{selected_char.name} ajouté à l'équipe.")

def list_available_characters(characters):
    print("Personnages disponibles :")
    for idx, char in enumerate(characters):
        print(f"{idx +1}. {char.getInfo()}")

start_game()