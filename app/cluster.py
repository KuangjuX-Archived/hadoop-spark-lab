from sklearn.decomposition import PCA, FastICA
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from hdbscan import HDBSCAN


class ClusterLoader:
    def __init__(self, data_path):
        self._df = pd.read_csv(data_path)
        print("Load Data %d lines." % (self._df.shape[0]))

    @property
    def df(self):
        return self._df


def handle_cluster(df):
    all_data = np.array(df.iloc[:, :6])
    label_data = np.array(df.iloc[:, :1])
    # X_reduced = PCA(n_components=2).fit_transform(all_data)
    # sc = StandardScaler()
    # X_reduced = sc.fit_transform(all_data)

    # print(max(predicts))
    # print(len(list(filter(lambda x: x == -1, predicts))))
    # X_reduced=all_data.copy()
    # kmeans = KMeans(n_clusters=3).fit(X_reduced)
    # X_reduced = PCA(n_components=2).fit_transform(all_data)
    # predicts = DBSCAN(eps=0.00001, min_samples=2).fit_predict(X_reduced)
    # kmeans = KMeans(n_clusters=3).fit(X_reduced)
    X_reduced = PCA(n_components=2).fit_transform(all_data)
    # model = HDBSCAN(algorithm='best',
    #                 min_cluster_size=2,
    #                 min_samples=None,
    #                 metric='euclidean')
    # predicts = model.fit_predict(X_reduced)
    predicts = DBSCAN(eps=6).fit_predict(X_reduced)
    print(max(label_data))
    # predicts = model.fit_predict(X_reduced)
    # print(max(predicts))
    # print(len(list(filter(lambda x: x == -1, predicts))))
    plt.title("women_cluster")
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=predicts, cmap=plt.cm.Set1)
    plt.show()


if __name__ == '__main__':
    cl = ClusterLoader('./word_count/cluster_female.csv')
    handle_cluster(cl.df)
