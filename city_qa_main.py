#!/usr/bin/python
# coding=utf-8

import query_analysis
import elastic_connnect

if __name__ == '__main__':
    es = elastic_connnect.ElasticConnect()
    query2search = query_analysis.QuestionMatch([u'./data/city.txt', u'./data/culture.txt',
                                                 u'./data/food.txt', u'./data/scene.txt', u'./data/extend.txt'])

    while True:
        query = input("请输入问题(输入q退出): ")
        if query == 'q':
            break

        condition_num, values = query2search.get_result(query)

        print('con_num: {}, values: {}'.format(condition_num, values))

        if values is not None:
            es_result = es.query_search(query=values)
            results = es.get_es_result(condition_num=condition_num, result=es_result)
            print(results)
        else:
            print("我不晓得你在说啥子...")
