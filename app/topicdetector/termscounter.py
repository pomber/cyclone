from collections import Counter
import docprocessing

MAX_SIZE = 10000
MAX_DOCS = 1000

class TermsCounter(object):
	
	def __init__(self, counts = None, docs_count = 0):
		self._counter = Counter() if counts is None else Counter(counts)
		self._docs_count = docs_count

	def update(self, doc):
		terms = docprocessing.get_terms(doc)
		self._counter.update(terms)
		self._docs_count += 1

	def add(self, other):
		self._counter += other._counter
		self._docs_count += other._docs_count
		self._remove_low_counts()

	def subtract(self, other):
		self._counter -= other._counter
		self._docs_count -= other._docs_count

	def list(self):
		return list(self._counter)

	def value(self, term):
		return self._counter[term]

	def docs_count(self):
		return self._docs_count

	def most_common(self, n=None):
		return self._counter.most_common(n)

	def _remove_low_counts(self):
		items = self._counter.items()
		low_counts = [term for term, count in items if count is 1]
		for term in low_counts:
			del self._counter[term]
