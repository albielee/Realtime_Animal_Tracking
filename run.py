"""
from PIL import Image

for i in range(1060):
	im1 = Image.open(r'./model_data/image'+str(i)+'.png')
	rgb_im = im1.convert('RGB')
	rgb_im.save(r'./model_data/jpgs/image'+str(i)+'.jpg')
"""
"""
f = open('./model_data/DatasetTrain.txt', 'r')
lines = f.readlines()

for i in range(len(lines)):
	lines[i] = lines[i].replace('.png','.jpg')

f = open('./model_data/DatasetTrain.txt','w')
f.writelines(lines)
f.close()
"""
"""
f = open('./model_data/DatasetTrain.txt', 'r')
lines = f.readlines()

for i in range(len(lines)):
	splits = lines[i].split(' ')
	splits.pop()
	lines[i] = splits.pop(0)
	for s in splits:
		lines[i] += ' ' + s
	lines[i]+='\n'

f = open('./model_data/DatasetTrain2.txt','w')
f.writelines(lines)
f.close()
"""
images = []
image_directories = []
box_data = []
box_ids = []
with open('./model_data/DatasetTest.txt', 'r') as f:
	lines = f.readlines()
	for line in lines:
		split = line.split(' ')
		directory = split.pop(0)
		boxes = []
		ids = []
		for box in split:
			sep = box.split(',')
			if(sep[0] == '\n'):
				continue
			x1 = int(sep[0])
			y1 = int(sep[1])
			x2 = int(sep[2])
			y2 = int(sep[3])
			id = int(sep[4])-1
			boxes.append([x1,y1,x2,y2])
			ids.append(id)

		image_directories.append(directory)
		box_data.append(boxes)
		box_ids.append(ids)

for i in range(len(image_directories)):
	with open('./model_data/DatasetTest2.txt','a+') as fd:
		fd.write("%s " % (image_directories[i]))
	for j,class_id in enumerate(box_ids[i]):
		bb = box_data[i][j]
		with open('./model_data/DatasetTest2.txt','a') as fd:
			fd.write("%i,%i,%i,%i,%i " % (bb[0], bb[1], bb[2], bb[3], class_id))

	with open('./model_data/DatasetTest2.txt', 'a+') as fd:
		fd.write("\n")

"""
f = open('DatasetTrain.txt', 'r')
lines = f.readlines()


for i in range(len(lines)):
	lines[i] = '/content/Realtime_Animal_Tracking' + lines[i][1:]

f = open('DatasetTrain2.txt','w')
f.writelines(lines)
f.close()
"""