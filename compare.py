__version__ = '2.0.0'
__author__ = 'Guillem Carrion Teixido'

import sqlite3
import yaml
import os
import sys
import argparse
import itertools
from lib.logger import get_custom_logger

class ComparisonTool:
    """

    """

    def __init__(self, db_path, logger):
        self.logger = logger
        self.dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.db = sqlite3.connect(db_path)

    def find_keys(self, table_name, included_columns=[], excluded_columns=[]):
        keys = []
        total_rows = self.query(f'SELECT COUNT(*) FROM {table_name}')[0][0]

        if included_columns:
            column_names = included_columns
        else:
            cur = self.db.execute(f"SELECT * FROM {table_name} LIMIT 1;")
            column_names = [description[0] for description in cur.description]
            if excluded_columns:
                for excluded_column in excluded_columns:
                    try:
                        column_names.remove(excluded_column)
                    except ValueError:
                        self.logger.warn(f'Excluded column {excluded_column} does not exist in {table_name} table.')
        column_names.sort()

        for number_of_columns in range(1, len(column_names) + 1):
            for combination in list(itertools.combinations(column_names, number_of_columns)):
                unique_rows = self.query(f"""SELECT COUNT(*) FROM 
                                            (SELECT DISTINCT {', '.join(combination)} FROM {table_name})""")[0][0]
                keys.append(combination) if unique_rows == total_rows else None

        return keys

    def find_common_keys(self, table_names: list, included_columns: list = [], excluded_columns: list = [], max_comb: int = None):
        common_keys = []

        if len(table_names) > 0:
            table_name = table_names.pop(0)
            common_keys = self.find_keys(table_name, included_columns, excluded_columns)

        while len(table_names) > 0 and common_keys:
            table_name = table_names.pop(0)
            table_keys = self.find_keys(table_name, included_columns, excluded_columns)
            common_keys = list(set(common_keys).intersection(table_keys))
        common_keys.sort()
        common_keys.sort(key=len)

        return common_keys if not max_comb else common_keys[0:max_comb]

    def query(self, sql):
        if sql.strip().upper().startswith('SELECT'):
            return self.db.cursor().execute(sql).fetchall()
        else:
            self.db.execute(sql)
            self.db.commit()
            return True


parser = argparse.ArgumentParser(prog='Comparison tool', description=None)
parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}', help='version of the tool')
parser.add_argument('-v', '--verbose', action='store_true', help='defines log level')
parser.add_argument('-c', '--create', action='store_true', help='creates a new db')
parser.add_argument('-k', '--keys', nargs='+', help='returns list of possible unique keys')
parser.add_argument('-t', '--top', type=int, help='max number of combinations')
parser.add_argument('-d', '--db', help='defines the db')
parser.add_argument('-e', '--exclude', action='extend', nargs='+', help='excludes columns from unique key search')
parser.add_argument('-i', '--include', action='extend', nargs='+', help='includes columns from unique key search')
args = parser.parse_args()


def start():
    logger = get_custom_logger()
    obj = ComparisonTool('D:\\Projects\\comparison_tool\\comparison.db', logger)
    if args.keys:
        for comb in obj.find_common_keys(args.keys, args.include, args.exclude, args.top):
            print(comb)
        # for comb in obj.find_keys(args.keys, args.include, args.exclude):
        #     print(comb)
    if (args.include or args.exclude) and not args.keys:
        parser.error('Argument -k is needed.')


if __name__ == "__main__":
    start()
