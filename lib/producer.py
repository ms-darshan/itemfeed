import json

import arrow
from kafka import KafkaProducer
from kafka.errors import KafkaError

from config.settings import KAFKA_SERVERS #, PUB_SUB_DATA_FLOW


def default_callback(x):
	print(x)

class Producer(object):
	"""Main Producer class or Pub-Sub"""
	__producer_instance = KafkaProducer(bootstrap_servers=KAFKA_SERVERS)
	ALLOWED_DATA_TYPES = {
		'str': 'string',
		'list': 'array',
		'dict': 'object'
	}
	# PUB_SUB_DATA_FLOW = PUB_SUB_DATA_FLOW # Get from database in future
	PUB_SUB_DATA_FLOW = {}
	server = None

	def __init__(self, topic=None, server=None):
		# print("baap called", self.__class__.__name__)
		if topic: self.topic = topic

		# I don't think this would help in Kafka, May be in different pub-sub model
		if server:
			self._connect(server)
		elif self.server:
			self._connect()

		self.serializer = self
		# print(self.server, server)
		self._check_instance()

	def _check_instance(self):
		if not self.topic:
			raise Exception("No topic found for ", self.__class__.__name__)

	def _connect(self, server):
		if isinstance(server, basestring):
			server = [server]
		elif isinstance(server, list):
			# Do nothing
			pass
		else:
			print("Please provide string or list type for server")
			return
		self.__producer_instance = KafkaProducer(bootstrap_servers=server)

	def close(self):
		pass

	def send(self, data, raw=False, key=None):
                if not raw:
                        data = self.format(data)
                
                future = self.__producer_instance.send(self.topic, self.serializer.serialize(data), key=key)
                # Block for 'synchronous' sends as send is asyn by default
                try:
                        return future.get(timeout=10)
                except KafkaError as e:
                        print("Error in publishing ", e)
                        return False

	def send_async(self, data, raw=False, key=None):
		if not raw:
			data = self.format(data)
		return self.__producer_instance.send(self.topic, self.serializer.serialize(data), key=key)

	def send_with_callback(self, data,raw=False, key=None):
		if not raw:
			data = self.format(data)
		return self.__producer_instance.send(self.topic, self.serializer.serialize(data), key=key) \
										.add_callback(on_send_success) \
										.add_errback(on_send_error)

	def _apply_rules(self, data, rule):
		pub_sub_data = {}
		# print(rule)
		for key in rule:
			optional = False
			exist_key = key
			if key.startswith('opt__'):
				optional = True
				key = key.replace('opt__', '', 1)

			if key.startswith('raw__'):
				pub_sub_data[key.replace('raw__', '', 1)] = rule[key]
			else:
				try:
					def getData(haystack, needle):
						try:
							return getattr(haystack, needle)
						except Exception as e:
							try:
								return haystack.get(needle)
							except:
								return None

					keys = key.split('.')
					value = data
					for k in keys:
						value = getData(value, k)
						if value == None:
							break
					pub_sub_data[rule[exist_key]] = value		
					# pub_sub_data[rule[key]] = getattr(data, key)
				except Exception as e:
					# try:
					# 	pub_sub_data[rule[key]] = data.get(key)
					# except:
					pub_sub_data[rule[exist_key]] = None

			if optional and ( pub_sub_data[rule[exist_key]] == None):
				del pub_sub_data[rule[exist_key]]

		return pub_sub_data

	def transform(self, data):
		if self.topic in PUB_SUB_DATA_FLOW:
			print("Found")
			pub_sub_data = {}
			for consumer in PUB_SUB_DATA_FLOW[self.topic]:
				if hasattr(self, 'transform_' + consumer):
					pub_sub_data[consumer] = getattr(self, 'transform_' + consumer)(data)
					continue

				rule = PUB_SUB_DATA_FLOW[self.topic][consumer]

				if isinstance(data, list) and isinstance(rule, list):
					pub_sub_data[consumer] = []
					for d in data:
						pub_sub_data[consumer].append(self._apply_rules(d, rule[0]))
				elif not isinstance(data, list) and isinstance(rule, list):
					pub_sub_data[consumer] = self._apply_rules(data, rule[0])
					# pub_sub_data[consumer] = [self._apply_rules(data, rule[0])]
				else:
					pub_sub_data[consumer] = self._apply_rules(data, rule)	

			return pub_sub_data
		else:
			print(")not Found")
			return data

	def format(self, data):
		pub_sub_data = self.transform(data)
		data_type = pub_sub_data.__class__.__name__
		if not data_type in self.ALLOWED_DATA_TYPES:
			raise Exception(data_type + ' not allowed')
		
		return {
			'data': pub_sub_data,
			'type': self.ALLOWED_DATA_TYPES[data_type],
			'time': arrow.utcnow().timestamp
		}

	def serialize(self, data):
		try:
			if not isinstance(data, str):
				return json.dumps(data).encode('utf-8')
		except:
			pass
		return data

	def pause(self):
		pass

	def resume(self):
		pass

	@classmethod
	def pause_all(cls):
		pass

	@classmethod
	def resume_all(cls):
		pass
