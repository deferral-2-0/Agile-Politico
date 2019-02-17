# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class VotesModel:
    """
    The v2 votes model.
    """

    def __init__(self, office, candidate, voter):
        self.office = office
        self.candidate = candidate
        self.voter = voter

    def save_vote(self):
        """
        Add a new vote to the votes table.
        """
        save_vote_to_db = """
        INSERT INTO votes(office, candidate, voter) VALUES(
            '{}', '{}', '{}'
        )""".format(self.office, self.candidate, self.voter)
        db.queryData(save_vote_to_db)

    # check if a user already voted
    @staticmethod
    def check_if_user_already_voted(voter, office):
        """
            checks if a user has already voted for a particular 
            post or not.
        """
        check_vote_query = """
        SELECT voter, office FROM votes
        WHERE votes.voter = '{}' AND votes.office = '{}'
        """.format(voter, office)
        voted = db.select_data_from_db(check_vote_query)
        return voted
