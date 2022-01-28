import math

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


def show_edu(mdf, fdf):
    ry1 = []
    ry2 = []
    y1 = []
    y2 = []
    xticks = ['高中中专及以下', '大专', '本科', '硕士', '博士']
    for item in xticks:
        ry1.append(mdf[mdf['education'].str.contains(item)].shape[0])
        ry2.append(fdf[fdf['education'].str.contains(item)].shape[0])
    for m, f in zip(ry1, ry2):
        y1.append(round(100 * m / sum(ry1), 2))
        y2.append(round(100 * f / sum(ry2), 2))
    plt.title('学历图', fontsize=13)
    plt.bar(np.arange(len(y1)), y1, width=0.4, color='tomato', label='男性')
    for x, y in enumerate(y1):
        plt.text(x, y, str(y)+'%')

    plt.bar(np.arange(len(y2)) + 0.4, y2, width=0.4, color='steelblue', label='女性')
    for x, y in enumerate(y2):
        plt.text(x + 0.4, y, str(y)+'%')

    plt.xticks(np.arange(len(xticks)) + 0.4 / 2, xticks)
    plt.ylabel('占比%')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    fdl = DataLoader('./raw_data/female.csv')
    mdl = DataLoader('./raw_data/male.csv')
    show_edu(mdl.df, fdl.df)
