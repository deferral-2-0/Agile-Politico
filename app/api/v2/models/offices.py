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

    @staticmethod
    def formatOffices(iterable):
        """
            This function will help in formatting the offices data 
            in a record format when its called in getting_all_offices
            or getting a specific office.
        """
        data = []
        for office in iterable:
            formattedOffice = {'id': office[0],
                               'name': office[1],
                               'type': office[2]}
            data.append(formattedOffice)
        return data

    @staticmethod
    def get_all_offices():
        """
            Fetch all the offices from the database.
        """
        get_all_offices = """
        SELECT id, name, type FROM offices
        """
        return OfficesModel.formatOffices(db.select_data_from_db(get_all_offices))
