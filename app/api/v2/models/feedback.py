from . import db


class FeedbackModel:
    """
    The v2 feedback model.
    """

    def __init__(self, voter, body):
        self.voter = voter
        self.body = body

    def save_feedback(self):
        """
        Record the feedback
        """
        save_feedback_to_db = """
        INSERT INTO feedback (voter, body) VALUES(
            '{}', '{}'
        )""".format(self.voter, self.body)
        db.queryData(save_feedback_to_db)

    @staticmethod
    def get_all_feedback():
        """
            Get all feedback from the database.
        """
        get_all_feedback_query = """
            SELECT * FROM feedback
            """
        return db.select_data_from_db(get_all_feedback_query)
