import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Registration import *
from Index import *

application = webapp2.WSGIApplication([
    ('/', Index),
    ('/Registration', Registration),
    ('/NewSailor',NewSailor),
    ('/gethint',GetHint),
    ('/NewRace',NewRace),
], debug=True)

