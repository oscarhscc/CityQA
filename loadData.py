#!/usr/bin/python                                                                                                                                                           
#coding=utf-8

import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import sys


# set mapping
def set_mapping(es, index_name="城市信息", doc_type_name="FAQ"):
    mapping = {
        "properties": {
            "city": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart"
            },
            "scenery": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart"
            },
            "foods": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart"
            }
        }
    }

    es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(index=index_name, ignore=True)
    es.indices.put_mapping(index=index_name, doc_type=doc_type_name, body=mapping)


def set_date(es, index_name="城市信息", doc_type_name="FAQ"):
    actions = []

    i = 1
    with open(u'city_info.txt', 'r', encoding="utf-8") as cityfile:
        reader = cityfile.readlines()
        for row in reader:
            action = {
                "_index": index_name,
                "_type": doc_type_name,
                "_id": i,
                "_source": {
                    "city": row[0],
                    "scenery": row[1],
                    "foods": row[2],
                }
            }

            i = i + 1

            actions.append(action)

    success, _ = bulk(es, actions, index=index_name, raise_on_error=True)
    print('Performed %d actions' % success)


if __name__ == '__main__':
	es = Elasticsearch(hosts=["192.168.1.118:9200"], timeout=5000)  # 118
	#es = Elasticsearch(hosts=["116.6.230.44:9200"], timeout=5000)  # 165
	set_mapping(es)
	set_date(es)
