# encoding=latin1
from __future__ import division
from math import log
import nltk

def get_terms(doc):
	tokens = tokenize(doc)
	terms = set()
	for token in tokens:
		if token.isalpha():
			terms.add(normalize(token))
	return terms

def tokenize(doc):
	tokens = doc.split()
	tokens = [t for t in tokens if not should_ignore(t)]
	text = " ".join(tokens)
	return nltk.word_tokenize(text)

def should_ignore(token):
	if token.startswith("@"):
		return True
	if token.startswith("#"):
		return True
	if token.startswith("http"):
		return True
	return False

def normalize(token):
	return token.lower()

def get_tf(term, terms_counter):
	return log(terms_counter.value(term), 2)

def get_idf(term, terms_counter):
	if is_stop_word(term):
		return 0
	docs_count = terms_counter.docs_count()
	terms_count = terms_counter.value(term)
	if docs_count is 0:
		return 1
	else:
		return log(docs_count / (terms_count + 2), 2)

stopwords = set(["que", "de", "a", "no", "la", "y", "me", "el", "en", "es", "se", "te", "lo", "por", "mi", "un", "si", "o", "con", "para", "los", "como", "mas", "e", "eu", "yo", "tu", "las", "una", "pero", "ya", "é", "não", "q", "le", "del", "do", "esta", "todo", "rt", "jajaja", "http"])
def is_stop_word(term):
	return term in stopwords
	

