from . import db

class AcceptanceModel:
    """
    The v2 acceptance model.
    """

    def __init__(self, candidate, acceptance):
        self.candidate = candidate
        self.acceptance = acceptance

    def save_vote(self):
        """
        Accept new applicant as a candidate.
        """
        save_request_to_db = """
        INSERT INTO candidature(candidate, acceptance) VALUES(
            '{}', '{}',
        )""".format(self.candidate, self.acceptance)
        db.queryData(save_request_to_db)

    # check if a user already accepted as a candidate
    @staticmethod
    def check_if_user_already_accepted_as_a_candidate(candidate):
        """
            checks if a user has already been made a candidate via 
            request acceptance.
        """
        check_candidature_query = """
        SELECT candidate FROM candidature
        WHERE candiature.candidate = '{}'
        """.format(candidate)
        acceptance = db.select_data_from_db(check_candidature_query)
        return acceptance