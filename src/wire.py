from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from asyncio import coroutine
import logging
import sys

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO,
    format="%(asctime)s %(levelname)7s: %(message)s")
logger = logging.getLogger(__name__)


class MyComponent(ApplicationSession):
   @coroutine
   def onJoin(self, details):
       print("session ready")

       def oncounter(count):
           print("event received: %s" % count)

       try:
           yield from self.subscribe(oncounter, u'sensor.lux')
           print("subscribed to topic")
       except Exception as e:
           print("could not subscribe to topic: {0}".format(e))


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
