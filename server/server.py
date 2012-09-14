import json
import web
import mimetypes
from web import http

urls = (
	"/", "Index", 
	"/topics", "Topics", 
	"/termscounter", "TermsCounter", 
	'/(?:css|img|js|rss)/.+', 'Public')
app = web.application(urls, globals())
render = web.template.render('views/')
public_dir = 'public'

topics_source = None

class Index:
	def GET(self):
		return render.index()

class Topics:
	def GET(self):
		topics = topics_source.get_current_topics()
		web.header('Content-Type', 'application/json')
		return json.dumps(topics)

class TermsCounter:
	def GET(self):
		return topics_source.get_terms_counter_as_text()

class Public:
	def GET(self): 
		try:
			file_name = web.ctx.path.split('/')[-1]
			web.header('Content-type', _mime_type(file_name))
			return open(public_dir + web.ctx.path, 'rb').read()
		except IOError:
			raise web.notfound()

def _mime_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def run():
	app.run()

def wsgifunc():
	return app.wsgifunc()

def set_topics_source(source):
	global topics_source
	topics_source = source