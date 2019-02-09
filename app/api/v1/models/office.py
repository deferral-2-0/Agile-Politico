OFFICES = []


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
