# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .offices import OfficesModel
from .candidates import CandidateModel
from .users import UserModel


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
        SELECT voter, office, candidate FROM votes
        WHERE votes.voter = '{}' AND votes.office = '{}'
        """.format(voter, office)
        voted = db.select_data_from_db(check_vote_query)
        return voted

    @staticmethod
    def resolve_user_voting_activity(user_id):
        """
        This function returns the voting activity undertaken by a user.
        for all the offices that are existent in the app.
        """
        data = []
        for office in OfficesModel.get_all_offices():
            info = None
            voteinfo = VotesModel.check_if_user_already_voted(
                user_id, office["id"])
            if(voteinfo):
                candidatevotedfor = UserModel.get_user_by_id(voteinfo[0][2])
                # get candidate by id
                info = "You have already voted for {} here".format(
                    candidatevotedfor[0][1])
            else:
                info = OfficesModel.get_all_candidates(office["id"])
            details = {
                "id": office["id"],
                "name": office["name"],
                "type": office["type"],
                "info": info
            }

            data.append(details)
        return data
