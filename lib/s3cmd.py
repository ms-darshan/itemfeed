import subprocess, os, ntpath
from config import settings
from lib.process import AsyncProcess

class S3cmd():
	def __init__(self):
		self.base_url = settings.S3_BASE_URL

	def path_leaf(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)

	async def upload(self, path, key = None, options = []):
		if not os.path.exists(path):
			print("Invalid Path")
			return None
		print("KEY: %s"% key)
		if key:
			# upload_to = "s3://"+settings.S3_BUCKET + "/"+"/".join(key.strip("/").split("/").append(self.path_leaf(path)))
			base_key = "/"+"/".join(key.strip("/").split("/"))
		else:
			base_key = "/"+self.path_leaf(path)
		# print("Base Key: %s"%base_key)
		upload_to = "s3://"+settings.S3_BUCKET + base_key
		# print("Upload to: %s"%upload_to)
		# s3cmd put path self.base_url
		# try: output = subprocess.run(["s3cmd", "put", path, upload_to], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		try:
			cmds = ["s3cmd"] + options + ["put", path, upload_to]
			result = await AsyncProcess().run(*cmds)
		except Exception as e:
			print("Error running subprocess: ", e)
			return None

		# Analyze output to see if error or not
		if result.stderr:
			print("Error Uploading Image: ", result.stderr)
			return None
		print("STDOUT: ", result.stdout)
		return (settings.S3_BASE_URL + base_key)