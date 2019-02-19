# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

from .users import UserModel


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
        database (ADMINS ONLY OPERATION)
        """
        save_new_office = """
        INSERT INTO offices(name, type) VALUES(
            '{}', '{}'
        ) RETURNING id;""".format(self.name, self.type)
        return db.queryData(save_new_office, True)

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
    def formatResults(iterable):
        """
            This function formats the results in a record format
        """
        data = []
        for result in iterable:
            formattedResult = {
                "candidate": result[0],
                "result": result[1],
                "office": result[2]
            }
            data.append(formattedResult)
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

    @staticmethod
    def get_specific_office(office_id):
        """
            This method gets to select a specific OFFICE
            from the list of offices that matches the id provided
            in the arguments
        """
        select_single_office = """
        SELECT id, name, type FROM offices
        WHERE offices.id = '{}'""".format(office_id)

        return OfficesModel.formatOffices(db.select_data_from_db(select_single_office))

    @staticmethod
    def get_office_results(office_id):
        """
        This method gets the results of a particular
        office.
        """
        get_all_office_results = """
            SELECT candidate, COUNT(candidate) AS result, office FROM votes WHERE votes.office = {} GROUP BY candidate, office;
        """.format(office_id)

        return OfficesModel.formatResults(db.select_data_from_db(get_all_office_results))

    @staticmethod
    def get_all_candidates(office_id):
        """
        this method returns all the candidates registered to a certain office.

        """
        get_all_candidates = """
        SELECT candidate FROM candidates WHERE candidates.office = {}
        """.format(office_id)

        allcandidates = db.select_data_from_db(get_all_candidates)
        candidates = []

        for candidate in allcandidates:
            user = UserModel.get_user_by_id(candidate[0])
            candidatel = user[0]
            candidates.append({
                "id": candidatel[0],
                "email": candidatel[3],
                "username": candidatel[1]
            })

        return candidates
