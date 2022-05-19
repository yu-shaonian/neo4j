#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import json
from py2neo import Graph,Node

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.g = Graph(
            host="10.7.12.89",
            port=7474,
            user="neo4j",
            protocol="http",
            password="guojun")
        self.num_limit = 20

    def chat_lawyer(self, sent):
        answer = '您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！'

        lawyer_ques = sent
        sql = 'match(m)-[r:professional]-(n) where n.name="{}" return m.name, m.document,m.introduction,m.link limit 5'.format(
            lawyer_ques)
        ress = self.g.run(sql).data()
        answer_final = ''
        print("下面是律师推荐：")
        answer_final += "下面是律师推荐："
        for i in ress:
            print(i['m.name'])
            if (len(i['m.document']) > 10):
                doc = i['m.document'].replace('\n', '').replace('\r', '')
                print(doc)
                answer_final += doc
            if (len(i['m.introduction']) > 10):
                inr = i['m.introduction'].replace('\n', '').replace('\r', '')
                print(inr)
                answer_final += inr
            print(i['m.link'])
            answer_final += i['m.link']
            return answer_final

    def chat_ques(self, sent):
        answer = '您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系运行维护人员。祝您身体棒棒！'

        lawyer_ques = sent
        sql_traffic = 'match(n:Traffic) where n.question="{}" return n.answer'.format(
            lawyer_ques)
        sql_company = 'match(n:Company) where n.question="{}" return n.answer'.format(
            lawyer_ques)
        sql_money = 'match(n:Money) where n.question="{}" return n.answer'.format(
            lawyer_ques)
        sql_worker = 'match(n:Worker) where n.question="{}" return n.answer'.format(
            lawyer_ques)
        ress1 = self.g.run(sql_traffic).data()
        ress2 = self.g.run(sql_company).data()
        ress3 = self.g.run(sql_money).data()
        ress4 = self.g.run(sql_worker).data()
        ress = []
        if(len(ress1)>0):
            ress = ress1
        if(len(ress2)>0):
            ress = ress2
        if(len(ress3)>0):
            ress = ress3
        if(len(ress4)>0):
            ress = ress4
        try:
            answer_final = ress[0]['n.answer'].replace('\n\n','\n')
            print(answer_final)
            return answer_final
        except:
            return answer





if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        handler.chat_ques(question)


