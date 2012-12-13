import webapp2
import datetime
from google.appengine.api import namespace_manager
from google.appengine.ext import db

def error(requestHandler, errorMsg):
  requestHandler.error(500)
  requestHandler.response.write("Error: " + errorMsg)

class ListListModel(db.Model):
  name = db.StringProperty(required=True)

class ListItemModel(db.Expando):
  name = db.StringProperty(required=True)
  created = db.DateTimeProperty()

class ListList(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    result = db.GqlQuery("SELECT * FROM ListListModel") 
    first = True
    for e in result:
      if not first:
        self.response.write(",")
      self.response.write(e.name)
      first = False

class ListStore(webapp2.RequestHandler):
  def get(self):

    nameArg = self.request.get("name", None)
    if nameArg == None:
      error(self, "name is required")
      return

    if nameArg == "":
      error(self, "name is empty")
      return

    self.response.headers['Content-Type'] = 'text/plain'

    listItem = ListItemModel(name=self.request.get("name"))
    listItem.created = datetime.datetime.now() # Force the created date. We don't want the user controlling this field

    args = self.request.arguments()
    for arg in args:
      argValue = self.request.get(arg)
      setattr(listItem, arg, argValue);
      # self.response.write(arg + "=" + argValue + "\n")

    ListListModel.get_or_insert(nameArg, name=nameArg)
    listItem.put()

    self.response.write('stored')
    
class QueryStore(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'

    nameArg = self.request.get("name", None)
    if nameArg == None:
      error(self, "name is required")
      return

    if nameArg == "":
      error(self, "name is empty")
      return

    result = db.GqlQuery("SELECT * FROM ListItemModel WHERE name = :1", nameArg) 
    first = True
    args = self.request.arguments()
    for e in result:
      skipItem = False
      props = e.dynamic_properties() 
      for arg in args:
        if arg == "name":
          continue
        if not (arg in props):
          skipItem = True
          break
        argValue = self.request.get(arg)
        if getattr(e, arg, None) != argValue:
          skipItem = True
          break
      if skipItem:
        continue;
      if not first:
        self.response.write(",")
      self.response.write("name="+ e.name + " ")
      for p in props:
        self.response.write(p +"="+ getattr(e, p) + " ")
      first = False
      self.response.write("\n")

class HelpRequest(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("/list-list - Provide a list of list names\n")
    self.response.write("/list-store?name&** - Store an item in list 'name'\n")
    self.response.write("/query-list-store?name&** - Fetch all items from list 'name' matching any specific value (example platform=mac)\n")
    self.response.write("/help - This help menu\n")

app = webapp2.WSGIApplication([('/', ListStore),
                               ('/help', HelpRequest),
                               ('/list-list', ListList),
                               ('/list-store', ListStore),
                               ('/query-list-store', QueryStore)],
                              debug=True)

