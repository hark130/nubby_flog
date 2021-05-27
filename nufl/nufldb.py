# Standard Imports
from typing import Any
import sqlite3

# Third Party Imports

# Local Imports


class NuflDb:

    def __init__(self, db_file: str) -> None:
        self._db_file = db_file  # Filename
        self._db_obj = None      # Sqlite3 object
        self._modified = False   # User has called set

    def __del__(self) -> None:
        self._close()

    def parse(self) -> None:
        self._db_obj = sqlite3.connect(self._db_file)

    def commit(self) -> None:
        self._commit()

    def get_team_cash(self, team_name: str) -> int:
        team_num = self.get_team_num(team_name)
        entry = self._get_record('Team_Listing', 'ID, iCash', team_num)
        return entry[1]

    def get_team_list(self, num_teams: int = 0) -> list:
        # LOCAL VARIABLE
        team_list = []
        list_len = num_teams  # Number of teams to return

        # GET IT
        entries = self._select_statement('ID, strName', 'Team_Listing')
        for entry in entries:
            team_list.append(tuple((entry[0], entry[1])))
        if 0 == num_teams:
            list_len = len(team_list)  # Return all teams

        # DONE
        return team_list[len(team_list) - list_len:]

    def get_team_roster(self, team_num: int) -> list:
        # LOCAL VARIABLE
        team_roster = []

        # GET IT
        entries = self._select_statement_full('ID, strName, idTeam_Listing', 'Player_Listing', 'idTeam_Listing', team_num)
        for entry in entries:
            team_roster.append(entry[0])

        # DONE
        return team_roster

    def get_team_name(self, team_num: int) -> str:
        entries = self._select_statement('ID, strName', 'Team_Listing')
        for entry in entries:
            if entry[0] == team_num:
                return entry[1]

    def get_team_num(self, team_name: str) -> int:
        entries = self._select_statement('ID, strName', 'Team_Listing')
        for entry in entries:
            if entry[1] == team_name:
                return entry[0]

    def set_player_casualty(self, player_id: int, injury_num: int) -> None:
        # LOCAL VARIABLES
        cur_cas_list = self._get_player_casualties(player_id)
        val_str = '{}, {}'
        if injury_num not in cur_cas_list:
            self._insert_statement('Player_Casualties',
                                   'idPlayer_Listing,idPlayer_Casualty_Types',
                                   val_str.format(player_id, injury_num))

    def set_team_cash(self, team_num: int, new_cash: int) -> None:
        self._update_statement('Team_Listing', 'iCash', 'ID', new_cash, team_num)

    def is_modified(self) -> bool:
        return self._modified

    def _commit(self) -> None:
        self._db_obj.commit()
        self._modified = False

    def _close(self) -> None:
        if self._db_obj:
            self._db_obj.close()
            self._db_obj = None

    def _get_player_casualties(self, player_id: int) -> list:
        # LOCAL VARIABLE
        cas_list = []
        entries = self._select_statement_full('*', 'Player_Casualties', 'idPlayer_Listing', player_id)
        for entry in entries:
            cas_list.append(entry[2])

        # DONE
        return cas_list

    def _get_record(self, table: str, field: str, id: int) -> tuple:
        records = self._select_statement(field, table)
        for record in records:
            if record[0] == id:
                return record

    def _get_record_index(self, table: str, field: str, id: int, index: int) -> Any:
        record = self._get_record(table, field, id)
        return record[index]

    def _insert_statement(self, table: str, field: str, values: str) -> None:
        cmd = 'INSERT INTO {} ({}) VALUES ({})'
        self._db_obj.execute(cmd.format(table, field, values))

    def _select_statement(self, field: str, table: str) -> sqlite3.Cursor:
        cmd = 'SELECT {} FROM {}'
        return self._db_obj.execute(cmd.format(field, table))

    def _select_statement_full(self, field: str, table: str, field_name: str, field_value: Any) -> sqlite3.Cursor:
        cmd = 'SELECT {} FROM {} WHERE {} = {}'
        return self._db_obj.execute(cmd.format(field, table, field_name, field_value))

    def _update_statement(self, table: str, field_name: str, id_name: str, field_value: Any, id_value: str) -> None:
        # LOCAL VARIABLES
        ret_val = None
        cmd = 'UPDATE {} SET {} = ? WHERE {} = ?'

        # UPDATE
        ret_val = self._db_obj.execute(cmd.format(table, field_name, id_name), (field_value, id_value))
        self._modified = True

        # DONE
        return ret_val
