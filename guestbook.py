import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Registration import *
from UnitTestPage import *
from Engine import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

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
        

class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/Registration', Registration),
    ('/NewSailor',NewSailor),
    ('/gethint',GetHint),
    ('/UnitTest',UnitTestPage),
    ('/NewRace',NewRace),
], debug=True)

