import jwt
import paho.mqtt.client as mqtt
import threading
import sys

from mqtt_publisher import main1
from mqtt_config_subscriber import main2

publisherThread = threading.Thread(target=main1)
configSubscriberThread = threading.Thread(target=main2)

configSubscriberThread.start()
publisherThread.start()
