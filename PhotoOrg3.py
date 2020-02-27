#! python3
# Photo Organizer
# Version 3.0
# By CodedAsian

import configparser
import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def filecount(source):
    count = 0

    for path, sub, files in os.walk(source):
        for f in range(len(files)):
            file = files[f]
            filelocation = '%s\%s' % (path, file)
            count = count + 1
    return count


def knownfiletypes(source):
    jpgcount = 0
    cr2count = 0
    cr3count = 0
    xmpcount = 0
    dngcount = 0
    psdcount = 0
    jpegcount = 0
    movcount = 0
    mp4count = 0
    pngcount = 0
    gifcount = 0
    pycount = 0
    proceed = True

    for path, sub, files in os.walk(source):
        for f in range(len(files)):
            file = files[f]
            filelocations = '%s\%s' % (path, file.upper())
            if filelocations.endswith('.JPG'):
                jpgcount = jpgcount + 1
            elif filelocations.endswith('.CR2'):
                cr2count = cr2count + 1
            elif filelocations.endswith('.CR3'):
                cr3count = cr3count + 1
            elif filelocations.endswith('.XMP'):
                xmpcount = xmpcount + 1
            elif filelocations.endswith('.DNG'):
                dngcount = dngcount + 1
            elif filelocations.endswith('.PSD'):
                psdcount = psdcount + 1
            elif filelocations.endswith('.JPEG'):
                jpegcount = jpegcount + 1
            elif filelocations.endswith('.MOV'):
                movcount = movcount + 1
            elif filelocations.endswith('.MP4'):
                mp4count = mp4count + 1
            elif filelocations.endswith('.PNG'):
                pngcount = pngcount + 1
            elif filelocations.endswith('.GIF'):
                gifcount = gifcount + 1
            elif filelocations.endswith('.PY'):
                pycount = pycount + 1
            else:
                proceed = False
                notknown = filelocations
                # print(filelocations)

    if proceed:
        print('---Image Files---')
        print('| JPG: %s | CR2: %s | CR3: %s | XMP: %s | DNG: %s | PSD: %s | JPEG: %s | PNG: %s| GIF: %s |' %
              (jpgcount, cr2count, cr3count, xmpcount, dngcount, psdcount, jpegcount, pngcount, gifcount))
        print('---Video Files---')
        print('| MOV: %s | MP4: %s |' % (movcount, mp4count))
        print('---Python Files---')
        print('| Python: %s |' % (pycount))
        return True
    if not proceed:
        print('Unknown File Type: %s' % (notknown))
        return False

def canon(source, model, date):
    year = (date[0:10].split(':')[0])
    month = (date[0:10].split(':')[1])
    day = (date[0:10].split(':')[2])

    cr2=cr3=xmp=dng=psd= source

    cr2file = cr2.replace('JPG', 'CR2')
    cr3file = cr3.replace('JPG', 'CR3')
    xmpfile = xmp.replace('JPG', 'XMP')
    dngfile = dng.replace('JPG', 'DNG')
    xmpfile = xmp.replace('JPG', 'PSD')

def main(source):

    model = None
    datetimeorginal = None

    for path, sub, files in os.walk(source):
        for f in range(len(files)):
            file = files[f]
            filelocation = '%s\%s' % (path, file.upper())

            if filelocation.endswith('.JPG'):

                jpgfile = Image.open(filelocation)

                try:
                    exifdata = jpgfile._getexif().items()
                except AttributeError as e:
                        # NoneType Error
                        # print(e)
                        #print(filelocation)
                        c=1010

                for key, value in exifdata:
                    if key in TAGS:
                        # Use To See Exif Data
                        #print('-------')
                        #print('%s[%s] : %s' % (TAGS[key],key, value))
                        if key == 272:
                            model = value
                        if key == 36867:
                            datetimeorginal = value
                        if key == 305:
                            software = value
                jpgfile.close()

                if model == 'Canon EOS 6D Mark II':
                    canon(filelocation, model, datetimeorginal)

                else:
                    # If None try software
                    c=10101



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    inputpath = config['PATHS']['input']
    mediapath = config['PATHS']['media']

    print('Input Path File Count: %s ' % (filecount(inputpath)))

    if knownfiletypes(inputpath):
        main(inputpath)
    print('Media Path File Count: %s ' % (filecount(mediapath)))
