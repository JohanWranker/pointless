import webapp2
import jinja2
import os
from Engine import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class UnitTestPage(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(UnitTestPage, self).__init__(*args, **kwargs)
        self.engine = Engine()
        self.sailNo = 23456
        self.dummyS = SailorData()
        self.dummyS.surName = "Elias"
        self.dummyS.lastName = "Wranker"
        self.dummyS.boatClass = "OptimistB"

         
    def get(self):
        print self.request.get("U")
        command = self.request.get("U")
        if command == None:
            pass
        elif command == "NewRace":
            self.engine.NewRace()
        elif command == "NewRaceInstance":
            activeRace = self.engine.GetAllRaces()[0]
            self.engine.NewRace(activeRace)
        elif command == "GetAllRaces":
            print self.engine.GetAllRaces()
        elif command == "NewSailor":
            self.sailNo = self.sailNo +3
            self.dummyS.sailNo = "SE-" + str(self.sailNo)
            activeRace = self.engine.GetAllRaces()[0]
            self.engine.NewSailor(activeRace, self.dummyS)
            
            
        template_values = []
        template = JINJA_ENVIRONMENT.get_template('UnitTest.html')
        self.response.write(open('UnitTest.html',"r").read())


