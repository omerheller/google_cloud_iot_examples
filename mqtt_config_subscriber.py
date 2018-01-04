# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses device credentials to subscribe to the device configuration topic of the MQTT broker residing in
# Google Cloud.
# Using this code a device can receive configuration from the server.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import datetime
import time

import jwt
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

configVar = ['1', 'False']

project_id = 'iot-weather-project'  # Enter your project ID here
registry_id = 'my-registry'  # Enter your Registry ID here
device_id = 'my-device'  # Enter your Device ID here
ca_certs = 'roots.pem'  # The location of the Google Internet Authority certificate, can be downloaded from https://pki.google.com/roots.pem
private_key_file = 'rsa_private.pem'  # The location of the private key associated to this device

# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
algorithm = 'RS256'
mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443  # port 8883 is blocked in BGU network
mqtt_topic = '/devices/{}/{}'.format(device_id, 'config')  # The 'config' topic is subscribed to
###


def create_jwt():
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # The time the token expires.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('config_subscriber: on_connect', mqtt.connack_string(rc))
    # Subscribe to the topic of interest once connected
    client.subscribe(mqtt_topic, 0)

def sensorAlert():
    sense = SenseHat()
    red = (255, 0, 0)

    for i in range(3):
        sense.clear()
        time.sleep(1)
        sense.clear(red)
        time.sleep(1)

    sense.clear()

def on_message(unused_client, unused_userdata, msg):
    """Callback for when a message is received."""
    #
    # CHECK SIGNATURE OF MESSAGE
    #
    global configVar
    configVar = msg.payload.split()
    if(configVar[1] == 'True'):
        sensorAlert()
    print("configVar has changed to:", configVar)
    #print ("Received", msg.topic, msg.qos, msg.payload)

def getConfig():
    return int(configVar[0])

def on_subscribe(unused_client, unused_userdata, mid, qos):
    print("Subscribed to Topic", mqtt_topic, qos)


# Create an mqtt client that includes the device path
client = mqtt.Client(
    client_id=('projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id,
        cloud_region,
        registry_id,
        device_id)))

def main2():
    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username='unused',
        password=create_jwt()
    )

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # Start the network loop.
    client.loop_forever()
