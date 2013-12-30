from google.appengine.ext import ndb
from Interfaces import *

class RaceModel(ndb.Model):
    date = ndb.DateProperty(auto_now_add=True)
    raceId = ndb.IntegerProperty()


#A model over a sailor - is used for the 'active sailors in a race and the 'sailors storage db'
class SailorModel(ndb.Model):
    sailNo = ndb.StringProperty() #The complete sail number 
    tags = ndb.IntegerProperty(repeated =True) # The numeric part of the sailno
    surName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    boatClass = ndb.StringProperty()
    registrationDate = ndb.DateTimeProperty(auto_now_add=True)

class Engine():
    def __init__(self):
        self.rootKey = ndb.Key('SailorsDataStore', 'RaceData')

    def NewRace(self,precedingRace = None):
         """Creats a new race. Return a token for the day"""
         
         print "Create a new Race"
         race = RaceModel(parent = self.rootKey)
         if not precedingRace:
            race.raceId = 1
         else:
             race.date = precedingRace.date
             race.raceId = precedingRace.raceId +1
         race.put()
         print race
         
    def GetCurrentRace(self):
        return self.GetAllRaces()[-1].key

    def GetAllRaces(self):
        """Returns all races as as list of Race objects, ordered in revers order"""
        query = RaceModel.query(ancestor=self.rootKey).order(-RaceModel.date)
        return query.fetch()
    
    def _GetRaceKey(self, race):
        print race
        qry = RaceModel.query(RaceModel.date == race.date, RaceModel.raceId == race.raceId)
        print qry.fetch()
        assert (len(qry.fetch()) == 1 )
        activeRace = qry.fetch(1)[0]
        return activeRace
        
    def NewSailor(self, race, sailor):
        """Register a new sailor to a race"""
    
        #parent=self._GetRaceKey(race)
        raceId = self.GetCurrentRace()
        sailorsData = SailorModel(parent=raceId)
        sailorsData.sailNo = sailor.sailNo
        numeric = 0
        sailorsData.tags = []
        for c in sailor.sailNo:
            if c.isdigit():
                numeric = numeric *10 + int(c)
                sailorsData.tags.append(numeric)
        if numeric == 0:
            sailorsData.tags.append(numeric)
        
        sailorsData.surName = sailor.surName
        sailorsData.lastName = sailor.lastName
        sailorsData.boatClass = sailor.boatClass
        sailorsData.put()
        self.UpdateSailorsDb(sailorsData)
        
    def UpdateSailorsDb(self,sailorsData):
        s = SailorModel(parent = self.rootKey)
        s.sailNo = sailorsData.sailNo
        s.tags = sailorsData.tags 
        s.surName = sailorsData.surName
        s.lastName = sailorsData.lastName
        s.boatClass = sailorsData.boatClass
        s.registrationDate = sailorsData.registrationDate
        s.put()

    def GetAllSailors(self,race):
        """ Returns all sailors in a specific race unordered"""
        #ancestor=self._GetRaceKey(race)
        raceId = self.GetCurrentRace()
        sailors = SailorModel.query(ancestor=raceId).fetch()
        return sailors
        
    def PreFetchSailorsBySailno(self, sailNo):
        print "looking for %s" %(int(sailNo))
        sailors = SailorModel.query(SailorModel.tags == int(sailNo)).fetch()
        print "number %s" % (len(sailors))
        return sailors
        
        
