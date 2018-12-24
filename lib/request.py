import tornado.web
import json
from bson import json_util
from lib.itemfeed_response import build_response
import traceback

class RequestHandler(tornado.web.RequestHandler):

	def initialize(self, **kwargs):
		# Creating APP reference for handlers
		self.APP = kwargs["app"]

	def write_error(self, status_code, **kwargs):
		print("In write Error")
		self.set_header('Content-Type', 'application/json')
		if self.settings.get("serve_traceback") and "exc_info" in kwargs:
			# in debug mode, try to send a traceback
			lines = []
			for line in traceback.format_exception(*kwargs["exc_info"]):
				lines.append(line)
			self.finish(json.dumps({
				'error': {
					'code': status_code,
					'message': self._reason,
					'traceback': lines,
				}
			}))
		else:
			self.finish(json.dumps({
				'error': {
					'code': status_code,
					'message': self._reason,
				}
			}))

	def respond_json(self, data = {}, raw = False):
		if not data:
			data = build_response(601)
		else:
			if raw:
				if not isinstance(data, dict):
					raise TypeError("data must be a dictionary object")
				if "status" not in data: 
					data["status"] = "success"
				if "code" not in data:
					data["code"] = 200
			else:
				data = build_response(code = 200, data = data)
		self.set_header("Content-Type", "application/json")
		self.finish(json.dumps(data, default = json_util))
