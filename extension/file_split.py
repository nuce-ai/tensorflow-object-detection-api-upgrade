import os 
import shutil 
import re 
import argparse
from collections import Counter 
temp = []
def clean_file(dsource):
    for r,d,f in os.walk(dsource):
        for file in f:
            temp.append(file.rsplit('.',1)[0])
    for i in Counter(temp):
        try:
            if(Counter(temp)[i] != 2):
                os.remove(dsource + "/" + i.rsplit('_',1)[0] + "/" + i + ".jpg")         
        except:
            if(Counter(temp)[i] != 2):
                os.remove(dsource + "/" + i.rsplit('_',1)[0] + "/" + i + ".xml")

def run(dsource,dtrain,dtest,ntest):
    source = []
    for r,d,f in os.walk(dsource):
        for file in f:
            source.append(dsource +"/" +file)
    
    # print(round((ntest*len(source))/100)*2)
    print(len(source))
    for i in source[0:round((ntest*len(source)/2)/100)*2]:
        head,tail = (os.path.split(i))
        shutil.copyfile(i,dtest + "/" + tail)

    for i in source[round((ntest*len(source)/2)/100)*2:]:
        head,tail = (os.path.split(i))
        shutil.copyfile(i,dtrain + "/" + tail)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rename images")
    parser.add_argument('-dsource', '--directory_source', type=str, required=True, help='Directory containing the images and label')
    parser.add_argument('-dtrain', '--directory_train', type=str, required=True, help='Directory containing train')
    parser.add_argument('-dtest', '--directory_test', type=str, required=True, help='Directory containing test')
    parser.add_argument('-ntest', '--number_test', type=int, required=True, help='number image of test')
    
    args = parser.parse_args()
    clean_file(args.directory_source)
    for i in os.listdir(args.directory_source):
        run(args.directory_source + "/" + i,args.directory_train,args.directory_test,args.number_test)
