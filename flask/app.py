import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL')

import requests
from dotenv import dotenv_values
from flask import Flask, render_template


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
config = dotenv_values(os.path.dirname(os.path.dirname(__file__)) + '/.env')


def get_by_uuid(uuid):
    return get({})


def get(query):
    response = requests.post(
    'http://localhost:1337/graphql',
    headers =  {
		'Content-Type': 'application/json',
			'Authorization':  'Bearer 529aa5620e514391b3acccff6a095a277961c8f41a3ca128bd3c27fd870f80adfaefd13089bb60c614976147753291c11ec2cc58db249cf491e102ca5fc7e8cbc785cc0597ea80a257d9fbac8233bde7da44ea04c18e2da5d530e839f3dba4c7b4c9975416a0ae2078f4d4e822734a3ea54114d246d7842962bb10499df05df7'
    },
    json={'query':query}
    )
    return response.json()

def inspect():
    json = get("""query {
   __type(name:"Drievoor12update") {
      data {
        attributes {
				title
				description
				}
      }
   }}
   """)
    return json


@app.route('/')
def index():
    json = get("""
      query  {
       drievoor12Updates {
            data {
              attributes {
  					    title
	   				    text
		  			    uuid
					    }
        }
      }
   }
    """)
  #  logging.info(inspect())
    return render_template('index.html', updates=json['data']['drievoor12Updates']['data'])

@app.route('/<path:uuid>')
@app.route('/<path:uuid>/<path:title>')
def update(uuid: str, title:str):
    json = get("""query  {
      drievoor12Updates(where: {uuid:"%s"}) {
        data {
          attributes {
          id
          title
          subtitle
          text
          _publish_on
          }
        }
      }
    }
    """ % uuid)
    return render_template('update.html', update=json['data']['drievoor12Updates']['data'][0])


@app.template_filter('datetime')
def filter_datetime(date):
    date = datetime.fromisoformat(date)
    native = date.replace(tzinfo=ZoneInfo('Europe/Amsterdam'))
    return native.strftime('%d %B, %Y')

@app.template_filter('path')
def filter_path(title):
    return title.replace(' ', '-').lower()

if __name__ == "__main__":
    app.run(debug=True)
