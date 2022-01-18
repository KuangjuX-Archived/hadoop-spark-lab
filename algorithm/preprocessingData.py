__author__ = 'Pumpkin'

import numpy as np
import pandas as pd
import re

# print(pd.DataFrame())
data = pd.read_csv('世纪佳缘-男.csv')
data.columns = ["uid", "education", "height", "car", "income", "house", "weight", "constellation", "nationality",
                "zodiac", "blood", "criterias_age", "criterias_height", "criterias_nationality", "criterias_education",
                "criterias_marriage", "criterias_location", "nickname", "sex", "marriage", "work_location", "image",
                "randTag", "randListTag", "shortnote"]


# 正则表达式：\s.
def clear_characters(text):
    return re.sub('\W', '', text)


data['criterias_education'] = data['criterias_education'].apply(clear_characters)
data['criterias_age'] = data['criterias_age'].apply(clear_characters)
data['criterias_height'] = data['criterias_height'].apply(clear_characters)
data['criterias_marriage'] = data['criterias_marriage'].apply(clear_characters)
data['criterias_location'] = data['criterias_location'].apply(clear_characters)

data.duplicated()  # 判断有无重复行
data.drop_duplicates(subset=["uid", "education", "height", "car", "income", "house", "weight", "constellation",
                             "nationality", "zodiac", "blood", "criterias_age", "criterias_height",
                             "criterias_nationality", "criterias_education", "criterias_marriage", "criterias_location",
                             "nickname", "sex", "marriage", "work_location", "image", "randTag", "randListTag",
                             "shortnote"], keep='first')  # 删除重复行

data['shortnote'] = data['shortnote'].str.replace('key: shortnote, value: ', '')
data['shortnote'] = data['shortnote'].str.replace('?', '', regex=False)
data['education'] = data['education'].str.replace('key: education, value: ', '')
data['height'] = data['height'].str.replace('key: height, value: ', '')
data['car'] = data['car'].str.replace('key: car, value: ', '')
data['income'] = data['income'].str.replace('key: income, value: ', '')
data['house'] = data['house'].str.replace('key: house, value: ', '')
data['weight'] = data['weight'].str.replace('key: weight, value: ', '')
data['weight'] = data['weight'].str.replace('公斤', '')
data['constellation'] = data['constellation'].str.replace('key: constellation, value: ', '')
data['nationality'] = data['nationality'].str.replace('key: nationality, value: ', '')
data['zodiac'] = data['zodiac'].str.replace('key: zodiac, value: ', '')
data['blood'] = data['blood'].str.replace('key: blood, value: ', '')
data['blood'] = data['blood'].str.replace('型', '')
data['blood'] = data['blood'].str.replace('保密', '--')
data['criterias_age'] = data['criterias_age'].str.replace('key: criterias_age, value: ', '')
data['criterias_age'] = data['criterias_age'].str.replace('之间', '')
data['criterias_age'] = data['criterias_age'].str.replace('岁', '')
data['criterias_age'] = data['criterias_age'].str.replace('以下', '')
data['criterias_height'] = data['criterias_height'].str.replace('key: criterias_height, value: ', '')
data['criterias_height'] = data['criterias_height'].str.replace('厘米', '')
data['criterias_height'] = data['criterias_height'].str.replace('或以', '')
data['criterias_height'] = data['criterias_height'].str.replace('上', '')
data['criterias_height'] = data['criterias_height'].str.replace('下', '')
data['criterias_nationality'] = data['criterias_nationality'].str.replace('key: criterias_nationality, value: ', '')
data['criterias_education'] = data['criterias_education'].str.replace('key: criterias_eduction, value: ', '')
data['criterias_marriage'] = data['criterias_marriage'].str.replace('key: criterias_marriage, value: ', '')
data['criterias_location'] = data['criterias_location'].str.replace('key: criterias_location, value: ', '')
data['nickname'] = data['nickname'].str.replace('key: nickname, value: ', '')
data['sex'] = data['sex'].str.replace('key: sex, value: ', '')
data['marriage'] = data['marriage'].str.replace('key: marriage, value: ', '')
data['work_location'] = data['work_location'].str.replace('key: work_location, value: ', '')
data['image'] = data['image'].str.replace('key: image, value: ', '')

# data['randTag'] = data['randTag'].str.replace('key: ', '')
# data['randListTag'] = data['randListTag'].str.replace('key: ', '')
# data['uid'] = data['uid'].str.replace('key: ', '')


data['criterias_age'] = data['criterias_age'].str.replace('fontcolor848284font', '')
data['criterias_height'] = data['criterias_height'].str.replace('fontcolor848284font', '')
data['criterias_education'] = data['criterias_education'].str.replace('fontcolor848284font', '')
data['criterias_marriage'] = data['criterias_marriage'].str.replace('fontcolor848284font', '')
data['criterias_location'] = data['criterias_location'].str.replace('fontcolor848284font', '')

data['criterias_age'] = data['criterias_age'].str.replace('keycriterias_agevalue', '')
data['criterias_height'] = data['criterias_height'].str.replace('keycriterias_heightvalue', '')
data['criterias_education'] = data['criterias_education'].str.replace('keycriterias_eductionvalue', '')
data['criterias_marriage'] = data['criterias_marriage'].str.replace('keycriterias_marriagevalue', '')
data['criterias_location'] = data['criterias_location'].str.replace('keycriterias_locationvalue', '')

data['criterias_age'] = data['criterias_age'].astype(str)
data['criterias_height'] = data['criterias_height'].astype(str)
data['criterias_age'] = data['criterias_age'].str[0:2] + ',' + data['criterias_age'].str[2:]
data['criterias_height'] = data['criterias_height'].str[0:3] + ',' + data['criterias_height'].str[3:]

# axis=1 表示列
data.drop(['uid', 'randListTag', 'randTag', 'image', 'income', 'sex'], axis=1, inplace=True)  # 删除列

# data = data.drop(data.columns[0], axis=1)

data.duplicated()  # 判断有无重复行
data.drop_duplicates(subset="shortnote", keep='first', inplace=True)  # 删除重复行


# 删除索引值为1的行
# data.drop(1)

# data.to_csv('世纪佳缘-女(1).csv')

data.to_csv('male.csv', index=False, encoding='utf_8_sig')
# print(data)
