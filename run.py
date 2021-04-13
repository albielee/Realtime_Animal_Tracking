f = open('DatasetTrain.txt', 'r')
lines = f.readlines()


for i in range(len(lines)):
	lines[i] = '/content'+lines[i][1:]

f = open('DatasetTrain2.txt','w')
f.writelines(lines)
f.close()