from Queue import Queue

class Stream(Queue):	

	_sentinel = object()

	def __iter__(self):		
		return iter(self.get, self._sentinel)

	def close(self):
		self.put(self._sentinel)

class StreamFactory(object):

	def create_stream(self):
		return Stream()
