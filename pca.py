import numpy as np
import pandas as pd
from sklearn import preprocessing

data = pd.read_csv('./problem2_1/new1_105.csv',encoding='gbk')
del data['Unnamed: 0']
a = data.head()

# def pca(data,alpha=0.85):
def pca(data,n_components):
    assert n_components <= data.shape[1]

    scaler = preprocessing.StandardScaler().fit(data)
    input = scaler.transform(data).astype(dtype='float32')

    cor = np.corrcoef(input)

    eigvalue = np.linalg.eig(cor)[0].astype(dtype='float32')
    eigvector = np.linalg.eig(cor)[1].astype(dtype='float32')

    # 贡献率，并按照升序排序
    contribute = [item / np.sum(eigvalue) for item in eigvalue]
    sort = np.argsort(contribute)

    pca = []

    # token = 0
    # i = 1
    # while token <= alpha:
    #     # len(input)-i是从后往前提取，即反向
    #     token += contribute[sort[len(input) - i]]
    #     pca.append(sort[len(input) - i])
    #     i += 1
    
    i = 1
    while i <= n_components:
        pca.append(sort[len(input) - i])
        i += 1

    pca_eig = {}
    for i in range(len(pca)):
        pca_eig[i+1] = [eigvalue[pca[i]]/sum(eigvalue),eigvector[pca[i]]]
    return pca_eig

x = pca(np.asmatrix(a.values),n_components=3)
print(x)
