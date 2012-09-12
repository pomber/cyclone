from datetime import datetime
import threading

class Timer(object):
	def __init__(self, listener, seconds_span=5):
		self._timespan = seconds_span
		self._listener = listener
		self._tick()

	def _tick(self):
		self._listener.new_timestamp(datetime.now())
		threading.Timer(self._timespan, self._tick).start()
		