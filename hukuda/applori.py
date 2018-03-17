# -*- coding: utf-8 -*-
import numpy as np
import SQLCollection as SQLC


def cosSim(horceInfoMatrix, standard, target):
	#ord:n乗根するためのパラメータ、axis:ノルムの取り方、axis=1は行ごと
	norm = np.linalg.norm(horceInfoMatrix, ord=2, axis=1)
	normalized_horceInfoVec = horceInfoMatrix / norm[:, np.newaxis]

	return np.dot(horceInfoMatrix[standard], horceInfoMatrix[target])

#出場馬間の類似度計算
def horceApplori(elementMatrix, horceNameId):
	#本来のhorceNameIdは枠番を想定。よって枠番1と2以降を計算、その後枠番2と3以降...を計算
	for i in range(len(elementMatrix)):
		standard = i
		apploriResult = np.empty((0,3), float)
		for j in range(len(elementMatrix)):
			target = j
			apploriResultElement = np.array([])
			#result = str(horceNameId[i]) + "と" + str(horceNameId[j]) + "間:" + str(cosSim(elementMatrix, standard, target))
			apploriResultElement = np.append(apploriResultElement, horceNameId[i])
			apploriResultElement = np.append(apploriResultElement, horceNameId[j])
			apploriResultElement = np.append(apploriResultElement, str(cosSim(elementMatrix, standard, target)))
			apploriResult = np.append(apploriResult, np.array([apploriResultElement]), axis=0)
	return apploriResult

if __name__ == "__main__":
	
	sqlhorse_jokey_zisyolection = SQLC.SQLCollection()
	#テスト用データセット作成
	SVMTestData = sqlhorse_jokey_zisyolection.getTestData()
	elementMatrix = np.empty((0,3), float)
	horceNameId = np.array([])
	for test in SVMTestData:
		horceNameId = np.append(horceNameId,test[1])
		elementVector = np.array([])
		elementVector = np.append(elementVector, test[4]*1.0)
		elementVector = np.append(elementVector, test[5]*1.0)
		elementVector = np.append(elementVector, test[8]*1.0)
		elementMatrix = np.append(elementMatrix, np.array([elementVector / np.linalg.norm(elementVector)]), axis=0)
	print(horceApplori(elementMatrix,horceNameId))