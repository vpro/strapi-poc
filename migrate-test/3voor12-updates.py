#!/usr/bin/env python3
import os

import requests
from elasticsearch import Elasticsearch, helpers
from dotenv import dotenv_values
from datetime import datetime
import markdownify




config = dotenv_values(os.path.dirname(os.path.dirname(__file__)) + '/.env')

headers={
    'Authorization':  'Bearer ' + config['MIGRATE_TOKEN']
}
API_URL='http://' + config['HOST'] + ":" + config['PORT'] + "/api"

def post_to_strapi(json):
	incoming_uuid = json['uuid']
	check = requests.get(API_URL + "/drievoor12updates?filters[uuid][$eq]=" + incoming_uuid, headers=headers)
	check_json = check.json()
	if len(list(check_json['data'])) > 0:
		response = requests.put(API_URL + "/drievoor12updates/" + str(list(check_json['data'])[0]['id']),
		headers= headers,
		json={
		  "data":	json
		})
	else:
		response = requests.post(API_URL + "/drievoor12updates/",
		headers= headers,
		json={
		  "data":	json
		}
	    )
	if response.status_code >= 200 and response.status_code < 300:
		print(response.status_code)
		if response.status_code == 204:
			pass
		else:
			print(response.json())
		return
	elif 400 == response.status_code:
		print(response.json())
		pass
	else:
		raise Exception("Error posting to strip: " + str(response.status_code) + " " + response.text)


def map_to_strapi(source):
	return {
	'uuid': source['id'],
	'title': source['title'],
	'subtitle': source['subtitle'],
	'text': markdownify.markdownify(source['text']),
	'publishDate': datetime.fromtimestamp(source['publishDate'] / 1000).isoformat(),
	'type': source['type'],

	 }



def migrate():
	es = Elasticsearch("http://localhost:9210")
	resp = helpers.scan(
	es,
	index="3voor12_updates",
	scroll = '3m',
	preserve_order=True,
	query= {
	'sort':'publishDate:desc'
	}
	)

	for num, doc in enumerate(resp):
	   print("%s" % str(doc))
	   source = doc["_source"]
	   print(num)
	   post_to_strapi(map_to_strapi(source))


migrate()
