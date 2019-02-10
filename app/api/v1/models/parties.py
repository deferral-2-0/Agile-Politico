PARTIES = []


class PartiesModel:
    def __init__(self, name, logoUrl):
        self.id = len(PARTIES)
        self.name = name
        self.logoUrl = logoUrl

    def save_party(self):
        """
            This method saves the instance object to the
            list of parties
        """
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
    def get_party_object(party_id):
        """
            returns the object with all attributes and functions as well
        """
        return [party for party in PARTIES if party.id == party_id]

    @staticmethod
    def get_party(party_id):
        """
            returns the object with only the attributes.
        """
        return [vars(party) for party in PARTIES if party.id == party_id]

    @staticmethod
    def deleteparty(party_id):
        """
        This function deletes an object which
        has an id that matches the one provided in the
        argument
        """
        found = False
        for party in PARTIES:
            if party.id == party_id:
                PARTIES.remove(party)
                found = True
        return found
