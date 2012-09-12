class EventStream(object):
	
	def __init__(self, stream):
		self._stream = stream

	def __iter__(self):
		return iter(self._stream)

	def new_document(self, text):
		document = Document(text)
		self._stream.put(document)

	def new_timestamp(self, datetime):
		timestamp = Timestamp(datetime)
		self._stream.put(timestamp)

	def close(self):
		self._stream.close()

class Event(object):

	def is_document(self):
		return False

	def is_timestamp(self):
		return False

class Document(Event):

	def __init__(self, text):
		self.text = text

	def is_document(self):
		return True

class Timestamp(Event):

	def __init__(self, datetime):		
		self.datetime = datetime

	def is_timestamp(self):
		return True
		