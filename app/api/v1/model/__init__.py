OFFICES = []

# def __init__(self, id, type, name):
#     self.id = id
#     self.type = type
#     self.name = name

# def save_office(self):
#     OFFICES.append(self)


class OfficesModel:

    # This method gets the data attributes from the list of office objects
    @staticmethod
    def get_all_offices():
        return [vars(office) for office in OFFICES]
