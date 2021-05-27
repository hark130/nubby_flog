# Standard Imports
from collections import namedtuple, OrderedDict

# Third Party Imports

# Local Imports
from nufl.nufl_misc import clear_screen
from nufl.nufldb import NuflDb


# GLOBALS
# Menu NamedTuple
NuflMenuFormat = namedtuple('NuflMenuFormat', 'Title Entries')
# Menu Dictionaries
NUFL_MAIN_MENU = NuflMenuFormat('MAIN MENU', OrderedDict({'A':'Team Menu',
                                                          'B':'Update cash',
                                                          'C':'Cripple team',
                                                          'D':'Commit changes',
                                                          'E':'Exit'}))
NUFL_TEAM_MENU = NuflMenuFormat('TEAM MENU', OrderedDict({'A':'Last 10',
                                                          'B':'All Teams',
                                                          'C':'Name Search',
                                                          'D':'Main Menu'}))


def run_main_menu(db_obj: NuflDb) -> None:
    # LOCAL VARIABLES
    user_choice = ''
    user_data = []
    exit_code = list(NUFL_MAIN_MENU.Entries.keys())[len(NUFL_MAIN_MENU.Entries)-1]
    changes_committed = False

    # START
    while (user_choice != exit_code):
        user_choice = print_menu(NUFL_MAIN_MENU, user_data=user_data)
        if user_choice == 'A':
            user_data = run_team_menu(db_obj)
        elif user_choice == 'B':
            user_data = run_cash_menu(db_obj)
        elif user_choice == 'C':
            user_data = run_cripple_menu(db_obj)
        elif user_choice == 'D':
            user_data = []
            db_obj.commit()
            changes_committed = True
        else:
            user_data = []

    # DONE
    if db_obj.is_modified():
        print('Unsaved changes in the database')
        print('Save changes? [Y/n]')
        user_choice = input().upper()
        if user_choice == 'Y':
            db_obj.commit()
            print('Database changes saved')


def run_cash_menu(db_obj: NuflDb) -> list:
    # LOCAL VARIABLES
    team_choice = 0  # Team to modify
    team_name = ''   # Name of the team
    cash_choice = 0  # New amount of cash

    # START
    print('Choose team number:')
    team_choice = int(input())
    team_name = db_obj.get_team_name(team_choice)
    print(f'{team_name} has {db_obj.get_team_cash(team_name)} cash')
    print('Enter new cash total:')
    cash_choice = int(input())
    db_obj.set_team_cash(team_choice, cash_choice)
    return [f'{team_name} has {db_obj.get_team_cash(team_name)} cash']


def run_cripple_menu(db_obj: NuflDb) -> list:
    # LOCAL VARIABLES
    menu_output = []
    id_list = []

    # START
    print('Choose team number:')
    # 1. Empty Cash
    team_choice = int(input())
    db_obj.set_team_cash(team_choice, 0)
    # 2. Cripple Players
    id_list = db_obj.get_team_roster(team_choice)
    for player_id in id_list:
        db_obj.set_player_casualty(player_id, 10)
        db_obj.set_player_casualty(player_id, 11)
    # 3. Nerf Player Rolls
    # TO DO: DON'T DO NOW...

    # DONE
    return menu_output



def run_team_menu(db_obj: NuflDb) -> list:
    # LOCAL VARIABLES
    menu_output = []
    user_choice = print_menu(NUFL_TEAM_MENU)

    # START
    # Last 10
    if user_choice == 'A':
        print('Last 10')
        menu_output = db_obj.get_team_list(10)
    # All Teams
    elif user_choice == 'B':
        print('All Teams')
        menu_output = db_obj.get_team_list()
    # Name Search
    elif user_choice == 'C':
        print('Name Search')
        menu_output = []  # Placeholder

    # DONE
    return menu_output


def print_menu(menu: NuflMenuFormat, clr_screen: bool = True, user_data: list = []) -> str:
    # Clear Screen
    if clr_screen:
        clear_screen()
    # Print Title
    print(menu.Title)
    # Print Data
    if user_data:
        print()
    for entry in user_data:
        print(entry)
    if user_data:
        print()
    # Print Entries
    for key, value in menu.Entries.items():
        print(f'{key}.\t{value}')
    # User Input
    print('Choose an option:')
    return input().upper()
