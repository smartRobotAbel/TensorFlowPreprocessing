import glob
from PIL import Image
import  xml.etree.ElementTree as ET
import os

def updateCoordinate(actualSize,newSize,actualCoordinate):
    return round(actualCoordinate/actualSize * newSize)


def updateAnnotation(xmlfilename,newFilename,newH, newW):
    print(xmlfilename)
    print(newFilename)
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    filename = root.find('filename')
    filename.text = newFilename

    #get width and height
    height = root.find('size').find('height')
    width = root.find('size').find('width')

    # updateLabels xmin ymin xmax ymax
    objects = root.findall('object')
    print(objects)
    for bndBox in objects:
        bndBox = bndBox.find('bndbox')
        xmin = bndBox.find('xmin')
        xmax = bndBox.find('xmax')
        ymin = bndBox.find('ymin')
        ymax = bndBox.find('ymax')
        xmin.text = str(updateCoordinate(int(width.text), newW, int(xmin.text)))
        xmax.text = str(updateCoordinate(int(width.text), newW, int(xmax.text)))
        ymin.text = str(updateCoordinate(int(height.text), newH, int(ymin.text)))
        ymax.text = str(updateCoordinate(int(height.text), newH, int(ymax.text)))

    # update height and weight

    height.text = str(newH)
    width.text = str(newW)
    tree.write('./dataset/annotations/xmls/'+newFilename)

def changeformat(filename,format,index):
    return filename.split('.')[index]+'.'+format

def resize():
    class_name = 'robot_ball'
    #os.mkdir('resized')
    file_list = sorted(glob.glob('./input/*.jpg'))
    for idx,file_name in enumerate(file_list):
      im = Image.open(file_name)
      print(file_name)
      new_width  = 640
      new_height = 480
      im = im.resize((new_width, new_height))
      newFilename = class_name + '_' + str(idx+1).zfill(3) + '.jpg'
      im.save('./dataset/images/'+newFilename)
      updateAnnotation('.'+changeformat(file_name,'xml',1),changeformat(newFilename,'xml',0),new_height,new_width)

resize()
