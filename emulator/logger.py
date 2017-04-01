#!/usr/bin/python3
import settings
from datetime import datetime

class Logger(object):
	def __init__(self):
		pass

	def log_event(text, event_type=0):
		logfile = open(settings.LOG_PATH,'a')
		logfile.write(settings.LOG_FORMAT.format(curdate=datetime.now(), event_type=event_type, data=text))
		logfile.close()
