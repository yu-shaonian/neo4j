import os
import json
from py2neo import Graph,Node

class LawBuild:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, '../lawdata/kg_crime.json')
        self.data_money_path = os.path.join(cur_dir, '../lawdata/money.xls') #债务问题
        self.data_traffic_path = os.path.join(cur_dir, '../lawdata/traffic.xls') #债务问题


        self.g = Graph(
            host="10.7.12.89",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            port=7474,  # neo4j 服务器监听的端口号
            protocol = "http",
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="guojun")

    def read_nodes(self):
        # 共8类节点
        crimes = [] #罪行
        crime_bigs = [] # 大的犯罪
        # crime_smalls = []  #小的犯罪
        laws       = []  #法律条文
        crime_links = []
        concepts =    []    #概念
        punishment   = []   #处罚
        explantions  = []   #解释
        defences     = []   #辩护


        # 构建节点实体关系（7类别关系）
        rels_belong = [] #　罪行归属
        rels_punish = [] #   罪行处罚
        rels_law = [] # 罪行对应法律条纹
        rels_concept = [] # 罪行概念解释
        rels_defence = [] # 犯罪辩护
        rels_explantion = [] # 罪行解释
        rels_link = [] # 罪行对应链接

        crime_infos = []#犯罪信息




        count = 0
        for data in open(self.data_path,encoding='utf-8'):
            crime_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            crime = data_json['crime_small']
            crime_dict['name'] = crime
            crimes.append(crime)
            crime_dict['crime_big'] = ''
            crime_dict['crime_link'] = ''
            crime_dict['concept'] = ''   #gainian   概念
            crime_dict['symptom'] = ''    #tezheng  特征
            crime_dict['difference'] = ''   #rending
            crime_dict['punish'] = ''      #chufa  处罚
            crime_dict['law'] = ''         #fatiao法条
            crime_dict['explantion'] = ''   #jieshi解释
            crime_dict['defence'] = ''      #bianhu辩护

            if 'crime_big' in data_json:
                # crime_bigs += data_json['crime_big']
                crime_dict['crime_big'] = data_json['crime_link']
                rels_belong.append([crime,data_json['crime_big']])
                crime_bigs.append(data_json['crime_big'])

            if 'crime_link' in data_json:
                crime_dict['crime_link'] = data_json['crime_link']
                rels_link.append([crime, data_json['crime_link']])
                crime_links.append(data_json['crime_link'])

            if 'gainian' in data_json:
                crime_dict['concept'] = data_json['gainian']
                for _concept in data_json['gainian']:
                    rels_concept.append([crime, _concept])
                    concepts.append(_concept)

            if 'tezheng' in data_json:
                crime_dict['symptom'] = data_json['tezheng']
                # rels_.append([crime, data_json['gainian']])

            if 'rending' in data_json:
                crime_dict['difference'] = data_json['rending']
                # rels_concept.append([crime, data_json['gainian']])

            if 'chufa' in data_json:
                crime_dict['punish'] = data_json['chufa']
                for _punish in data_json['chufa']:
                    rels_punish.append([crime, _punish])
                    punishment.append(_punish)

            if 'fatiao' in data_json:
                crime_dict['law'] = data_json['fatiao']
                for _law in data_json['fatiao']:
                    laws.append(_law)
                    rels_law.append([crime,_law])

            if 'jieshi' in data_json:
                crime_dict['explantion'] = data_json['jieshi']
                for _explantion in data_json['jieshi']:
                    explantions.append(_explantion)
                    rels_explantion.append([crime, _explantion])


            if  'bianhu' in data_json:
                crime_dict['defence'] = data_json['bianhu']
                for _defence in data_json['bianhu']:
                    defences.append(_defence)
                    rels_defence.append([crime, _defence])

            crime_infos.append(crime_dict)





        return crimes, punishment, defences, laws, set(crime_bigs), crime_links, concepts ,\
               (explantions),rels_belong,rels_concept,rels_defence,rels_explantion,rels_law,rels_link,rels_punish,crime_infos

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return


    '''创建知识图谱中心法律的节点'''
    def create_crimes_nodes(self, crime_infos):
        count = 0
        for crime_dict in crime_infos:
            node = Node("Crime", name=crime_dict['name'], crime_big=crime_dict['crime_big'],
                        crime_link=crime_dict['crime_link'] ,concept=crime_dict['concept'],
                        symptom=crime_dict['symptom'],difference=crime_dict['difference'],
                        punish=crime_dict['punish']
                        ,law=crime_dict['law'] , explantion=crime_dict['explantion'],defence=crime_dict['defence'])
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_graphnodes(self):
        # Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        crimes, punishment, defences, laws, crime_bigs, crime_links, concepts, \
        explantions, rels_belong, rels_concept, rels_defence, rels_explantion, rels_law, rels_link, rels_punish, crime_infos = self.read_nodes()

        self.create_crimes_nodes(crime_infos)
        self.create_node('Crime_small', crimes)
        self.create_node('Punishment', punishment)
        self.create_node('Defence', defences)
        self.create_node('Law', laws)
        self.create_node('Crime_big', crime_bigs)
        self.create_node('Crime_link', crime_links)
        self.create_node('Concept', concepts)
        self.create_node('Explantion', explantions)
        return

    def create_graphrels(self):
        crimes, punishment, defences, laws, crime_bigs, crime_links, concepts, \
        explantions, rels_belong, rels_concept, rels_defence, rels_explantion, rels_law, rels_link, rels_punish, crime_infos = self.read_nodes()

        # Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Crime', 'Crime_big', rels_belong, 'belongs_to', '归属')
        self.create_relationship('Crime', 'Concept', rels_concept, 'concept', '概念')
        self.create_relationship('Crime', 'Punishment', rels_punish, 'punish', '惩罚')
        self.create_relationship('Crime', 'Defence', rels_defence, 'to_defence', '辩护')
        self.create_relationship('Crime', 'Law', rels_law, 'law', '对应法条')#这个关系没有添加进行
        self.create_relationship('Crime', 'Crime_link', rels_link, 'link', '链接')
        self.create_relationship('Crime', 'Explantion', rels_explantion, 'explantion', '解释')


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        for edge in edges:
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return





if __name__ == '__main__':
    test = LawBuild()
    test.create_graphnodes()
    test.create_graphrels()