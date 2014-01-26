class RaceData():
    def __init__(self):
        self.date = None
        self.raceId = None
    
    def GetRaceName(self):
        return "%s:%s"%(self.date, self.raceId)
        
    def __str__(self):
        return "date:%s raceId:%s"%(self.date, self.raceId)

class SailorData():
    def __init__(self):
        self.sailNo = None
        self.surName = None
        self.lastName = None
        self.boatClass = None

