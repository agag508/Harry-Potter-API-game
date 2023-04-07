# *** API Harry Potter ***
# Version 11.01.2023
# Made by Aga and Milena

# Import the libraries which program needs in order to work
import json  # Helps decode JSON data back into native objects
import requests  # Library for using API
import random  # Library for drawing a random number
import time
from time import sleep  # Import sleep for time delay while display
from colorama import Fore  # Allows us to colour text
from rich.console import Console  # Helps to create a player table, installed before
from rich.table import Table

emojis = "\U0001F47B \U0001F9D9 \U0001F9DA \U0001F9DC \U0001F9DE \U0001F9DF"  # Display some graphic using unicode

print(emojis * 4)
greeting = "\U0001F44B WELCOME TO THE WIZARD WORLD!\U0001F31F"
for i in range(31):  # Loop runs through all the letters
    print(greeting[i], end=' ', flush=True)
    # sleep(0.3)  # Letters output with 0.3s delay

print(Fore.LIGHTYELLOW_EX + """

                        ____ 
                      .'* *.'
                   __/_*_*(_
                  / _______ |
                 _\_)/___\(_/_ 
                / _((\- -/))_ |
                \ \())(-)(()/ /
                 ' \(((()))/ '
                / ' \)).))/ ' |
               / _ \ - | - /_  |
    """)
sleep(1)

# A list with instructions

begin = ['Today you are going to fight in the Hogwarts battle! \U0001F9D9 \U0001F9DA',
         '\nYour job is to pick a character and try to defeat your opponent \U0001F480',
         '\nIf you are lucky enough to pick a wizard \U0001F9D9 you will throw a spell in a game.',
         'The spells have different strength level, so you better try your best here! \U0001F9D9\n',
         'If your character is not a wizard, you in a big trouble! The dice will decide your fate! \U0001F3B2\n',
         'Make sure you are up for the challenge, because there can only be one winner in this game. \U0001F947 ']

# Prints the list components
for sentence in begin:
    print(Fore.LIGHTWHITE_EX + sentence)
    sleep(3)


