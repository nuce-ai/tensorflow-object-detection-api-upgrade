import os 
import argparse
import random
import string
from PIL import Image

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif','pdf'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def rescale_images(directory, size):
    for img in os.listdir(directory):
        try:
            im = Image.open(directory+"/"+img)
            im_resized = im.resize(size, Image.ANTIALIAS)
            im_resized.save(directory+"/"+img)
        except:
            os.remove(directory+"/"+img)
def rename_object(directory,name):
    for img in os.listdir(directory):
        if img and allowed_file(img):
            filename = img.replace(img.rsplit('.',1)[0],name + "_" + randomString(8))
            filename = filename.replace(filename.rsplit('.',1)[1],'jpg')
            os.rename(directory + "/" + img,directory + "/" + filename)
        else:
            os.remove(directory + "/" + img)

def run(path):

    for i in os.listdir(path):
        try:
            rename_object(path +"/"+i,i)
            rescale_images(path +"/"+i,(800,600))
            
        except:
            print(i)
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rename images")
    parser.add_argument('-dsource', '--directory_source', type=str, required=True, help='Directory containing the images and label')
    
    args = parser.parse_args()
    run(args.directory_source)