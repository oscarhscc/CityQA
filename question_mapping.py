#!/usr/bin/python
# coding=utf-8

from refo import finditer, Predicate, Star, Any
import re


class WordReplace(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(WordReplace, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        return self.action(matches), self.condition_num


pos_city = "city"
pos_culture = "cul"
pos_scene = "scene"
pos_food = "food"

city_entity = (WordReplace(pos=pos_city))
culture_entity = (WordReplace(pos=pos_culture))
scene_entity = (WordReplace(pos=pos_scene))
food_entity = (WordReplace(pos=pos_food))

city = (WordReplace("城市") | WordReplace("地方") | WordReplace("位置") | WordReplace("地点") | WordReplace("哪儿") | WordReplace("哪") | WordReplace("哪里"))
food = (WordReplace("吃的") | WordReplace("小吃") | WordReplace("美食") | WordReplace("好吃的") | WordReplace("特产"))
culture = (WordReplace("风俗") | WordReplace("文化") | WordReplace("人文") | WordReplace("风情") | WordReplace("特色") | WordReplace("风土人情"))
scene = (WordReplace("景点") | WordReplace("美景") | WordReplace("风景") | WordReplace("好玩"))
introduce = (WordReplace("介绍") | WordReplace("简介") | WordReplace("描述") | WordReplace("了解"))


class Question:
    def __init__(self):
        pass

    @staticmethod
    def city_question_search(word_objects):
        query = None
        for w in word_objects:
            if w.pos == pos_city:
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "default_field": "city",
                                        "query": w.token
                                    }
                                }
                            ]
                        }
                    },
                    "size": 100
                }
                break
        return query

    @staticmethod
    def culture_question_search(word_objects):
        query = None
        for w in word_objects:
            if w.pos == pos_culture:
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "default_field": "cultures",
                                        "query": w.token
                                    }
                                }
                            ]
                        }
                    },
                    "size": 100
                }
                break
        return query

    @staticmethod
    def food_question_search(word_objects):
        query = None
        for w in word_objects:
            if w.pos == pos_food:
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "default_field": "foods",
                                        "query": w.token
                                    }
                                }
                            ]
                        }
                    },
                    "size": 100
                }
                break
        return query

    @staticmethod
    def scene_question_search(word_objects):
        query = None
        for w in word_objects:
            if w.pos == pos_scene:
                query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "default_field": "scenery",
                                        "query": w.token
                                    }
                                }
                            ]
                        }
                    },
                    "size": 100
                }
                break
        return query


'''
1.广州有什么景点 | 有哪些景点是广州的
2.成都有哪些美食 | 有哪些美食是成都的
3.乌鲁木齐有哪些风俗 | 哪些风俗是乌鲁木齐的
4.臭豆腐是哪个城市的小吃| 哪个城市有串串香
5.介绍一下深圳 | 给我深圳的介绍
6.哈尔滨是一个什么样的城市
7.天安门在哪儿 | 哪儿有天安门
8.花鼓灯是哪儿的 | 哪儿有花鼓灯
'''

rules = [
    Rule(condition_num=1, condition=((city_entity + Star(Any(), greedy=False) + scene + Star(Any(), greedy=False)) |
                                     (scene + Star(Any(), greedy=False) + city_entity + Star(Any(), greedy=False))),
         action=Question.city_question_search),
    Rule(condition_num=2, condition=((city_entity + Star(Any(), greedy=False) + food + Star(Any(), greedy=False)) |
                                     (food + Star(Any(), greedy=False) + city_entity + Star(Any(), greedy=False))),
         action=Question.city_question_search),
    Rule(condition_num=3, condition=((city_entity + Star(Any(), greedy=False) + culture + Star(Any(), greedy=False)) |
                                     (culture + Star(Any(), greedy=False) + city_entity + Star(Any(), greedy=False))),
         action=Question.city_question_search),
    Rule(condition_num=4, condition=((food_entity + Star(Any(), greedy=False) + city + Star(Any(), greedy=False)) |
                                     (city + Star(Any(), greedy=False) + food_entity + Star(Any(), greedy=False))),
         action=Question.food_question_search),
    Rule(condition_num=5, condition=((introduce + Star(Any(), greedy=False) + city_entity + Star(Any(), greedy=False)) |
                                     (city_entity + Star(Any(), greedy=False) + introduce + Star(Any(), greedy=False))),
         action=Question.city_question_search),
    Rule(condition_num=6, condition=(city_entity + Star(Any(), greedy=False) + city + Star(Any(), greedy=False)),
         action=Question.city_question_search),
    Rule(condition_num=7, condition=((scene_entity + Star(Any(), greedy=False) + city + Star(Any(), greedy=False)) |
                                     (city + Star(Any(), greedy=False) + scene_entity + Star(Any(), greedy=False))),
         action=Question.scene_question_search),
    Rule(condition_num=8, condition=((culture_entity + Star(Any(), greedy=False) + city + Star(Any(), greedy=False)) |
                                     (city + Star(Any(), greedy=False) + culture_entity + Star(Any(), greedy=False))),
         action=Question.culture_question_search)
]
