import os
import png
import sys
from PIL import Image
import struct
import argparse
import glob

pixels = []

parser = argparse.ArgumentParser(description='Unpack a png into the original file')
parser.add_argument('-i', help="the input file", required=True)
parser.add_argument('-o', help="the output file", required=True)
args = vars(parser.parse_args())

inputfile = args.get('i')
outputfile = args.get('o')

numfiles = glob.glob(inputfile + '_*.png')

#print "There are %d files being processed" % numfiles

for i in range(42):
    print "_%d.png" % i
    with open(inputfile + "_%d.png" % i,'rb') as inputpixels:
        reader = png.Reader(file=inputpixels)
        png_read = reader.read()
        pixels.append(list(png_read[2]))

print 'Starting to write final output file'
with open(outputfile,'wb') as output:
    for i in pixels:
        for j in i:
            for k in j:
                output.write(struct.pack('B',k))
