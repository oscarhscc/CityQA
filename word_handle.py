#!/usr/bin/python
# coding=utf-8

import jieba
import jieba.posseg as psg


class Word:
    def __init__(self, token, pos):
        self.token = token  # 分词
        self.pos = pos  # 词性


class Tagger:
    def __init__(self, dict_paths):
        for path in dict_paths:
            jieba.load_userdict(path)

    @staticmethod
    def get_word_objects(sentence):
        for token, tag in psg.cut(sentence):
            print(token, tag)
        return [Word(token, tag) for token, tag in psg.cut(sentence)]
