from threading import Thread

class DocAggregator(object):

	_current_docset = None
	_last_timestamp = None
	
	def __init__(self, stream_factory, eventstream, interval=60):
		self._stream_factory = stream_factory
		self._eventstream = eventstream
		self._interval = interval
		
		self._docset_stream = stream_factory.create_stream()

		self._start_new_docset()
		Thread(target=self._aggregate).start()

	def _aggregate(self):
		for event in self._eventstream:
			if event.is_document():
				self._current_docset.put(event.text)
			elif self._should_start_new_docset(event):
				self._start_new_docset()
		self._current_docset.close()
		self._docset_stream.close()

	def _should_start_new_docset(self, timestamp):
		if self._interval is 0:
			return False

		current_time = timestamp.datetime
		if self._last_timestamp is None:
			self._last_timestamp = current_time

		time_elapsed = current_time - self._last_timestamp
		if time_elapsed.total_seconds() >= self._interval:
			self._last_timestamp = current_time
			return True

	def _start_new_docset(self):
		if self._current_docset:
			self._current_docset.close()
		self._current_docset = DocSet(self._stream_factory)
		self._docset_stream.put(self._current_docset)

	def stream(self):
		return self._docset_stream

class DocSet(object):

	def __init__(self, stream_factory):
		self._doc_stream = stream_factory.create_stream()

	def put(self, text):
		self._doc_stream.put(text)

	def close(self):
		self._doc_stream.close()

	def stream(self):
		return self._doc_stream
