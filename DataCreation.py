import glob
import random
from PIL import Image
from PIL import ImageEnhance
import sys

def calculate_brightness(image, x1, y1, x2, y2):
    greyscale_image = image.convert('L')
    cropped_image = greyscale_image.crop((x1,y1,x2,y2))
    histogram = cropped_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / (pixels+1)
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def match_brightness(image, brightness):
  width, height = bg_image.size
  image_brightness = calculate_brightness(image, 0, 0, width,height)
  brightness_dif = (brightness-image_brightness)+0.45

  rgb_im = image.convert('RGBA')
  #Modify the brightness of each pixel in the image
  im_width, im_height = image.size
  for y in range(0, im_height):
    for x in range(0, im_width):
      r, g, b, a = rgb_im.getpixel((x, y))
      r = r*brightness_dif
      if(r > 255.0):
        r=255.0
      if(r < 0.0):
        r=0
      g = g*brightness_dif
      if(g > 255.0):
        g=255.0
      if(g < 0.0):
        g=0
      b = b*brightness_dif
      if(b > 255.0):
        b=255.0
      if(b < 0.0):
        b=0
      rgb_im.putpixel((x, y), (int(r), int(g), int(b), int(a)))

  return rgb_im

#Get background images
num_of_backgrounds = 19
backgrounds = []
for i in range(num_of_backgrounds):
  im = Image.open( str('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/Backgrounds/background ('+str(i+1)+').png') , 'r')
  backgrounds.append(im)
 
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

#images = []
#type_class = []

import os
os.chdir('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/')

images = []
image_directories = []
box_data = []
box_ids = []
with open('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/image_data.csv', 'r') as f:
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
      id = int(sep[4])
      boxes.append([x1,y1,x2,y2])
      ids.append(id)
    
    im = Image.open(directory, 'r')
    images.append(im)
    image_directories.append(directory)
    box_data.append(boxes)
    box_ids.append(ids)


#image_dir = 'D:/cropped_images/content/cropped_images/'
#for filename in os.listdir(image_dir):
#    if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
#      im = Image.open( str('D:/cropped_images/content/cropped_images/'+filename) , 'r')
#      images.append(im)
 #     name, _ = ''.join([i for i in filename if not i.isdigit()]).split('.')
 #     #print(name)
 #     type_class.append(classes[name])

import random
shuffle = list(zip(images, image_directories, box_data, box_ids))
random.shuffle(shuffle)
images, image_directories, box_data, box_ids = zip(*shuffle)
#get forest landscape background images
test_image_num = 500

