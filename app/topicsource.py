from topicdetector.termscounterpersistence import load_terms_counter
from topicdetector.termscounterpersistence import terms_counter_as_text
from topicdetector.topicdetector import TopicDetector
from tweetsource.tweetsource import TweetSource
from eventstream.eventstream import EventStream
from docset.docaggregator import DocAggregator
from clocksource.timer import Timer
from stream.stream import StreamFactory
from stream.stream import Stream
from threading import Thread
from config import config

class TopicsSource(object):

	def __init__(self):		
		self._topics = []
		self._docset_stream = self._create_docset_stream()
		self._topicdetector = self._create_topicdetector()
		Thread(target=self._start).start()

	def _create_docset_stream(self):
		docset_interval = config["docset.interval"]
		timer_tick = config["timer.tick"]

		stream_for_events = Stream()
		eventstream = EventStream(stream_for_events)
		timer = Timer(eventstream, seconds_span=timer_tick)
		tweetsource = TweetSource(eventstream, config)
		streamfactory = StreamFactory()
		docaggregator = DocAggregator(streamfactory, eventstream, interval=docset_interval)
		return docaggregator.stream()

	def _create_topicdetector(self):
		topics_count = config["topics.count"]

		terms_counter_path = config["tc.path"]
		terms_counter = load_terms_counter(terms_counter_path)
		return TopicDetector(terms_counter, topics_count=topics_count)

	def _start(self):
		for docset in self._docset_stream:
			topics = self._topicdetector.get_topics(docset)
			self._topics = _normalize_topics(topics)

	def get_current_topics(self):
		return self._topics

	def get_terms_counter_as_text(self):
		terms_counter = self._topicdetector.get_terms_counter()
		return terms_counter_as_text(terms_counter)


def _normalize_topics(topics):
	if len(topics) is 0:
		return []
		
	max_weight = max([t.weight for t in topics])
	min_weight = min([t.weight for t in topics])
	return [{"text": t.term, "weight": _normalize_weight(t.weight, max_weight, min_weight)} for t in topics]

def _normalize_weight(w, maxw, minw):
	if maxw == minw:
		return 0.5
	return ((w - minw) / (maxw - minw)) * 0.9 + 0.1