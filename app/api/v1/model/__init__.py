OFFICES = []
PARTIES = []


class OfficesModel:

    def __init__(self, id, type, name):
        self.id = id
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
    # def __init__(self, id, name, logoUrl):
    #     self.id = id
    #     self.name = name
    #     self.logoUrl = logoUrl

    # def save_party(self):
    #     PARTIES.append(self)
    @staticmethod
    def get_all_parties():
        return [vars(party) for party in PARTIES]
