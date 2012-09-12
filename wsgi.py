from app.topicsource import TopicsSource
from server import server
import web

topics_source = TopicsSource()
server.set_topics_source(topics_source)

web.config.debug = True
application = server.wsgifunc()

if __name__ == "__main__":
    server.run()