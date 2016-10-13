import png
import sys
import os
import math
import struct
import argparse

writearr = []
maxwidth = 4000
maxheight = 3000
bytesperpixel = 3
maxsize = maxwidth * maxheight * bytesperpixel

parser = argparse.ArgumentParser(description='Pack any files into a PNG or series of PNGs')
parser.add_argument('-i', help="the input file", required=True)
parser.add_argument('-o', help="the output file", required=True)
args = vars(parser.parse_args())

inputfile = args.get('i')
outputfile = args.get('o')

filesize = os.path.getsize(inputfile)
numfiles = math.ceil(filesize/float(maxsize))
bytesread = 0

numpixels = int(math.ceil(filesize/3.0))

#TODO WRITE ALL FILES AT ONCE?????
for i in range(int(numfiles)):
    writearr = []
    width = 4000
    height = 3000
    # TODO need to recalculate pixels and just general variables.
    # reading bytes wayyyyyy faster now. Could read entire file probably instead
    newwidth = math.ceil(4 * math.sqrt(numpixels/12))
    newheight = math.ceil(3 * math.sqrt(numpixels/12))
    if newwidth < width:
        width = newwidth
    if newheight < height:
        height = newheight
    extrabytes = bytesperpixel * int((width * height) - numpixels)
    if extrabytes <= 0:
        extrabytes = 0
    with open(inputfile, 'rb') as readBytes:
        readBytes.seek(bytesread)
        for k in range(int(height)):
            # read in a row's worth of bytes
            byte_data = [ord(test) for test in list(readBytes.read(int(width * bytesperpixel)))]
            bytesread += int(width * bytesperpixel)
            # give some kind of user feedback
            print bytesread, filesize
            # if there was nothing more to read in the file we want to break to add
            # 0's to the row so we can write out the PNG
            if len(byte_data) < (width * bytesperpixel):
                break
            writearr.append(byte_data)

    print int((width * bytesperpixel) - len(byte_data))
    if int((width * bytesperpixel) - len(byte_data)) != 0:
        for j in range(int((width * bytesperpixel) - len(byte_data))):
            byte_data.append(0)
        writearr.append(byte_data)
    #print writearr

    testfile = open(outputfile + "_%d.png" % i, 'wb')
    w = png.Writer(width, height)
    w.write(testfile, writearr)
    testfile.close()
    numpixels -= maxsize/3.0
