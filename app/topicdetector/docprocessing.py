from __future__ import division
from math import log
import nltk

def get_terms(doc):
	tokens = tokenize(doc)
	terms = set()
	for token in tokens:
		if token.isalpha():
			terms.add(token.lower())
	return terms

def tokenize(doc):
	return nltk.word_tokenize(doc)

def get_tf(term, terms_counter):
	return log(terms_counter.value(term), 2)

def get_idf(term, terms_counter):
	docs_count = terms_counter.docs_count()
	terms_count = terms_counter.value(term)
	if docs_count is 0:
		return 1
	else:
		return log(docs_count / (terms_count + 2), 2)
	