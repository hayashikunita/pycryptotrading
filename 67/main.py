import logging
import sys
from app.controllers.streamdata import stream
from app.controllers.webserver import start
from threading import Thread

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    streamThread = Thread(target=stream.stream_ingestion_data)
    serverThread = Thread(target=start)

    streamThread.start()
    serverThread.start()

    streamThread.join()
    serverThread.join()

