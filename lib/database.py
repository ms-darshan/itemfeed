from config import settings
from pymongo import MongoClient, database as pymongodb
from sqlalchemy import create_engine
from item.models import Item
from variant.models import Variant, Property

DATABASES = settings.DATABASES

class DatabaseDriver():

	__STATE__ = None
	__CLIENT__ = None
	__USERNAME__ = None
	__PASSWORD__ = None
	__HOST__ = None
	__PORT__ = None
	__DATABASE__ = None
	__TYPE__ = None
	
	def __init__(self, db_obj):
		if not db_obj or not isinstance(db_obj, dict):
			raise TypeError("DataBase Initialization Failed. Invalid init database dictionary", db_obj)

		mandate = ["type", "host", "port", "database"]
		mandate_type = [str, [str, list], [int, list], str]
		for i, x in enumerate(mandate):
			if x not in db_obj:
				raise KeyError("%s: Missing"%(x))
			if isinstance(mandate_type[i], list):
				valid = False
				for y in mandate_type[i]:
					if isinstance(db_obj[x], y):
						valid = True
						break
				if not valid:
					raise TypeError("%s: %s given. Must be %s"%( x, str(type(db_obj[x])), " | ".join([str(j) for j in mandate_type[i]]) ) )
			elif not isinstance(db_obj[x], mandate_type[i]):
				raise TypeError("%s: %s given. Must be %s"%(x, str(type(db_obj[x])), mandate_type[i]))

		self.__HOST__ = db_obj["host"]
		self.__PORT__ = db_obj["port"]
		self.__TYPE__ = db_obj["type"]
		self.__DATABASE__ = db_obj["database"]
		if "username" in db_obj and isinstance(db_obj["username"], str):
			self.__USERNAME__ = db_obj["username"]
		if "password" in db_obj and isinstance(db_obj["password"], str):
			self.__PASSWORD__ = db_obj["password"]

	@property
	def state(self):
		return self.__STATE__

	@state.setter
	def state(self, value):
		if isinstance(value, str):
			self.__STATE__ = value
		else:
			raise TypeError("Invalid type for state: str")
			


class MongoHandler(DatabaseDriver):

	__REPLICA_SET__ = None

	def __init__(self, db_obj):
		if not db_obj:
			raise ValueError("Mongo Initialization Failed. Invalid init database dictionary", db_obj)

		if "replica_set" in db_obj and isinstance(db_obj["replica_set"], str):
			self.__REPLICA_SET__ = db_obj["replica_set"]
		
		super().__init__(db_obj)
		self.state = "PROCESSING"

	def generate_url(self):
		protocol = "mongodb://"
		
		auth_str = ""
		if self.__USERNAME__ and self.__PASSWORD__:
			auth_str = self.__USERNAME__ + ":" + self.__PASSWORD__ + "@"
		
		host_arr = []
		for i, host in enumerate(self.__HOST__):
			host_arr.append(host + ":" + str(self.__PORT__[i]))
		host_str = ",".join(host_arr)
		
		replica_set_str = ""
		if self.__REPLICA_SET__:
			replica_set_str = "?replicaSet=" + self.__REPLICA_SET__
		
		try:
			gen_url = protocol + auth_str + host_str + "/" + self.__DATABASE__ + replica_set_str
			self.GEN_URL = gen_url
		except Exception as e:
			print("Error generating URL: ", e)
			return False
		return gen_url

	def connect(self):
		g_url = self.generate_url()
		if not g_url or not isinstance(g_url, str):
			raise TypeError("Invalid URL generated for mongo: ", g_url)
		client = MongoClient(g_url)
		if not client:
			raise ValueError("Invalid mongoClient generated: ", client)
		self.client = client[self.__DATABASE__]
		self.state = "CONNECTED"
		return True

	@property
	def client(self):
		return self.__CLIENT__

	@client.setter
	def client(self, value):
		if isinstance(value, pymongodb.Database):
			self.__CLIENT__ = value
		else:
			raise TypeError("Invalid type for client: MongoClient")


class PostgreSQLHandler(DatabaseDriver):
        def __init__(self, db_obj):
                if not db_obj:
                        raise ValueError("PostgreSQL Initialization Failed. Invalid init database dictionary", db_obj)
                super().__init__(db_obj)
                self.state = "PROCESSING"                

        def makeUrl(self):
            uesr = ""
            if self.__USERNAME__:
                user = self.__USERNAME__
            pwd = ""
            if self.__PASSWORD__:
                pwd = self.__PASSWORD__
            url = str(self.__TYPE__) + "://" + str(uesr) + ":" + str(pwd) + "@" + str(self.__HOST__) + ":" + \
                 str(self.__PORT__) + "/" + str(self.__DATABASE__)
            return str(url)

        def connect(self):
                db_url = self.makeUrl()
                print(db_url)
                self.__CONNECTION__ = create_engine(db_url, echo=settings.DEBUG)

                if not self.__CONNECTION__:
                        raise ValueError("Invalid connection object generated")

                self.client = self.__CONNECTION__
                self.state = "CONNECTED"
                Base = settings.getDeclartiveBase()
                Base.metadata.create_all(self.__CLIENT__)
                return True

        @property
        def client(self):
                return self.__CLIENT__

        @client.setter
        def client(self, value):
                if value:
                        self.__CLIENT__ = value
                else:
                        raise TypeError("Invalid type for client: MongoClient")	

class ConnectDB():
	__DATABASES__ = {}
	def __init__(self):
		for x in DATABASES:
			if "type" in DATABASES[x] and DATABASES[x]["type"] == "mongo":
				self.__DATABASES__[x] = MongoHandler(DATABASES[x])
			elif "type" in DATABASES[x] and DATABASES[x]["type"] == "postgresql":
				self.__DATABASES__[x] = PostgreSQLHandler(DATABASES[x])
			else:
				print("Invalid database config", x)

	def connect(self):
		for x in self.__DATABASES__:
			print("Connecting to %s"%x)
			try: k = self.__DATABASES__[x].connect()
			except Exception as e:
				print("Error connecting to %s"%(x), e)
				continue
			if not k:
				print("Error connecting to %s"%(x))
			else:
				print("Connection established with %s"%(x))

	@property
	def databases(self):
		dbs = {}
		for x in self.__DATABASES__:
			if self.__DATABASES__[x].state == "CONNECTED":
				dbs[x] = self.__DATABASES__[x]
		return dbs
