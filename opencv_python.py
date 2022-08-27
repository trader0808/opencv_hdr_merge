from __future__ import print_function
from __future__ import division
from lib2to3.pgen2.token import tok_name
import cv2 as cv
import argparse
import os
import numpy as np

def loadExopsureSeq(path):
    images = []
    times = []
    with open(os.path.join(path, 'list.txt')) as f:
        content = f.readlines()
    for line in content:
        tokens = line.split()
        images.append(cv.imread(os.path.join(path,tokens[0])))
        times.append(1/float(tokens[1]))
    
    return images, np.asarray(times, dtype=np.float32)

parser = argparse.ArgumentParser(description='Code for High dynamic range Imaging Tutorial')
parser.add_argument('--input', type=str, help='Path to the directory that contains images to load and exposure times')
args = parser.parse_args()

if not args.input:
    parser.print_help()
    exit(0)

images, times = loadExopsureSeq(args.input)

calibrate = cv.createCalibrateDebevec()
response = calibrate.process(images, times)

merge_debevec = cv.createMergeDebevec()
hdr = merge_debevec.process(images, times, response)

tonemap = cv.createTonemap(2.2)
ldr = tonemap.process(hdr)

merge_mertens = cv.createMergeMertens()
fusion = merge_mertens.process(images)

cv.imwrite('fusion.png', fusion*255)
cv.imwrite('ldr.png', ldr * 255)
cv.imwrite('hdr.hdr', hdr)