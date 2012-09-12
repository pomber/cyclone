from threading import Thread
from datetime import datetime
from datetime import timedelta
import codecs

DOC_PREFIX = "TW"
TS_PREFIX = "TS"

class FileSource(object):
  
    def __init__(self, filename, listener): 
        self._filename = filename
        self._listener = listener
        Thread(target=self._start).start()

    def _start(self):
        source = codecs.open(self._filename, "r", encoding="utf-8")
        for line in source:
            if is_document(line):
                text = get_text(line)
                self._listener.new_document(text)
            elif is_timestamp(line):
                datetime = get_datetime(line)
                self._listener.new_timestamp(datetime)
        self._listener.close()

def is_document(line):
    return line.startswith(DOC_PREFIX)

def is_timestamp(line):
    return line.startswith(TS_PREFIX)

def get_text(line):
    return line[3:].rstrip('\n')

def get_datetime(line):
    timestamp = line[3:]
    dt, _, us = timestamp.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)