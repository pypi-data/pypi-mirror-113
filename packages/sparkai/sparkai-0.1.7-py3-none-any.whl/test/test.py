#!/usr/bin/env python3

from lib import SparkAIClient
import os
import sys

api_key = None
try:
    api_key = os.environ['SPARKAI_API_KEY']
except:
    print('SPARKAI_API_KEY needs to be set')
    sys.exit()

client = SparkAIClient(api_key=api_key)
print(client.create_new_engagement_from_url('https://picsum.photos/640/480'))
