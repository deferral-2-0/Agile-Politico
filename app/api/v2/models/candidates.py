from . import db


class CandidateModel:

    @staticmethod
    def check_if_candidate_is_already_registered(user_id, office_id):
        check_vote_query = """
        SELECT candidate, office FROM candidates
        WHERE candidates.candidate = '{}' AND candidates.office = '{}'
        """.format(user_id, office_id)

        isregistered = db.select_data_from_db(check_vote_query)
        return isregistered

    @staticmethod
    def register_politician_user_to_office(office_id, candidate_id):
        """
            This method is meant to add a candidate vying an office to the 
            candidates tables.
        """
        save_candidate_info = """
            INSERT INTO candidates(office, candidate) VALUES(
                '{}', '{}')""".format(office_id, candidate_id)
        db.query_data_from_db(save_candidate_info)
