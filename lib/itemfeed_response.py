response_codes = {
	'200': 'OK',
	'110': 'Invalid or Missing Auth Token',
	'111': 'Blacklisted Client',
	'112': 'Incorrect Password',
	'113': 'CODE-RED: Invalid or Fake Client ID',
	'114': 'CODE-RED: Incorrect Client Secret',
	'115': 'Missing Access Token',
	'116': 'Invalid Refresh Token',
	'117': 'Incorrect Access Token',
	'118': 'Unsupported Client Type',
	'501': 'Unsupported Request Type',
	'119': 'Missing Payload',
	'120': 'Missing Client ID or Secret',
	'121': 'Your ID is not in system. Please contact your manager.',
	'122': 'Missing Refresh Token',
	'403': 'Forbidden. You do not have access to this resource',
	'410': 'Data Already Existent',  # case of create new
	'411': 'Data Non Existent',
	'601': 'Custom server error'
}

def build_response(code, message = None, data = None):
	status = "failure"
	if str(code) == "200":
		status = "success"
	res = {
		"status": status,
		"code": int(code),
		"message": response_codes[str(code)]
	}
	if isinstance(message, str):
		res["message"] = message
	if data:
		res["data"] = data
	return res