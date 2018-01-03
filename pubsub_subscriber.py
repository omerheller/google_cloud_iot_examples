# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses service credentials to subscribe to a topic of the Pub/Sub broker residing in
# Google Cloud.
# Using this code a server can receive messages from the device.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import time
import os
import tweepy  
import sys
import ast

from google.cloud import pubsub
from oauth2client.service_account import ServiceAccountCredentials

project_id = 'iot-weather-project'  # Enter your project ID here
topic_name = 'topic'  # Enter your topic name here
subscription_name = 'my_subscription'  # Can be whatever, but must be unique (for the topic?)
service_account_json = 'service_account.json' # Location of the server service account credential file

# Consumer keys and access tokens, used for OAuth  
consumer_key = 'GsjokoqTGBv4JiJGzFV39djUG'  
consumer_secret = 'ajq1ukXmZpa09gul1HWKnCeaiQ6AIw0vnSSW0SxPpWLIU3Jqu4'  
access_token = '937304494202867712-cEXfYE3huKFatlijRTPh9uisOusDwpb'  
access_token_secret = 'qivv8xozzby4N2XIYhdRrY64e6s5gsj5PcVRLQutDGZPk'

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)
   
# Creation of the actual interface, using authentication  
api = tweepy.API(auth)

def on_message(message):
    """Called when a message is received"""
    if message.data != 'PING':
    	data = ast.literal_eval(message.data)
	#
	#
	# ADD A ROW TO THE DATABASE
	#
	#
    	tweet_text = "Time: %s\nTemperature: %s\nHumidity: %s\nPressure: %s\n" % (data[0], str(data[1]), str(data[2]), str(data[3]))
        if len(tweet_text) <= 280:
            api.update_status(status=tweet_text)
        else:
			print("The following tweet was too long to publish: ", tweet_text)
    print('Received message: {}'.format(message))
    message.ack()


# Ugly hack to get the API to use the correct account file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json

# Create a pubsub subscriber
subscriber = pubsub.SubscriberClient()

topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic_name,
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=subscription_name,
)

# Try to delete the subscription before creating it again
try:
    subscriber.delete_subscription(subscription_name)
except: # broad except because who knows what google will return
    # Do nothing if fails
    None

# Create subscription
subscription = subscriber.create_subscription(subscription_name, topic)

# Subscribe to subscription
print "Subscribing"
subscriber.subscribe(subscription_name, callback=on_message)

# Keep the main thread alive
while True:
    time.sleep(100)
