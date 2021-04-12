import numpy as np

import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

import random
from PIL import Image
from PIL import ImageEnhance
import os
os.chdir('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/')

images = []
image_directories = []
box_data = []
box_ids = []
a=0
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
      boxes.append(ia.BoundingBox(x1=x1,y1=y1,x2=x2,y2=y2))
      ids.append(id)
    
    im = Image.open(directory, 'r')
    to_arr = np.asarray(im)
    images.append(to_arr )
    image_directories.append(directory)
    box_data.append(boxes)
    box_ids.append(ids)#

    break

seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips
    iaa.Crop(percent=(0, 0.1)), # random crops
    # Small gaussian blur with random sigma between 0 and 0.5.
    # But we only blur about 50% of all images.
    iaa.Sometimes(
        0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    # Strengthen or weaken the contrast in each image.
    iaa.LinearContrast((0.75, 1.5)),
    # Add gaussian noise.
    # For 50% of all images, we sample the noise once per pixel.
    # For the other 50% of all images, we sample the noise per pixel AND
    # channel. This can change the color (not only brightness) of the
    # pixels.
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
    # Make some images brighter and some darker.
    # In 20% of all cases, we sample the multiplier once per channel,
    # which can end up changing the color of the images.
    iaa.Multiply((0.8, 1.2), per_channel=0.2),
    # Apply affine transformations to each image.
    # Scale/zoom them, translate/move them, rotate them and shear them.
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
        rotate=(-25, 25),
        shear=(-8, 8)
    )
], random_order=True) # apply augmenters in random order

images_aug, bbs_aug = seq(image=images[0], bounding_boxes=box_data[0])
bbs_aug[0] = bbs_aug[0].clip_out_of_image(images_aug[0])

new_im = Image.fromarray(np.uint8(images_aug))
new_im.save('D:/Git_Repos/Realtime_Animal_Tracking/Realtime_Animal_Tracking/' +"TESTT"+'.png', 'png')