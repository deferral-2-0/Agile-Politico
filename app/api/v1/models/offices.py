"""
This is the offices model
"""

OFFICES = []


class OfficesModel:

    def __init__(self, type, name):
        """
            This is the constructor method that
            instanciates an object from the OfficesModel
        """
        self.id = len(OFFICES)
        self.type = type
        self.name = name

    # save new office
    def save_office(self):
        """
            This method appends
            an object to the list of
            objects
        """
        OFFICES.append(self)

    @staticmethod
    def get_all_offices():
        """
            This method gets all the attributes from
            the objects in the list of objects
        """
        return [vars(office) for office in OFFICES]

    @staticmethod
    def get_office(party_id):
        """
            This method gets the attributes of an
            object if the object has an ID equal to
            the id provided in the parameters
        """
        return [vars(office) for office in OFFICES if office.id == party_id]
