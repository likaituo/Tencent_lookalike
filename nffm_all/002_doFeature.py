import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from scipy import sparse
import os
import numpy as np
import time
import random
import gc
import warnings
warnings.filterwarnings("ignore")

print('#####################加载数据##################')
train = pd.read_csv('./data/train.csv')
evals = pd.read_csv('./data/evals.csv')
#test1 = pd.read_csv('./data/test1.csv')
test2 = pd.read_csv('./data/test2.csv')

print('#####################加载CV_cvr数据##################')
train_cvcvr = pd.read_csv('./data/train_x_CV_cvr_select.csv')
evals_cvcvr = pd.read_csv('./data/evals_x_CV_cvr_select.csv')
#test1_cvcvr = pd.read_csv('./data/test1_x_CV_cvr_select.csv')
test2_cvcvr = pd.read_csv('./data/test2_x_CV_cvr_select.csv')

print('#####################加载cvr数据##################')
train_cvr = pd.read_csv('./data/train_x_cvr_select.csv')
evals_cvr = pd.read_csv('./data/evals_x_cvr_select.csv')
#test1_cvr = pd.read_csv('./data/test1_x_cvr_select.csv')
test2_cvr = pd.read_csv('./data/test2_x_cvr_select.csv')

print('#####################加载ratio数据##################')
train_ratio = pd.read_csv('./data/train_x_ratio_select.csv')
evals_ratio = pd.read_csv('./data/evals_x_ratio_select.csv')
#test1_ratio = pd.read_csv('./data/test1_x_ratio_select.csv')
test2_ratio = pd.read_csv('./data/test2_x_ratio_select.csv')

print('合并原始数据')
data = pd.concat([train, evals], ignore_index=True)
#data = pd.concat([data, test1], ignore_index=True)
data = pd.concat([data, test2], ignore_index=True)
print('data shape:', data.shape)

print('合并CV_cvr数据')
data_cvcvr = pd.concat([train_cvcvr, evals_cvcvr], ignore_index=True)
#data_cvcvr = pd.concat([data_cvcvr, test1_cvcvr], ignore_index=True)
data_cvcvr = pd.concat([data_cvcvr, test2_cvcvr], ignore_index=True)
print('data_cvcvr shape:', data_cvcvr.shape)

print('合并cvr数据')
data_cvr = pd.concat([train_cvr, evals_cvr], ignore_index=True)
#data_cvr = pd.concat([data_cvr, test1_cvr], ignore_index=True)
data_cvr = pd.concat([data_cvr, test2_cvr], ignore_index=True)
print('data_cvr shape:', data_cvr.shape)

print('合并ratio数据')
data_ratio = pd.concat([train_ratio, evals_ratio], ignore_index=True)
#data_ratio = pd.concat([data_ratio, test1_ratio], ignore_index=True)
data_ratio = pd.concat([data_ratio, test2_ratio], ignore_index=True)
print('data_ratio shape:', data_ratio.shape)

print('CV_cvr特征等距离散化')
feature = evals_cvcvr.columns.tolist()
for f in feature:
    data_cvcvr[f] = pd.cut(data_cvcvr[f], 10, labels=False)

print('cvr特征等距离散化')
feature = evals_cvr.columns.tolist()
for f in feature:
    data_cvr[f] = pd.cut(data_cvr[f], 10, labels=False)

print('ratio特征等距离散化')
feature = evals_ratio.columns.tolist()
for f in feature:
    data_ratio[f] = pd.cut(data_ratio[f], 10, labels=False)

print('Saving CV_cvr...')
full_data = pd.concat([data, data_cvcvr], axis=1)
print('Saving cvr...')
full_data = pd.concat([full_data, data_cvr], axis=1)
print('Saving ratio...')
full_data = pd.concat([full_data, data_ratio], axis=1)

del data
del data_cvcvr
del data_cvr
del data_ratio
gc.collect()

tr = train_cvcvr.shape[0]
ev = evals_cvcvr.shape[0]
train = full_data[:tr+ev]
test2 = full_data[tr+ev:]

print('train:',tr+ev)
print('test:',test2.shape[0])
print('保存数据...')
train.to_csv('./data/train_cv_cvr_ratio.csv', index=False)
test2.to_csv('./data/test2_cv_cvr_ratio.csv', index=False)
