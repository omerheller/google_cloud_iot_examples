# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses service credentials to modify device configuration over REST API of Google Cloud.
# Using this code a server can change the configuration of the device.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import base64
import datetime
import json
import rsa

import googleapiclient
import jwt
import requests

from google.oauth2 import service_account
from googleapiclient import discovery

service_account_json = 'service_account.json' # Location of the server service account credential file
device_id = 'my-device'  # Enter your Device ID here
project_id = 'iot-weather-project'  # Enter your project ID here
registry_id = 'my-registry'  # Enter your Registry ID here
#message = '1 False'
#message2 = '4 True'
now = datetime.datetime.now()
with open('priv_key.pem', mode='rb') as privatefile:
     keydata = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)
  # This is the configuration to be sent to the device, any binary data should work

# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
###

device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
    project_id, cloud_region, registry_id, device_id)


def get_client():
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)

def sendMaliciousConfig(message,filename):

	f = open(filename,"rb") #opens file 

	
	signature = f.read()
	configuration_payload = str([message, signature])

	body = {"versionToUpdate": "0", "binaryData": base64.urlsafe_b64encode(configuration_payload)}

	get_client().projects().locations().registries().devices().modifyCloudToDeviceConfig(name=device_name,
                                                                                           body=body).execute()

	print 'Sent Malicious Configuration'
