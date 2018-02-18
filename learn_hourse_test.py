import numpy as np
import matplotlib as plt
import pandas as pd
from chainer import cuda,Variable,optimizers
import chainer.functions as F
import chainer.links as L

import dataMolding as M

def createModel(input,hidden,output):
	l1 = L.Linear(input,hidden)
	l2 = L.Linear(hidden,output)
	return (l1,l2)

def forward(x,inLayer,outLayer):
	h = inLayer(x)#ここでエラー
	return outLayer(h)

def nameToValue(matrix,name_list,dataName = "順位"):
	value = 0.0
	cnt = 0
	print(name_list.iloc[0])
	for i in name_list:
		mat = matrix

def main():
	#initilize
	horse = pd.read_csv("/Users/tadamasa/Documents/failedFactory/data/keibaData.csv",header=0)
	horse = horse.loc[:,['着順','馬名','馬番','斤量','騎手','馬体重','日付']]

	#馬番、斤量、
	test = M.getValueRace(horse,"日付",201606050311)
	print(test)
	#訓練データの生成
	for i in range(test.shape[0]):
		if i==0:
			train = M.getValueRace(horse,"馬名",test["馬名"].iloc[i])
		else:
			train = pd.concat([train,M.getValueRace(horse,"馬名",test["馬名"].iloc[i])])

	print(train,train.shape)

	#maxVal = max(train["馬番"])
	#print(maxVal)
#数値情報の正規化
	train = M.normalization(train,"馬番")
	train = M.normalization(train,"斤量")
#馬体重の算出
	train["馬体重"] = train["馬体重"].str[0:3].astype(float)
	train = M.normalization(train,"馬体重")
	print(train)

	nameToValue(horse,test["馬名"])

	tmp = M.set_index(train,"馬名")

#馬、騎手の平均順位
'''
	tmp = test.loc[:,["馬名"]]
	for i in tmp:
		if i == 0:
			mean = train[train["馬名"] = tmp.iloc[i]].mean()
		else:
			mean = pd.concat(mean,train[train["馬名"] = tmp.iloc[i]].mean())
'''

if __name__ == '__main__':
	main()
