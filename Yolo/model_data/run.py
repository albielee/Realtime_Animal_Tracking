images = []
image_directories = []
box_data = []
box_ids = []
with open('DatasetTrain', 'r') as f:
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
      x1 = float(sep[0])
      y1 = float(sep[1])
      x2 = float(sep[2])
      y2 = float(sep[3])
      id = int(sep[4])-1
      boxes.append([x1,y1,x2,y2])
      ids.append(id)

    image_directories.append(directory)
    box_data.append(boxes)
    box_ids.append(ids)

for i in range(len(image_directories)):
	print(image_directories[i])
	with open('DatasetTrain2','a+') as fd:
		fd.write("%s " % (image_directories[i]))
	for j,class_id in enumerate(box_ids[i]):
		bb = box_data[i][j]
		with open('DatasetTrain2','a') as fd:
			fd.write("%i,%i,%i,%i,%i " % (bb[0], bb[1], bb[2], bb[3], class_id))

	with open('DatasetTrain2', 'a+') as fd:
		fd.write("\n")

"""
f = open('DatasetTest.txt', 'r')
lines = f.readlines()


for i in range(len(lines)):
	lines[i] = lines[i][:50]+lines[i][51:]

f = open('DatasetTest2.txt','w')
f.writelines(lines)
f.close()
"""
"""
f = open('Test.txt', 'r')
lines = f.readlines()


classes = {
	"Head": 0,
	"Arm": 1,
	"Body": 2,
	"Chimp": 3,
	"BearHead": 4,
	"BearLeg": 5,
	"BearBody": 6,
	"Bear": 7
}
old_num = 1000
f = open('NewTest.txt','w')
for i in range(len(lines)):
	new_line = True
	class_id, x1,y1,x2,y2,name,_,__ = lines[i].split(',')
	class_id = classes[class_id]
	im_num = int(name[13]+name[14])
	print(im_num)	
	if(old_num != im_num):
		f.write('\n./model_data/'+name)
		old_num = im_num
	f.write(" "+x1+","+y1+","+x2+","+y2+","+str(class_id))
		
f.close()

"""