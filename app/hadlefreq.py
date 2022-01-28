import json
import random
from copy import deepcopy

if __name__ == '__main__':
    item_nums = 100
    data_path = './word_count/freqItemsets(1).csv'
    graph = {}
    node = []
    existword = {}
    with open(data_path, 'r',encoding='utf8') as reader:
        id = 0
        for line in reader.readlines()[:20]:
            # print(line)
            a, b, n = line.strip().split(',')

            if a not in existword.keys():
                temp = {}
                temp['id'] = str(id)
                temp['name'] = a
                temp["symbolSize"] = int(n) / 900
                if random.randint(0, 9) < 5:
                    temp["category"] = 'A'
                else:
                    temp["category"] = 'B'
                temp["x"] = random.randint(-5, 20)
                temp["y"] = random.randint(-5, 20)
                node.append(deepcopy(temp))
                id += 1

            if b not in existword.keys():
                temp = {}
                temp['id'] = str(id)
                temp['name'] = a
                temp["symbolSize"] = int(n) / 900
                if random.randint(0, 9) < 5:
                    temp["category"] = 'A'
                else:
                    temp["category"] = 'B'
                temp["x"] = random.randint(-5, 20)
                temp["y"] = random.randint(-5, 20)
                node.append(deepcopy(temp))
                id += 1
    graph['node']=node
    data = json.dumps(graph).decode("unicode-escape")
    print(data)