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

class Club(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()

def RaceDataMapper(raceModel):
    raceData = RaceData()
    raceData.date   =  raceModel.date
    raceData.raceId =  raceModel.raceId
    return raceData
  
class Engine():
    def __init__(self):
        self.rootKey = ndb.Key('SailorsDataStore', 'RaceData')
        
    def GetClubs(self):
        key = ndb.Key(Club,'PointLESS')
        
        if len(Club.query(ancestor=key).fetch()) == 0:
            #There are no clubs - let's add a 'demo'
            demo1 = Club(parent= key)
            demo1.name = 'Demo1'
            demo1.description = 'Just for demo..'
            demo1.put()
            demo2 = Club(parent= key)
            demo2.name = 'Demo2'
            demo2.description = 'Just for demo..(2)'
            demo2.put()
            clubs = [demo1]

        clubs = Club.query(ancestor=key).fetch()
        
        res = []
        for club in clubs:
            res.append(club)
            
        return res
    
    def GetClubKey(self,clubName):
        key = ndb.Key(Club,'PointLESS')
        clubKey = Club.query(Club.name == clubName, ancestor=key).fetch()[0].key
        
        #print "The clubKey %s"%(clubKey)
        return clubKey
    
    def NewRace2(self,clubName):
        """Creats a new race."""
         
        #print "Create a new Race"
        race = RaceModel(parent = self.GetClubKey(clubName))
        race.put()
        race.raceId = 1
        existingRaces = self.GetAllRaces2(clubName)
        if len(existingRaces)>0 and race.date == existingRaces[0].date:
            race.raceId = existingRaces[0].raceId +1
        race.put()
        #print race
    
    def GetAllRaces2(self,clubName):
        """Returns all races as a list of Race objects, ordered in revers order"""
        print "Fetch all races for club %s"%(clubName)
        query = RaceModel.query(ancestor=self.GetClubKey(clubName)).order(-RaceModel.date, -RaceModel.raceId)
        raceData = map(RaceDataMapper,query.fetch())
        
        return raceData
    
    def GetActiveRace(self,clubKey):
        #old
        """ Return the last race (since that is the active one) """
        qry = RaceModel.query(RaceModel.date == race.date, RaceModel.raceId == race.raceId)
        #print qry.fetch()
        assert (len(qry.fetch()) == 1 )
        activeRace = qry.fetch(1)[0]
        return activeRace        
        

   
         
    def GetCurrentRaceId(self):
        allRaces = self.GetAllRaces()
        currentRace = "empty"
        if len(allRaces) > 0:
            currentRace = allRaces[-1].key.urlsafe()
        return currentRace

    def GetAllRaces(self):
        #old
        """Returns all races as a list of Race objects, ordered in revers order"""
        query = RaceModel.query(ancestor=self.rootKey).order(-RaceModel.date)
        return query.fetch()
    
    def _GetRaceKey(self, race):
        #print race
        qry = RaceModel.query(RaceModel.date == race.date, RaceModel.raceId == race.raceId)
        #print qry.fetch()
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
        #print "looking for %s" %(int(sailNo))
        sailors = SailorModel.query(SailorModel.tags == int(sailNo)).fetch()
        #print "number %s" % (len(sailors))
        return sailors
        
        
