class Notam:
    def __init__(self, NotamId, NotamType, issued, affectedFIR, traffic, purpose, scope, coordinates, radius):
        self.NotamId = NotamId
        self.NotamType = NotamType
        self.issued = issued
        self.affectedFIR = affectedFIR
        self.traffic = traffic
        self.purpose = purpose
        self.scope = scope
        self.coordinates = coordinates
        self.radius = radius