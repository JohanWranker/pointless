import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def sailorsDataStore():
    """Root for all sailors."""
    return ndb.Key('SailorsDataStore', 'LessSailors')


class SailorsData(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    sailNo = ndb.StringProperty()
    surName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    boatClass = ndb.StringProperty()
    registrationDate = ndb.DateTimeProperty(auto_now_add=True)

class Registration(webapp2.RequestHandler):

    def get(self):
        
        template_values = {
        'DataStore': sailorsDataStore().urlsafe()
        }

        template = JINJA_ENVIRONMENT.get_template('Registration.html')
        self.response.write(template.render(template_values))

class NewSailor(webapp2.RequestHandler):
    def post(self):
    
        sailorsData = SailorsData(parent=sailorsDataStore())
        sailorsData.sailNo = self.request.get('SailNo')
        sailorsData.surName = self.request.get('SurName')
        sailorsData.lastName = self.request.get('LastName')
        sailorsData.boatClass = self.request.get('Class')
        
       

        self.redirect('/?tom')
