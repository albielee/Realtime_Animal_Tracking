f = open('DatasetTest.txt', 'r')
lines = f.readlines()


for i in range(len(lines)):
	lines[i] = '/content/'+lines[i][14:]

f = open('DatasetTest.txt','w')
f.writelines(lines)
f.close()

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