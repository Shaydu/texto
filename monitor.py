import configparser, os
import sys
import time
import logging
import pprint

from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from twilio.rest import TwilioRestClient

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


config = configparser.ConfigParser()
config.read('configs.cfg')

API_SID = ConfigSectionMap("Prod")['api_sid']
API_SECRET = ConfigSectionMap("Prod")['api_secret']
API_PHONE = ConfigSectionMap("Prod")['api_phone']
API_PHONE_TO = ConfigSectionMap("Prod")['api_phone_to']

class MyHandler(FileSystemEventHandler):
     def getClient(self):
        return self.__client

     def setClient(self, client):
        self.__client = client
    
     def on_created(self, event):
         pprint.pprint(event.event_type)
         pprint.pprint(event.src_path)
         pprint.pprint(dir(event))
         client.messages.create(to=API_PHONE_TO,
            from_=API_PHONE,
            body=event.src_path)
         #time.sleep(500)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    event_handler = MyHandler() #LoggingEventHandler()
    client = TwilioRestClient(account=API_SID, token=API_SECRET)
    event_handler.setClient(client)
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


