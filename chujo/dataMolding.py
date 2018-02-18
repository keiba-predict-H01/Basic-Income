#coding:utf-8
import numpy as np
import pandas as pd

#名前にindex付け
def set_index(matrix,name):
	mat = matrix.sort_values(by = name).loc[:,name].value_counts().sort_index()
	#mat = mat.value_counts().sort_index()
	for i in range(mat.shape[0]):
		mat[i] = i+1
	return mat

#日付の一覧取得
def getViewDate(matrix,str = '日付'):
	return matrix.loc[:,str].value_counts().sort_index().index

#特定の行の抽出
def getValueRace(matrix,columns,value):
	return matrix.loc[matrix[columns] == value]

def normalization(matrix,columns):
	maxVal = max(matrix[columns])
	matrix[columns] = (matrix[columns] / maxVal)
	return matrix

def main():
	horse = pd.read_csv("/Users/tadamasa/Documents/failedFactory/data/keibaData.csv",header=0)
	train = horse.loc[:,['着順','馬名','馬番','斤量','騎手','単勝','人気','馬体重','調教師','日付']]
#index付け
	mat = set_index(train,'騎手')
	print(mat)
	#mat.to_csv("horse_index.csv",encoding= 'shift_jis')

#日付一覧取得
	mat = getViewDate(train)
	print(mat)
	mat = train.sort_values(by = '日付').loc[:,'日付'].value_counts().sort_index()
	print(mat)

#テストデータの取得
	test = getValueRace(train,"日付",201606050311)
	print(test,test.shape)
	print()
#訓練データの取得
	for i in range(test.shape[0]):
		mat = getValueRace(train,"馬名",test["馬名"].iloc[i])
		print(mat,mat.shape)




#データのID変換
'''
	mat = set_index(train,'騎手')
	for i in range(train):
		for j in mat:
			if train['騎手'] == mat[j].index:
				train['騎手'] == mat[j]
	print(mat)
'''



if __name__ == '__main__':
	main()
