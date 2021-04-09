f = open('DatasetTest.txt', 'r')
lines = f.readlines()


for i in range(len(lines)):
	lines[i] = './model_data/'+lines[i]

f = open('DatasetTest.txt','w')
f.writelines(lines)
f.close()