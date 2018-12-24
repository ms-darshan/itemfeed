from lib.main import Itemfeed
from config.settings import ROOT_DIR
import os, errno

def main():
	print("=================== Loading ItemFeed  =====================")
	ws = Itemfeed()
	ws.start()

if __name__ == "__main__":
	main()
