# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class OfficesModel:
    """
        v2 offices model
    """

    def __init__(self, name, type):
        """
            Initialize an OfficesModel.
        """
        self.name = name
        self.type = type

    def save_office(self):
        """
        Add a new office to the
        database (ADMIN ONLY OPERATION)
        """
        save_new_office = """
        INSERT INTO offices(name, type) VALUES(
            '{}', '{}'
        )""".format(self.name, self.type)
        db.query_data_from_db(save_new_office)
