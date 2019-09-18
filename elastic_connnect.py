#!/usr/bin/python
# coding=utf-8

from elasticsearch import Elasticsearch


class ElasticConnect:
    def __init__(self):
        self.elastic_connect = Elasticsearch(hosts=['192.168.1.118'], timeout=50000)

    def query_search(self, query):
        return self.elastic_connect.search(index='城市信息', body=query)

    @staticmethod
    def get_es_result(condition_num, result):
        values = []
        # 广州有什么景点 | 有哪些景点是广州的
        if condition_num == 1:
            for hit in result['hits']['hits']:
                value = hit['_source']['scenery']
            values = value.split('，')
        # 成都有哪些美食 | 有哪些美食是成都的
        elif condition_num == 2:
            for hit in result['hits']['hits']:
                value = hit['_source']['foods']
            values = value.split('，')
        # 乌鲁木齐有哪些风俗 | 哪些风俗是乌鲁木齐的
        elif condition_num == 3:
            for hit in result['hits']['hits']:
                value = hit['_source']['cultures']
            values = value.split('，')
        # 臭豆腐是哪个城市的小吃| 哪个城市有串串香
        elif condition_num == 4:
            for hit in result['hits']['hits']:
                value = hit['_source']['city']
                values.append(value)
        # 介绍一下深圳 | 给我深圳的介绍
        elif condition_num == 5:
            for hit in result['hits']['hits']:
                value = hit['_source']['describe']
                values.append(value)
        # 哈尔滨是一个什么样的城市
        elif condition_num == 6:
            for hit in result['hits']['hits']:
                value = hit['_source']['describe']
                values.append(value)
        # 天安门在哪儿 | 哪儿有天安门
        elif condition_num == 7:
            for hit in result['hits']['hits']:
                value = hit['_source']['city']
                values.append(value)
        # 花鼓灯是哪儿的 | 哪儿有花鼓灯
        elif condition_num == 8:
            for hit in result['hits']['hits']:
                value = hit['_source']['city']
                values.append(value)

        return list(set(values))
