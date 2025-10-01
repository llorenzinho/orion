from orion.core.database.db import Database, get_database


def database() -> Database:
    return get_database()  # cached instance of Database class
