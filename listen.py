# from lib.router import CustomRuleRouter
from config import settings as SETTINGS
from lib.consumer import Consumer

from importlib import import_module
import inspect

def run():
	for x in SETTINGS.INSTALLED_APPS:
		preArr = []
		r = import_module(".router", x)
		try:
			for consumer_class, topics in r.consumers:
				# print(consumer_class, topics)
				for topic in list(set(topics)):
					Consumer.addListener(topic, consumer_class)
				# print(Consumer.listeners)
		except Exception as e:
			print(e)
			continue
	Consumer().consume()
		

if __name__ == '__main__':
	run()
