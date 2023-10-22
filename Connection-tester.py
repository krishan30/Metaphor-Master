
from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

print(es.info())
