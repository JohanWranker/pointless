import webapp2
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if not user:
            user = "Okänd"
            
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('This is PointLess ' + 'Hello, ' + user.nickname())


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

