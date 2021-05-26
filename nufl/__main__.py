from nufl.nufldb import NuflDb
import os


def main() -> None:
    print('NUFL!')
    # parse_db(os.path.join('raw', 'working.db'))
    nufl_obj = NuflDb(os.path.join('raw', 'working.db'))
    nufl_obj.parse()
    # for entry in nufl_obj._select_statement('*', 'sqlite_master'):
    #     print(entry)
    # record = nufl_obj._get_record('Team_Listing', '*', 2)
    # print(record)
    # entry = nufl_obj._get_record_index('Team_Listing', '*', 2, 1)
    # print(entry)
    # entry = nufl_obj._get_record_index('Team_Listing', '*', 2, 7)
    # print(entry)
    print(nufl_obj.get_team_name(362))
    print(nufl_obj.get_team_num('Bearded Basterds'))
    print(nufl_obj.get_team_cash('Bearded Basterds'))

if __name__ == '__main__':
    main()
