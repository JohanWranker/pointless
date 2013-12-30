import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Interfaces import *
from Engine import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def RaceDataStore():
    """Root for all sailors."""
    return ndb.Key('SailorsDataStore', 'RaceData')


class SailorsData(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    sailNo = ndb.StringProperty()
    surName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    boatClass = ndb.StringProperty()
    registrationDate = ndb.DateTimeProperty(auto_now_add=True)

class Registration(webapp2.RequestHandler):

    def get(self):
        
        sailors_query = SailorsData.query(
            ancestor=RaceDataStore()).order(-SailorsData.registrationDate)
        sailors = sailors_query.fetch(10)
        raceId = self.request.get('RaceId','')
        
        engine=Engine()
        sailors = engine.GetAllSailors('2356')
        print "All sailors %s" % (sailors)


        
        template_values = {
            'DataStore': RaceDataStore().urlsafe(),
            'SAILORS'  : sailors,
            'RACEID'   : raceId
        }

        template = JINJA_ENVIRONMENT.get_template('Registration.html')
        self.response.write(template.render(template_values))

class GetHint(webapp2.RequestHandler):
    def get(self):
        #print "GetHint *******************************"
        sailNo = self.request.get('q','')
        engine=Engine()
        sailors = engine.PreFetchSailorsBySailno(sailNo)
        self.response.write('<sailors>')
        for sailor in sailors:
            self.response.write('<sailor sailNo="%s" surName="%s" lastName="%s"/>'%
            (sailor.sailNo,sailor.surName, sailor.lastName))
        self.response.write('</sailors>')
        
class NewSailor(webapp2.RequestHandler):
    def post(self):
    
        s = SailorData()
        s.sailNo = self.request.get('SailNo')
        s.surName = self.request.get('SurName')
        s.lastName = self.request.get('LastName')
        s.boatClass = self.request.get('Class')

        raceId = self.request.get('RaceId','')
        engine=Engine()
        engine.NewSailor(raceId,s)
        
        self.redirect('Registration')
        
        
