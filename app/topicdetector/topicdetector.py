from termscounter import TermsCounter
from termscounterqueue import TermsCounterQueue
from collections import defaultdict
import docprocessing

class TopicDetector(object):

	def __init__(self, terms_counter=None, topics_count=60, queue_size=12):
		self._terms_counter = terms_counter or TermsCounter()
		self.topics_count = topics_count
		self._tc_queue = TermsCounterQueue(queue_size)

	def get_topics(self, docset):
		docset_terms_counter = self._get_terms_counter(docset)
		self._tc_queue.add_termscounter(docset_terms_counter)
		
		discarded_termscounter = self._tc_queue.discard_termscounter()
		self._terms_counter.add(discarded_termscounter)

		current_termscounter = self._tc_queue.get_termscounter()
		weights = self._get_terms_weights(current_termscounter)
		top_terms = self._get_top_terms(weights)

		return [Topic(term, weights[term]) for term in top_terms[:self.topics_count]]

	def get_terms_counter(self):
		return self._terms_counter

	def _get_terms_counter(self, docset):
		terms_counter = TermsCounter()
		for doc in docset.stream():
			terms_counter.update(doc)
		return terms_counter

	def _get_terms_weights(self, terms_counter):
		weights = defaultdict(float)
		for term in terms_counter.list():
			tf = docprocessing.get_tf(term, terms_counter)
			idf = docprocessing.get_idf(term, self._terms_counter)
			weights[term] = tf * idf
		return weights

	def _get_top_terms(self, weights):
		return sorted(weights, key=weights.get, reverse=True)
		
class Topic(object):

	def __init__(self, term, weight):		
		self.term = term
		self.weight = weight

	def __str__(self):
		return self.term.encode("ascii", "replace") + " " + str(self.weight)
		