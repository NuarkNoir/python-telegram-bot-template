# For now this file only creates tables in your DB
# You can add anything DB-related here, e.g. migrations
from peewee import *
from database.db import MODELS, db_handle, stop_db


def main():
    try:
        db_handle.connect()
    except Exception as px:
        print(px)
        return

    print("Creating tables...")
    for model in MODELS:
        print(f"\t {model.__name__}...")
        try:
            model.create_table()
        except Exception as px:
            print(px)
    print("Done creating tables")

    stop_db()


if __name__ == '__main__':
    main()
