#!/usr/bin/python
# coding=utf-8


import word_handle
import queation_mapping


class QuestionMatch:
    def __init__(self, dict_paths):
        self.tw = word_handle.Tagger(dict_paths)  # 自定义分词
        self.rules = queation_mapping.rules  # 定义搜索规则

    def get_result(self, question):  # 语义解析
        word_objects = self.tw.get_word_objects(question)
        queries_dict = dict()

        for rule in self.rules:
            query, num = rule.apply(word_objects)
            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return 0, None
        elif len(queries_dict) == 1:
            for key, value in queries_dict.items():
                return key, value
        else:
            # TODO 匹配多个语句，以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.items(), key=lambda item: item[0], reverse=False)
            return sorted_dict[0][0], sorted_dict[0][1]
