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
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def match_brightness(image, brightness):
  width, height = bg_image.size
  image_brightness = calculate_brightness(image, 0, 0, width,height)
  brightness_dif = (brightness-image_brightness)+0.3

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
num_of_backgrounds = 20
backgrounds = []
for i in range(num_of_backgrounds):
  im = Image.open( str('D:/cropped_images/content/background ('+str(i+1)+').png') , 'r')
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

images = []
type_class = []

import os

image_dir = 'D:/cropped_images/content/cropped_images/'
for filename in os.listdir(image_dir):
    if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
      im = Image.open( str('D:/cropped_images/content/cropped_images/'+filename) , 'r')
      images.append(im)
      name, _ = ''.join([i for i in filename if not i.isdigit()]).split('.')
      #print(name)
      type_class.append(classes[name])

import random
shuffle = list(zip(images, type_class))
random.shuffle(shuffle)
images, type_class = zip(*shuffle)
#get forest landscape background images

#for image in images: c

count = 5335
#image_data = 'image_data.csv'
for i in range(2):
  for ind, img in enumerate(images):
    #image bounding box = dir(i)
    bg_image=random.choice(backgrounds)
    width, height = bg_image.size
    #Get a copy of the background to paste on
    bg_copy = bg_image.copy()
    margin_size = 40

    #paste the image somewhere in the background
    x = random.randint(margin_size, width-margin_size)
    y = random.randint(margin_size, height-margin_size)

    num = random.randrange(2, 10)*0.1
    img = img.resize((int(img.width*num), int(img.height*num)), Image.ANTIALIAS)
    #Get image dimensions
    im_width, im_height = img.size
    #Get brightness of background region
    bg_region_brightness = calculate_brightness(bg_copy, x, y, x+im_width, y+im_height)
    #Match the images brightness with the background region
    img = match_brightness(img, bg_region_brightness)
    
    #bg_copy = bg_copy.convert('RGBA')
    img = img.convert('RGBA')
    
    new_img = Image.new('RGBA', bg_copy.size, (0, 0, 0, 0))
    new_img.paste(bg_copy, (0,0))
    new_img.paste(img, (x,y), mask=img)

    max_size = 416
    new_width = im_width + 40
    if(new_width > max_size):
      new_width = max_size
    new_height = im_height + 40
    if(new_height > max_size):
      new_height = max_size

    half_width = int(new_width/2)
    half_height = int(new_height/2)

    left = x-half_width
    if(left < 0):
      left = 0
    upper = y-half_height
    if(upper < 0):
      upper = 0
    right = x+im_width + half_width + 40
    if(right > width):
      right = width
    lower = y+im_height + half_height + 40
    if(lower > height):
      lower = height

    new_img = new_img.crop((left, upper, right, lower))
    #bg_copy.paste(img, (x, y, x+im_width, y+im_height), img)
    width, height = new_img.size
    #Save the image
    count+=1
    
    if(count > 5000):
      path_name =  "yolov4test/image"
    else:
      path_name =  "yolov4train/image"
    new_img.save('D:/cropped_images/content/' +path_name+str(count)+'.png', 'png')

    if(count % 50 == 0):
      print(str(count) + ' out of 6000ish')

    id = type_class[ind]

    bb_right = half_width+im_width
    if(bb_right > width):
      bb_right = width-1
    bb_bot = half_height+im_height
    if(bb_bot > height):
      bb_bot = height-1

    bb = [x-left, y-upper, bb_right, bb_bot]
    #centre_x = (bb[0] + (im_width/2))/width
    #centre_y = (bb[1] + (im_height/2))/height
    #bb_width = im_width/width
    #bb_height = im_height/height
    #Save the corresponding bounding box ground truth, image name and class
    if(count > 5000):
      with open('D:/cropped_images/content/yolov4test/DatasetTest.txt','a+') as fd:
        fd.write("%s %i,%i,%i,%i,%i\n" % ('./model_data/'+path_name+str(count)+'.png', bb[0], bb[1], bb[2], bb[3], id))
    else:
      with open('D:/cropped_images/content/yolov4train/DatasetTrain.txt','a+') as fd:
        fd.write("%s %i,%i,%i,%i,%i\n" % ('./model_data/'+path_name+str(count)+'.png', bb[0], bb[1], bb[2], bb[3], id))
