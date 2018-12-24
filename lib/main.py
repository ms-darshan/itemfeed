from config import settings as SETTINGS
from . import router
from tornado.web import Application
from tornado.routing import RuleRouter
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line, options, define
from lib.database import ConnectDB


define("port", default=SETTINGS.PORT, help="run on the given port", type=int)
define("address", default=SETTINGS.ADDRESS, help='Listen on', type=str)

class Itemfeed():
	DBCONN = None
	def __init__(self):
		self.ROUTER = router.CustomRuleRouter()
		# print("All Routes: ", self.ROUTER.ROUTES)

	def connect_db(self):
		self.DBCONN = ConnectDB()
		self.DBCONN.connect()
		print("Database connections established with maximum effort")

	def start(self):
		parse_command_line()
		# Repurpose tuples to keep itemfeed reference
		rs = self.ROUTER.ROUTES
		for i, x in enumerate(rs):
			rs[i] = x + ({"app": self},)
		# Connect Database
		self.connect_db()

		# Attach Routes 
		router = RuleRouter([("/.*", Application(rs,debug = True))])
		
		# Configure Server and start
		server = HTTPServer(router)
		server.listen(options.port)
		print("Server Listening on PORT: " + str(options.port))
		IOLoop.current().start()
