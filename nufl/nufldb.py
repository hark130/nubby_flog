from typing import Any
import sqlite3


class NuflDb:

    def __init__(self, db_file: str) -> None:
        self._db_file = db_file  # Filename
        self._db_obj = None      # Sqlite3 object

    def __del__(self) -> None:
        if self._db_obj:
            self._db_obj.close()
            self._db_obj = None

    def parse(self) -> None:
        self._db_obj = sqlite3.connect(self._db_file)

    def get_team_cash(self, team_name: str) -> int:
        team_num = self.get_team_num(team_name)
        entry = self._get_record('Team_Listing', 'ID, iCash', team_num)
        return entry[1]

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

    def _get_record(self, table: str, field: str, id: int) -> tuple:
        records = self._select_statement(field, table)
        for record in records:
            print(record)
            if record[0] == id:
                return record

    def _get_record_index(self, table: str, field: str, id: int, index: int) -> Any:
        record = self._get_record(table, field, id)
        return record[index]

    def _select_statement(self, field: str, table: str) -> sqlite3.Cursor:
        cmd = 'SELECT {} FROM {}'
        return self._db_obj.execute(cmd.format(field, table))
