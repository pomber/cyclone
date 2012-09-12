from termscounter import TermsCounter
import codecs


def persist_terms_counter(terms_counter, filename):
	with codecs.open(filename, "w", encoding="utf-8") as out:
		out.write(str(terms_counter.docs_count()))
		out.write("\n")
		for term, count in terms_counter.most_common():
			line = u"{0:9d} {1}\n".format(count, term)
			out.write(line)

def load_terms_counter(filename):
	with codecs.open(filename, "r", encoding="utf-8") as source:
		docs_count = int(source.readline().rstrip('\n'))
		terms_counts = {}
		for line in source:
			splits = line.split()
			term = splits[1]
			count = int(splits[0])
			terms_counts[term] = count
	return TermsCounter(counts=terms_counts, docs_count=docs_count)

