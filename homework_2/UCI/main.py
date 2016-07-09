# -*- coding: utf-8 -*-

import os
import apriori
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

dataSet = []

source_file_path = 'diagnosis_parsed.txt'
with open(os.path.join(source_file_path), 'r') as f:
	for line in f:
		#print('line', line)
		tmp_data = []
		line = line.rstrip('\n')
		line_details = line.split(',')
		for v in line_details:
			tmp_data.append(v)
		#print('tmp_data', tmp_data)
		#print('len tmp_data', len(tmp_data))
		#if len(tmp_data) > 1 and tmp_data not in dataSet:
		if tmp_data not in dataSet:
			dataSet.append(tmp_data)
f.close()

#print('dataSet', dataSet)

#dataSet = apriori.loadDataSet()

#C1 = apriori.createC1(dataSet)

#D = map(set, dataSet)
#print('D', D)
#L1, suppData0 = apriori.scanD(D, C1, 0.5)

#频繁项集L
#所有候选项集的支持度信息suppData
L, suppData = apriori.apriori(dataSet, 0.3)

print('L:', L)
#print('suppData:', suppData)
rules = apriori.generateRules(L, suppData, minConf = 0.3)
#print('rules', len(rules))

rules_remove_redundancy = []
def remove_redundancy():

	redundancy_indices = []

	for i in range(0, len(rules) - 1):
		for j in range(i + 1, len(rules)):
			if rules[i][0] < rules[j][0] and rules[i][1] < rules[j][1] and rules[i][4] <= rules[j][4]:
				if i not in redundancy_indices:
					redundancy_indices.append(i)

			if rules[j][0] < rules[i][0] and rules[j][1] < rules[i][1] and rules[j][4] <= rules[i][4]:
				if j not in redundancy_indices:
					redundancy_indices.append(j)
	#print('redundancy_indices', len(redundancy_indices))

	for i in range(0, len(rules)):
		if i not in redundancy_indices:
			rules_remove_redundancy.append(rules[i])
	#for k in redundancy_indices:
		#del rules[k]

remove_redundancy()
#print('rules_remove_redundancy', len(rules_remove_redundancy))

def plot():

	sur = []
	con = []
	for v in rules_remove_redundancy:
		print(v)
		sur.append(v[2])
		con.append(v[3])

	#plt.scatter(sur, con)
	plt.hist2d(sur, con, bins = 40, norm = LogNorm())
	plt.colorbar()
	plt.xlim(xmin = 0.3)
	#plt.ylim(ymin = 0.3)
	plt.show()

plot()
