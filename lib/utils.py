import ntpath, os

class Utils():
	def __init__(self):
		pass
		# print("Utils init")

	def basename(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)

	def file_name(self, path):
		return os.path.splitext(self.basename(path))[0]