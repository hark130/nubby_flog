# Standard Imports
import os
import sys

# Third Party Imports

# Local Imports
from nufl.nufldb import NuflDb
from nufl.nufl_menu import run_main_menu


def main() -> None:
    nufl_obj = NuflDb(sys.argv[1])
    nufl_obj.parse()
    run_main_menu(nufl_obj)
    # parse_db(os.path.join('raw', 'working.db'))
    # for entry in nufl_obj._select_statement('*', 'sqlite_master'):
    #     print(entry)
    # record = nufl_obj._get_record('Team_Listing', '*', 2)
    # print(record)
    # entry = nufl_obj._get_record_index('Team_Listing', '*', 2, 1)
    # print(entry)
    # entry = nufl_obj._get_record_index('Team_Listing', '*', 2, 7)
    # print(entry)
    # print(nufl_obj.get_team_name(362))
    # print(nufl_obj.get_team_num('Bearded Basterds'))
    # print(nufl_obj.get_team_cash('Bearded Basterds'))
    # nufl_obj._update_statement('Team_Listing', 'iCash', 'ID', 1337, 362)
    # print(nufl_obj.get_team_cash('Bearded Basterds'))
    # nufl_obj.commit()


if __name__ == '__main__':
    main()
