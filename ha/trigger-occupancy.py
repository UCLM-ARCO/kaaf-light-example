#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import argparse
from requests import post


parser = argparse.ArgumentParser()
services = choices=['turn_on', 'turn_off', 'toggle']
parser.add_argument("service", type=str, choices=services, help="Name of the entity service")
parser.add_argument("entity", type=str, help="Entity ID, without <entity-type>.<platform>")
args = parser.parse_args()

url = "http://localhost:8123/api/services/virtual/%s" % args.service
data = '{"entity_id": "binary_sensor.virtual_%s"}' % args.entity
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI4MWQwMzU0NmRkNDk0ZjYxYmEwNjAwZTc1MTJiM2E5NSIsImlhdCI6MTYyMDA4MTM4MywiZXhwIjoxOTM1NDQxMzgzfQ.M5dlUZndljtdamZ20jUPtWYcCTOi7o-3pfv6SpVFaq0",
    "content-type": "application/json"
}

response = post(url, headers=headers, data=data)
print(response.text)