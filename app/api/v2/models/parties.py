# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class PartiesModel:
    """
        v2 parties model
    """

    def __init__(self, name, hqAddress, logoUrl):
        self.name = name
        self.hqAddress = hqAddress,
        self.logoUrl = logoUrl

    def save_party(self):
        """
        Add a new party to db
        """
        save_party_query = """
        INSERT INTO parties(name, hqAddress, logoUrl) VALUES(
            '{}', '{}', '{}'
        )""".format(self.name, self.hqAddress, self.logoUrl)

        db.query_data_from_db(save_party_query)

    @staticmethod
    def get_all_parties():
        """
            Get all parties
        """
        get_all_parties_query = """
        SELECT id, name, hqAddress, logoUrl FROM parties
        """
        return db.query_data_from_db(get_all_parties_query)
