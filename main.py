import models
import utils
import game

def start_game():
    print("Starting the game...")
    while True:
        utils.clear_screen()
        print('============================================================================\n'
              '                          Bienvenue dans CyberPynk !\n'
              '                         1. Commencer une nouvelle partie\n'
              '                         2. Consulter le classement\n'
              '                         3. Quitter le jeu\n'
              '============================================================================'
              )
        choice = input('Entrez votre choix (1-3): \n')
        match choice:
            case '1':
                utils.clear_screen()
                team_selection()
            case '2':
                utils.clear_screen()
                print("Top 10 des joueurs :")
                utils.showScores(10)
                input("Appuyez sur Entrée pour revenir au menu principal...")
            case '3':
                print("Merci d'avoir joué à CyberPynk ! À bientôt.")
                break
            case _:
                print("Choix invalide. Veuillez réessayer.")

        
def team_selection():
    while True:
        username = input('Entrez votre pseudo: \n')
        if not username:
            print("Veillez entrer un pseudo valide.")
            continue
        break
    print(f"Bienvenue, {username}!")
    print("Choisissez votre équipe de 3 pour partir a l'aventure :")
    team = models.Team(members=[])
    characterData = utils.getCharacters()
    characters = [utils.convertToEntity(char) for char in characterData]
    while len(team) < 3:
        #Selection loop
        utils.clear_screen()
        if len(team) > 0:
            print(team.getTeamInfo())
        print("Personnages disponibles :")
        for idx, char in enumerate(characters):
            print(f"{idx +1}. {char.getInfo()}")
        choice = input(f"Sélectionnez un personnage: \n")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(characters):
            print("Choix invalide. Veuillez réessayer.")
            continue
        selected_char = characters[int(choice) - 1]
        team.append(selected_char)
        characters.pop(int(choice) - 1)
        print(f"{selected_char.name} ajouté à l'équipe.")
    utils.clear_screen()
    print(f"Équipe finale : {team.getTeamInfo()}")
    player = models.Player(username=username, team=team)
    game.game_loop(player)

start_game()