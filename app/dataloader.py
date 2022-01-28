import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class DataLoader():

    @property
    def df(self):
        return self._df

    def __init__(self, data_path):
        self._df = pd.read_csv(data_path)
        print("Load Data %d lines." % (self._df.size))


def count_height(df):
    # male range
    height_area = [160, 165, 170, 175, 180, 185, 190]
    result = []
    for index, height in enumerate(height_area):
        ndf = df[(df['height'] >= height) & (df['height'] < height + 5)]
        result.append(ndf.shape[0])
        print(ndf.shape[0])
    plt.title('男性身高')
    bar = plt.bar(list(map(lambda x: '{}-{}'.format(x, x + 5), height_area)), result)
    plt.bar_label(bar, label_type='edge')
    plt.show()


def show_possesion(df):
    sizes = []

    ndf = df[((df['car'].str.contains('已经购车') | df['car'].str.contains('已购车')) & (
        (df['house'].str.contains('已购房') | df['house'].str.contains('已购住房'))))]
    sizes.append(ndf.shape[0])

    ndf = df[((df['car'].str.contains('暂未购车') | df['car'].str.contains('--')) & (
        (df['house'].str.contains('已购房') | df['house'].str.contains('已购住房'))))]
    sizes.append(ndf.shape[0])

    ndf = df[((df['car'].str.contains('已经购车') | df['car'].str.contains('已购车')) & (
        (df['house'].str.contains('暂未购房') | df['house'].str.contains('需要时购置') | df['house'].str.contains('与父母同住'))))]
    sizes.append(ndf.shape[0])

    ndf = df[((df['car'].str.contains('暂未购车') | df['car'].str.contains('--')) & (
        (df['house'].str.contains('暂未购房') | df['house'].str.contains('需要时购置') | df['house'].str.contains('与父母同住'))))]
    sizes.append(ndf.shape[0])

    print(sizes)

    labels = ['有房有车', '有房无车', '有车无房', '无车无房']
    explode = (0, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.title("女性住房购车情况")
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    dl = DataLoader('./raw_data/female.csv')
    show_possesion(dl.df)
