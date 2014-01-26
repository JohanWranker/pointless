import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Engine import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class Index(webapp2.RequestHandler):

    def get(self):
        defaultClubName = 'empty'
        activeClubName = self.request.get('club',defaultClubName)                
        engine = Engine()
        
        #Locate all clubnames and present those in a list
        clubs = engine.GetClubs()
        for club in clubs:
            if club.name == activeClubName:
                clubs.remove(club) #The active club is marked active club instead
                break
        
        #Present all races connected to a club in a list (nevest on top)         
        races = []
        if activeClubName != defaultClubName:
            for race in engine.GetAllRaces2(activeClubName):
                races += [race.GetRaceName() ]
 
        template_values = { 
            'CLUBS' : clubs,
            'ACTIVE_CLUB' : activeClubName,
            'RACES':  races
            
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class NewRace(webapp2.RequestHandler):
    def get(self):
        clubName = self.request.get('Club','')
        engine=Engine()
        engine.NewRace2(clubName)
        
        self.redirect('/?club='+clubName)
        




