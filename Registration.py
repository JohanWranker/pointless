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

        print "############### " + str(sailors)
        
        template_values = {
            'DataStore': RaceDataStore().urlsafe(),
            'SAILORS'  : sailors
        }

        template = JINJA_ENVIRONMENT.get_template('Registration.html')
        self.response.write(template.render(template_values))

class GetHint(webapp2.RequestHandler):
    def get(self):
        print "GetHint"
        self.response.write("<tr>")
        self.response.write("<td %s />" %("3619")) #,"Elias", "Wranker"))
        self.response.write("</tr>")
        #do until rs.EOF
#  for each x in rs.Fields
#    response.write("<tr><td><b>" & x.name & "</b></td>")
#   response.write("<td>" & x.value & "</td></tr>")
#  next
#  rs.MoveNext
#loop
        
class NewSailor(webapp2.RequestHandler):
    def post(self):
    
        sailorsData = SailorsData(parent=RaceDataStore())
        sailorsData.sailNo = self.request.get('SailNo')
        sailorsData.surName = self.request.get('SurName')
        sailorsData.lastName = self.request.get('LastName')
        sailorsData.boatClass = self.request.get('Class')
        sailorsData.put()
        self.redirect('Registration')
