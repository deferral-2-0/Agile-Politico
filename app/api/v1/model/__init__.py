OFFICES = []
PARTIES = []


class OfficesModel:

    def __init__(self, type, name):
        self.id = len(OFFICES)
        self.type = type
        self.name = name

    # save new office
    def save_office(self):
        OFFICES.append(self)
    # This method gets the data attributes from the list of office objects
    @staticmethod
    def get_all_offices():
        return [vars(office) for office in OFFICES]

    @staticmethod
    def get_office(id):
        return [vars(office) for office in OFFICES if office.id == id]


class PartiesModel:
    def __init__(self, name, logoUrl):
        self.id = len(PARTIES)
        self.name = name
        self.logoUrl = logoUrl

    def save_party(self):
        PARTIES.append(self)

    def setname(self, newname):
        """
            sets the name of the object to a new name provided in the parameter
        """
        self.name = newname

    @staticmethod
    def get_all_parties():
        """
            returns a list of all objects with only their attributes
        """
        return [vars(party) for party in PARTIES]

    @staticmethod
    def get_party_object(id):
        """
            returns the object with all attributes and functions as well
        """
        return [party for party in PARTIES if party.id == id]

    @staticmethod
    def get_party(id):
        """
            returns the object with only the attributes. 
        """
        return [vars(party) for party in PARTIES if party.id == id]

    @staticmethod
    def deleteparty(id):
        found = False
        for party in PARTIES:
            if party.id == id:
                PARTIES.remove(party)
                found = True
        return found