def run():  # Whole game goes in this function

    # A function that makes a prompt to the user to input a number of the wizard
    def get_your_id():
        while True:
            try:  # Integer datatype required
                y_id = int(input(Fore.LIGHTBLUE_EX + '\n\nPlease choose your ID number from the range 0 - 401: '))
            except ValueError:  # Check for datatype error
                print(f"{Fore.LIGHTRED_EX}The provided value is NOT an integer! Try again.")
                continue
            else:
                if y_id not in range(403):  # Number must fit within the range 0-402, if no - try again
                    print(f"{Fore.LIGHTRED_EX}Please provide a VALID ID number between 0 and 401!")
                    y_id = int(input(f"{Fore.LIGHTBLUE_EX}Enter the correct number: "))
            break

        sleep(2)
        print(Fore.CYAN + "\nThank you. \U0001F917 Character ID number you chosen is: {}. \U0001F60E".format(y_id))
        sleep(2)
        return y_id

    def get_opponent_id():  # Opponent ID
        get_id = random.choice(range(402))  # Call random number in range 0-401
        sleep(2)
        print("Your opponent ID is: {}. \U0001F62F\n".format(get_id))  # Print opponent number
        sleep(1)
        return get_id

    # Will use it to get json character from API
    your_id = get_your_id()
    opponent_id = get_opponent_id()

    response_api = requests.get('https://hp-api.onrender.com/api/characters')  # Use HP API
    hogwarts_data = response_api.text  # Getting a text formatted data from API
    json_data: object = json.loads(hogwarts_data)  # JSON format data

    your_character = json_data[int(your_id)]  # Getting a character based on chosen ID
    opponent = json_data[int(opponent_id)]  # Getting opponent character

    # The game begins
    print(Fore.LIGHTYELLOW_EX + "Let's start the game! \U0001F579\n"
                                "Your character is {} "
                                "and you are going to fight against {}! \U0001F3AE".format(your_character['name'],
                                                                                           opponent[
                                                                                               'name']))
    sleep(2)
    print(f"{Fore.LIGHTGREEN_EX}!!(ﾉﾟﾛﾟ)o･：*…━━━☆)ﾟ3ﾟ(★━━━…‥*：･o(ﾟﾛﾟヽ)")
    sleep(4)
    print(Fore.MAGENTA + "\nThese are your attributes:")  # Some API attributes of character
    sleep(3)

    table = Table(title="\n{}".format(your_character['name']))  # Table title
    table.add_column(" Attributes ")  # Columns
    table.add_column(" Description ")

    table.add_row("name", your_character['name'])  # Rows
    table.add_row("gender", your_character['gender'])
    table.add_row("species", your_character['species'])
    table.add_row("house", your_character['house'])
    table.add_row("ancestry", your_character['ancestry'])
    table.add_row("hair colour", your_character['hairColour'])

    # Table creation
    console = Console()
    console.print(table)

    sleep(2)

    # Prompt to proceed the game
    proceed = input(Fore.LIGHTYELLOW_EX + 'If you want to proceed with the game press ENTER otherwise leave! \n')

    def roll_the_dice():  # Roll the dice loading
        for y in range(6):
            loading = "......"
            print(loading[y], end=' ', flush=True)
            sleep(0.5)

    def dice_game():
        if not your_character['hogwartsStudent']:  # If you are not a Hogwarts Student
            dice = [1, 2, 3, 4, 5, 6]  # Dice list
            print("\U0001F52E You are unable to throw a spell because you are not a Hogwarts Student! "
                  "You will throw a dice instead. \U0001F3B2")

            roll_the_dice()  # Rolling a dice
            op_score = random.choice(dice)  # Opponent random score
            dice.remove(op_score)
            print(Fore.CYAN + "\nYour opponent's score is: " + Fore.LIGHTWHITE_EX + "{}".format(op_score) +
                  Fore.LIGHTYELLOW_EX + '.\nNow it is your turn to throw a dice! \U0001F3B2')

            your_score = random.choice(dice)  # User random score
            roll_the_dice()
            print(Fore.CYAN + '\nYour score is: ' + Fore.LIGHTWHITE_EX + "{}".format(your_score))

            if op_score > your_score:  # If opponent score is higher we lost
                print(Fore.LIGHTYELLOW_EX + 'You lost! Game over. Try your luck next time! \U0001F625\n')
                return 'Bye!'
            elif your_score > op_score:  # If opponent score is lower we win
                print('You won the battle! Luck is on your side today! Well done!\U0001F973\n')
                return 'Bye!'
            else:  # If the score is the same is a draw
                print('Draw!')
                return 'Bye'

        else:  # Hogwarts students can throw a spells
            sleep(1)
            print((
                      '\U0001F9D9') + Fore.LIGHTWHITE_EX + 'You picked {}, who is a Hogwarts student and you are a '
                                                           'member '
                                                           'of {}\U0001F9D9!'.format(your_character['name'],
                                                                                     your_character['house']))
            sleep(2)
            print('\nIt is time to do some magic \U0001FA84 Remember, the stronger spell will win!')
            sleep(1)

    dice_game()

    spell_response_api = requests.get('https://hp-api.onrender.com/api/spells')
    spell_data = spell_response_api.text  # Converting spells API to txt format
    json_spell = json.loads(spell_data)  # Converting data to json format

    spell_list = []  # Placeholder list merging name and description together
    spell_dict = {}  # Placeholder dictionary holding spell name, description and key number between 0 and 10
    x = 0  # List/dictionary index

    for element in json_spell:  # Loop creating dictionary and list with spells
        spell_list.append('{} : {}. Spell strength: {}'.format(element['name'], element['description'],
                                                               random.choice(range(1, 11))))
        # Creates dictionary with name, description and random strength of the spell
        spell_dict[x] = spell_list[x]  # adding items into dictionary
        x += 1  # incrementing index value

    def draw_spell():  # A function drawing a spell
        print(Fore.BLUE + '\nThe spell strength ranges between 1 and 10. ')
        sleep(0.5)
        # A variable holding player's spell ID of choice
        your_spell_id = input('Pick a number between 0 and 76, remember choose wisely \U0001F9D9: ')

        while int(your_spell_id) not in range(77):  # Loop validating the user input
            your_spell_id = int(input('Please provide a valid number between 0 and 10.'))
        else:  # Continues the game if input in the given range
            your_spell = spell_dict[int(your_spell_id)]  # Assigning the spell from dictionary based on provided ID
            opponent_spell = random.choice(spell_dict)  # Drawing a random spell for opponent

            # Loading a spell
            for index in range(3, 0, -1):
                print(f'{Fore.CYAN}Casting a spell...{index}')
                time.sleep(0.5)

            if your_spell[-1] == opponent_spell[-1]:  # Comparing strength of both characters
                return ('\n\U0001F9D9 \U0001F91D ' * 10 + Fore.MAGENTA +
                        ''' \n\t\t\t\t You have thrown 
{} 
    \t\t\tYour opponent spell is:
{}
    \t\t\tIt is a draw! \n'''.format(your_spell, opponent_spell))  # Returning game outcome
            elif your_spell[-1] < opponent_spell[-1]:
                return ('\n\U0001F480 \U0001F494 ' * 10 + Fore.MAGENTA +
                        ''' \n\t\t\t\t You have thrown:
{}
    \t\t\tYour opponent spell is:
{}  
    \t\t\tYour lost! \n'''.format(your_spell, opponent_spell))  # Returning game outcome
            else:
                return ('\n\U0001F973 \U0001F499 ' * 10 + Fore.MAGENTA +
                        ''' \n\t\t\t\t You have thrown:
{} 
    \t\t\tYour opponents spell is:
{}
\t\t\t\t\t\t\U0001F389 \U0001F38A
    \t\t\tWell done, you won! \n'''.format(your_spell, opponent_spell))  # Returning game outcome

    if your_character['hogwartsStudent']:
        print(draw_spell())

    play_again = input(Fore.WHITE + "\U0001F579\U0001F3AE\U0001F52E Do you wanna play again? Y/N?: ")
    if play_again in ["Y", "y"]:
        run()  # Reboot the game
    elif play_again in ["N", "n"]:
        print(f"{Fore.LIGHTGREEN_EX}Thanks for playing muggle! See you soon!")
        print(emojis * 4)
    else:
        print("Sorry I did not understand! Please restart the game if you wanna play again.")


run()  # Starts the game
