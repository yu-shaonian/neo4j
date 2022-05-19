import os
import json
from py2neo import Graph,Node
import xlwt  # 进行excel操作
import xlrd

class QuestionBuild:
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
        traffic = []   #交通
        money = []   #债务
        company = []  #公司
        worker = []   #工人
        lawyer = []  #律师
        professonal = []  #律师擅长领域




        rels_prof = [] # 律师擅长领域




        count = 0


        data = xlrd.open_workbook('../lawdata/money.xls')  # 打开xls文件
        table = data.sheets()[0]
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            # 跳过第一行
            if i == 0:
                continue
            money.append(table.row_values(i))
        for i in money:
            node = Node("Money", link=i[0], question=i[1],
                        answer=i[2]
                       )
            self.g.create(node)
            count += 1
        print("money finished")


        data = xlrd.open_workbook('../lawdata/traffic.xls')  # 打开xls文件
        table = data.sheets()[0]
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            # 跳过第一行
            if i == 0:
                continue
            traffic.append(table.row_values(i))
        for i in traffic:
            node = Node("Traffic", link=i[0], question=i[1],
                        answer=i[2]
                       )
            self.g.create(node)
            count += 1
        print("traffic finished")

        data = xlrd.open_workbook('../lawdata/workers.xls')  # 打开xls文件
        table = data.sheets()[0]
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            # 跳过第一行
            if i == 0:
                continue
            worker.append(table.row_values(i))
        for i in worker:
            node = Node("Worker", link=i[0], question=i[1],
                        answer=i[2]
                       )
            self.g.create(node)
            count += 1
        print("worker finished")


        data = xlrd.open_workbook('../lawdata/company.xls')  # 打开xls文件
        table = data.sheets()[0]
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            # 跳过第一行
            if i == 0:
                continue
            company.append(table.row_values(i))
        for i in company:
            node = Node("Company", link=i[0], question=i[1],
                        answer=i[2]
                       )
            self.g.create(node)
            count += 1
        print("Company finished")


        data = xlrd.open_workbook('../lawdata/lawyer_final.xls')  # 打开xls文件
        table = data.sheets()[0]
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            # 跳过第一行
            if i == 0:
                continue
            lawyer.append(table.row_values(i))
            _lawyer = table.row_values(i)
            if(len(table.row_values(i)[3])>5):
                _profess = table.row_values(i)[3].split("\n")
                for j in _profess:
                    professonal.append(j)
                    rels_prof.append([_lawyer[0],j])
        for i in lawyer:
            node = Node("Lawyer", name=i[0], link=i[1],
                        introduction=i[2],professional=i[3],document=i[4]
                       )
            self.g.create(node)
            count += 1
        print("lawyer finished")

        self.create_node('Professonal', professonal)
        self.create_relationship('Lawyer', 'Professonal', rels_prof, 'professional', '擅长领域')



















    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return


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
    test = QuestionBuild()
    test.read_nodes()
