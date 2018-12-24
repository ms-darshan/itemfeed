import asyncio

class ProcessStream():
	stdin = None
	stderr = None
	stdout = None
	def __init__(self, stderr, stdout, stdin):
		if stderr:
			self.stderr = stderr.decode("UTF-8").strip()
		if stdin:
			self.stdin = stdin
		if stdout:
			self.stdout = stdout.decode("UTF-8").strip()

class AsyncProcess():
	def __init__(self):
		print("Async Process Ready")

	async def run(self, *args):
		#Create subprocess
		# cmd = ["ls", "-l"]
		# k = type(cmd)
		# print("Creating subprocess: ", *cmd)
		process = await asyncio.create_subprocess_exec(
				*args,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.PIPE,
			)
		print("Started: ", args, '(pid = '+ str(process.pid) +')')
		stdout, stderr = await process.communicate()
		if process.returncode == 0:
			print('Done:', args, '(pid = ' + str(process.pid) + ')')
		else:
			print('Failed:', args, '(pid = ' + str(process.pid) + ')')
		ps = ProcessStream(stderr, stdout, None)
		return ps
