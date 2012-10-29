from collections import deque
from termscounter import TermsCounter

class TermsCounterQueue(object):

	def __init__(self, queue_size):
		self._queue_size = queue_size
		self._queue = deque()
		self._tc = TermsCounter()
		
	def add_termscounter(self, termscounter):
		self._queue.append(termscounter)
		self._tc.add(termscounter)

	def discard_termscounter(self):
		if len(self._queue) > self._queue_size:
			old_tc = self._queue.popleft()
			self._tc.subtract(old_tc)
			return old_tc
		else:
			return TermsCounter()

	def get_termscounter(self):
		return self._tc
