"""
    Initializes a connection to the db
"""
import os
import sys
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash

# import a current_app context so that we can get access to the apps config.
from flask import current_app as app


def init_db():
    """
        Initialize db connection
    """
    try:
        conn, cursor = connect_to_db()
        """
            first check if the app is in test mode,
            if its in test mode, then drop all tables and create them
            if not then don't drop them at all.
        """
        create_db_query = []
        if app.config['TESTING']:
            create_db_query = drop_table_if_exists() + set_up_tables()
        else:
            create_db_query = set_up_tables()
        i = 0
        while i != len(create_db_query):
            query = create_db_query[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        print("--"*50)
        conn.close()

    except Exception as error:
        print("\nQuery not executed : {} \n".format(error))


def set_up_tables():
    """
        Queries run to set up and create tables
    """
    table_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR (24) NOT NULL UNIQUE,
        firstname VARCHAR (24) NOT NULL,
        lastname VARCHAR (24) NOT NULL,
        othername VARCHAR (24),
        phone VARCHAR (24) NOT NULL,
        email VARCHAR (30) NOT NULL UNIQUE,
        password VARCHAR (128) NOT NULL,
        passportUrl VARCHAR (200),
        isPolitician BOOLEAN,
        isAdmin BOOLEAN
    )"""

    parties_table = """ 
    CREATE TABLE IF NOT EXISTS parties (
        id SERIAL PRIMARY KEY,
        name VARCHAR (35) NOT NULL UNIQUE,
        hqAddress VARCHAR (30),
        logoUrl VARCHAR
    )"""

    offices_table = """
        CREATE TABLE IF NOT EXISTS offices (
            id SERIAL PRIMARY KEY,
            name VARCHAR (35) NOT NULL UNIQUE,
            type VARCHAR (35)
        )"""

    canditates_table = """
        CREATE TABLE IF NOT EXISTS candidates (
            id SERIAL,
            candidate INTEGER,
            office INTEGER,
            PRIMARY KEY (office, candidate),
            FOREIGN KEY (candidate) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (office) REFERENCES offices(id) ON DELETE CASCADE
        )"""

    voters_table = """
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL,
            office INTEGER,
            candidate INTEGER,
            voter INTEGER,
            PRIMARY KEY (office, voter),
            FOREIGN KEY (office) REFERENCES offices(id) ON DELETE CASCADE,
            FOREIGN KEY (candidate) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (voter) REFERENCES users(id) ON DELETE CASCADE
        )"""

    return [table_users, parties_table,
            offices_table, canditates_table, voters_table]


def drop_table_if_exists():
    """
        Removes all tables on app restart
    """
    drop_users_table = """
    DROP TABLE IF EXISTS users CASCADE"""
    drop_parties_table = """
    DROP TABLE IF EXISTS parties CASCADE"""
    drop_offices_table = """
    DROP TABLE IF EXISTS offices CASCADE"""
    drop_candidates_table = """
    DROP TABLE IF EXISTS candidates CASCADE"""

    drop_voters_table = """
    DROP TABLE IF EXISTS votes CASCADE"""
    return [drop_users_table, drop_parties_table, drop_offices_table,
            drop_candidates_table, drop_voters_table]


def connect_to_db(query=None):
    """
        Initiates a connection to the db and executes a query
    """
    conn = None
    cursor = None
    DB_URL = app.config["DATABASE_URI"]
    try:
        # connect to db
        conn = psycopg2.connect(DB_URL)
        print("\n\nConnected {}\n".format(conn.get_dsn_parameters()))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if query:
            # Execute query
            cursor.execute(query)
            # Commit changes
            conn.commit()

    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print("DB ERROR: {}".format(error))
    return conn, cursor


def queryData(query, get_inserted_item=False):
    """
        Handles INSERT/PATCH/DELETE queries
    """
    try:
        conn, cursor = connect_to_db(query)
        if(get_inserted_item):
            lastitem = cursor.fetchone()[0]
            conn.close()
            return lastitem
        # After successful query
        conn.close()
    except psycopg2.Error as _error:
        sys.exit(1)


def select_data_from_db(query):
    """
        Handles SELECT queries
    """
    rows = None
    conn, cursor = connect_to_db(query)
    if conn:
        # Retrieve SELECT query results from db
        rows = cursor.fetchall()
        conn.close()

    return rows


# initialize the db operations
if __name__ == '__main__':
    init_db()
    connect_to_db()
