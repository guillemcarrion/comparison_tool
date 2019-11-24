import sqlite3
import yaml
import os
import argparse
import itertools

# from lib.arguments import args
from settings import *

__version__ = '1.0.0'

class ComparisonTool:
    """

    """
    def __init__(self):
        self.db = None
        self.db = sqlite3.connect(os.path.join(os.getcwd(), db_name))

    def connect2db(self):
        self.db = sqlite3.connect(os.path.join(os.getcwd(), db_name))

    def csv2db(self, csv_path):
        if self.db:
            True
        else:
            self.connect2db()
            self.csv2db(csv_path)

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
                        pass

        for number_of_columns in range(1, len(column_names) + 1):
            for combination in list(itertools.combinations(column_names, number_of_columns)):
                unique_rows = self.query(f"""SELECT COUNT(*) FROM (SELECT DISTINCT {', '.join(combination)} FROM {table_name})""")[0][0]
                keys.append(combination) if unique_rows == total_rows else None

        return keys


    def query(self, sql):
        if sql.strip().upper().startswith('SELECT'):
            return self.db.cursor().execute(sql).fetchall()
        else:
            self.db.execute(sql)
            self.db.commit()
            return True



    def __import_config(self):
        return self.a


parser = argparse.ArgumentParser(prog='Comparison tool', description=None)
parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}', help='version of the tool')
parser.add_argument('-v', '--verbose', action='store_true', help='shows the progress in detail')
parser.add_argument('-c', '--create', action='store_true', help='creates a new db')
parser.add_argument('-k', '--keys', help='returns list of possible unique keys')
parser.add_argument('-e', '--exclude', action='extend', nargs='+', help='excludes columns from unique key search')
parser.add_argument('-i', '--include', action='extend', nargs='+', help='includes columns from unique key search')
args = parser.parse_args()


def start():
    obj = ComparisonTool()
    if args.create:
        obj.connect2db()
    if args.keys:
        obj.connect2db()
        for comb in obj.find_keys(args.keys, args.include, args.exclude):
            print(comb)
    if (args.include or args.exlude) and not args.keys:
        parser.error('Argument -k is needed.')



if __name__ == "__main__":
    start()