scales = [0.3, 0.5, 1]#,500,700]
count = 0
print(len(images))
#image_data = 'image_data.csv'
for ind, img in enumerate(images):
  for scale in scales:
    #image bounding box = dir(i)
    bg_image=random.choice(backgrounds)
    width, height = bg_image.size
    #Get a copy of the background to paste on
    bg_copy = bg_image.copy()

    #scale += 100/img.width
    new_im = img.copy()

    #Scale the image
    #new_im = new_im.resize((int(scale), int(scale)), Image.ANTIALIAS)
    #Dont forget to scale the bounding boxes :
    #also get the bounding box size of all boxes
    max_x = 0
    min_x = 3000
    max_y = 0
    min_y = 3000
    new_bboxs = []
    for bbox in box_data[ind]:
      box = []
      for i in range(len(bbox)):
        #if x value
        if(i == 0 or i == 2):
          new_len = bbox[i]#*x_scale
          if(max_x < new_len):
            max_x = new_len
          if(min_x > new_len):
            min_x = new_len

        #if y value
        if(i == 1 or i == 3):
          new_len = bbox[i]#*y_scale
          if(max_y < new_len):
            max_y = new_len
          if(min_y > new_len):
            min_y = new_len

        box.append(new_len)

      new_bboxs.append(box)

    c_left = 120
    if(min_x-c_left < 0):
      c_left = min_x
    c_top = 120
    if(min_y-c_top < 0):
      c_top = min_y
    c_right = max_x+120
    if(c_right > new_im.width):
      c_right = new_im.width
    c_bottom = max_y+120
    if(c_bottom > new_im.height):
      c_bottom = new_im.height
    new_im = new_im.crop((min_x-c_left, min_y-c_top, c_right, c_bottom))
    for bbox in new_bboxs:
      for i in range(len(bbox)):
        if(i == 0 or i == 2):
          bbox[i] -= (min_x-c_left)
        if(i == 1 or i == 3):
          bbox[i] -= (min_y-c_top)

    new_im = new_im.resize((int(new_im.width*scale), int(new_im.height*scale)), Image.ANTIALIAS)
    for bbox in new_bboxs:
      for i in range(len(bbox)):
        bbox[i] = int(bbox[i]*scale)


    #Get image dimensions
    im_width = (max_x - min_x)
    im_height = (max_y - min_y)

    #get random paste coordinates
    #if(new_im.width < bg_copy.width):
    #  x = random.randint(-bg_copy.width+new_im.width+1, 0)
    #else:
    #  x = 0
    #if(new_im.height < bg_copy.height):
    #  y = random.randint(-bg_copy.height+new_im.height+1, 0)
    #else:
    #  y = 0
    if(new_im.width == 0 or bg_copy.width == 0 or new_im.height == 0 or bg_copy.height == 0):
      continue

    if(new_im.width > bg_copy.width):
      x=random.randint(1,bg_copy.width)
      pw = bg_copy.width-1
    else:
      x=random.randint(1,new_im.width)
      pw = new_im.width-1

    if(new_im.height > bg_copy.height):
      y=random.randint(1,bg_copy.height)
      ph = bg_copy.height-1
    else:
      y=random.randint(1,new_im.height)
      ph = new_im.height-1

    print("x",x)
    print("y",y)

    #Get brightness of background region
    bg_region_brightness = calculate_brightness(bg_copy, x+bg_copy.width-new_im.width, y+bg_copy.height-new_im.height, x+bg_copy.width+new_im.width, y+bg_copy.height+new_im.height)
    #Match the images brightness with the background region
    new_im = match_brightness(new_im, bg_region_brightness)

    #bg_copy = bg_copy.convert('RGBA')
    new_im = new_im.convert('RGBA')

    #bg_copy = bg_copy.crop((x, y, x+im_width, y+im_height))
    
    new_img = Image.new('RGBA', new_im.size, (0, 0, 0, 0))

    new_img.paste(bg_copy, (x-pw,y-ph))
    new_img.paste(new_im, (0,0), mask=new_im)

    #for bbox in new_bboxs:
    #  for i in range(len(bbox)):
     #   if(i == 0 or i == 2):
     #     bbox[i] += x
     #   if(i == 1 or i == 3):
     #     bbox[i] += y

    #bg_scale = 416/new_img.width
    #width_dif = new_img.width-new_img.width*bg_scale
    #height_dif = new_img.height-new_img.height*bg_scale
    #new_img = new_img.resize((int(new_img.width*bg_scale), int(new_img.height*bg_scale)), Image.ANTIALIAS)

    
    #for bbox in new_bboxs:
    #  for i in range(len(bbox)):
    #    if(i == 0 or i == 2):
    #      bbox[i] -= width_dif
    #      bbox[i]=bbox[i]*bg_scale
     #     if(bbox[i] > new_img.width):
    #        bbox[i] = new_img.width
     #   if(i == 1 or i == 3):
    #      bbox[i] -= height_dif
    #      bbox[i]=bbox[i]*bg_scale
    #      if(bbox[i] > new_img.height):
    #        bbox[i] = new_img.height
    #    if(bbox[i]<0):
    #        bbox[i] = 0


    ########
    
    """
    margin = 50
    if(min_x-margin > 0):
      c_left = min_x-margin
    else:
      c_left = 0
    
    if(max_x+margin < width):
      c_right = max_x+margin
    else:
      c_right = width

    if(min_y-margin > 0):
      c_top = min_y-margin
    else:
      c_top = 0
    
    if(max_y+margin < height):
      c_bottom = max_y+margin
    else:
      c_bottom = height

    #print((min_x, min_y, max_x, max_y))
    for bbox in new_bboxs:
      for i in range(len(bbox)):
        if(i == 0 or i == 2):
          bbox[i] = bbox[i]-c_left
        else:
          bbox[i] = bbox[i]-c_top

    new_img = new_img.crop((c_left, c_top, c_right, c_bottom))
    """
    #Save the image
    

    if(ind > len(images)-500):
      path_name =  "yolov4test/image"
    else:
      path_name =  "yolov4train/image"

    new_img.save('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/' +path_name+str(count)+'.png', 'png')

    if(count % 50 == 0):
      print(str(count) + ' out of 6000ish')

    class_ids = box_ids[ind]
    #centre_x = (bb[0] + (im_width/2))/width
    #centre_y = (bb[1] + (im_height/2))/height
    #bb_width = im_width/width
    #bb_height = im_height/height
    #Save the corresponding bounding box ground truth, image name and class
    if(ind > len(images)-500):
      save_dir = './yolov4test/DatasetTest.txt'
    else:
      save_dir = './yolov4train/DatasetTrain.txt'

    with open(save_dir,'a+') as fd:
      fd.write("%s " % ('./model_data/'+str(count)+'.png'))
    for j,class_id in enumerate(class_ids):
      bb = new_bboxs[j]
      with open(save_dir,'a') as fd:
        fd.write("%i,%i,%i,%i,%i " % (bb[0], bb[1], bb[2], bb[3], class_id))

    with open(save_dir, 'a+') as fd:
      fd.write("\n")

    count+=1