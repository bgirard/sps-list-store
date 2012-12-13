import webapp2
import datetime
from google.appengine.ext import db

def error(requestHandler, errorMsg):
  requestHandler.error(500)
  requestHandler.response.write("Error: " + errorMsg)

class ListItem(db.Model):
  name = db.StringProperty(required=True)
  created = db.DateTimeProperty()

class ListStore(webapp2.RequestHandler):
  def get(self):

    if self.request.get("name", None) == None:
      error(self, "name is required")
      return

    if self.request.get("name") == "":
      error(self, "name is empty")
      return

    self.response.headers['Content-Type'] = 'text/html'

    listItem = ListItem(name=self.request.get("name"))
    listItem.created = datetime.datetime.now() # Force the created date. We don't want the user controlling this field

    args = self.request.arguments()
    for arg in args:
      argValue = self.request.get(arg)
      setattr(listItem, arg, argValue);
      # self.response.write(arg + "=" + argValue + "<br>")

    listItem.put()

    self.response.write('stored')
    
class QueryStore(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('not done')


app = webapp2.WSGIApplication([('/', ListStore),
                               ('/list-store', ListStore),
                               ('/query-list-store', QueryStore)],
                              debug=True)
