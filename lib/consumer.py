from kafka import KafkaConsumer
from kafka.structs import TopicPartition

import time
import json
import arrow

from config.settings import KAFKA_SERVERS


def connect(servers=KAFKA_SERVERS):
	try:
		return KafkaConsumer(bootstrap_servers=servers, group_id='itemfeed')
	except Exception as e:
		print("Erro connecting kafka consumer", e)

class Consumer(object):
	""""Main kafka consumer class"""
	__consumer_instance = connect()
	listeners = {}

	def __init__(self):
		self.__stop = False
		# self.topics = self.listeners.keys()

	@property
	def topics(self):
		keys = self.listeners.keys()
		# print(self.__consumer_instance.committed(TopicPartition('user_activity', 0)))
		if len(keys) > 0:
			return keys
		raise Exception("No topics given")

	@classmethod
	def addListener(self, topic, consumer):
		consumers = Consumer.listeners.get(topic, [])
		consumers.append(consumer)
		Consumer.listeners[topic] = consumers

	def getListeners(self, topic):
		return Consumer.listeners.get(topic, [])

	def reconnect(self):
		self.__consumer_instance = connect()

	def stop(self):
		self.__stop = True
		self.__consumer_instance.close()

	def consume(self):
		print("Consuming . . .")
		if(self.__consumer_instance):
			self.__consumer_instance.subscribe(self.topics)
			# self.__consumer_instance.seek(self.topics)
			try:
				# while not self.__stop:
				for msg in self.__consumer_instance:
					try:
						if self.__stop:
							break
						# print(msg)
						# print(msg.topic, msg.partition, msg.offset, type(msg.value))
						self.do_process(msg)
						self.__consumer_instance.commit_async()
						print("Message Consumed")
					except Exception as e:
						print('sdfsdf', e)
						self.do_exception(msg, e)
				print("Closing")
				self.__consumer_instance.close()
			except Exception as error:
				print(error)
				print("Exception in consuming topics %s error is %s"%(self.topics, str(error)))
				self.consume()
				# self.error_callback(str(error))
		else:
			print("No consumer instance available something went wrong !")
			# self.error_callback('[ No Consumr Instance Available ] : Something Went Wrong !')

	def pickData(self, value):
		try:
			value = json.loads(value)
		except Exception as e:
			print(e)

		# Change delay calculation
		print("Delay in consuming :", arrow.now().timestamp - (value['time'] / 1000), "sec")
		core_data = value['data'].get('itemfeed')
		if core_data:
			return core_data

		return False

	def do_process(self, consumer_record):
		listeners = self.getListeners(consumer_record.topic)
		data = self.pickData(consumer_record.value)
		if not data:
			return self.do_exception(consumer_record, 'Data for Panzer not found in the message for topic ' + consumer_record.topic)
		
		for listener in listeners:
			listener_instance = listener()
			try:
				listener_instance.initialize(data)
			except Exception as e:
				print("Error calling initializer", e)
				pass

			try:
				listener_instance.process_data(data)
			except Exception as error:
				print(error)
				listener_instance.process_exception(error)

	def do_exception(self, consumer_record, error):
		listeners = self.getListeners(consumer_record.topic)
		for listener in listeners:
			listener().process_exception(error)
