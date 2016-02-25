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

        def event(count):
            print("event received: %s" % count)

        yield from self.subscribe(lambda x: print("lux : %f" % x), u'sensor.lux')
        yield from self.subscribe(lambda x: print("temp : %f" % x), u'sensor.temp')
        yield from self.subscribe(lambda x: print("target : %f" % x), u'pid.input.light')


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
