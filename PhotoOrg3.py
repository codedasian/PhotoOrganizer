#! python3
# Photo Organizer
# Version 3.0
# By CodedAsian

import configparser
import os
import shutil
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
    mp3count = 0
    vfcount = 0
    sfkcount = 0
    bakcount = 0
    wavcount = 0
    avicount = 0
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
            elif filelocations.endswith('.MP3'):
                mp3count = mp3count + 1
            elif filelocations.endswith('.VF'):
                vfcount = vfcount + 1
            elif filelocations.endswith('.SFK'):
                sfkcount = sfkcount + 1
            elif filelocations.endswith('.BAK'):
                bakcount = bakcount + 1
            elif filelocations.endswith('.WAV'):
                wavcount = wavcount + 1
            elif filelocations.endswith('.AVI'):
                avicount = avicount + 1
            else:
                proceed = False
                notknown = filelocations
                # print(filelocations)

    if proceed:
        print('---Image Files---')
        print('| JPG: %s | CR2: %s | CR3: %s | XMP: %s | DNG: %s | PSD: %s | JPEG: %s | PNG: %s| GIF: %s |' %
              (jpgcount, cr2count, cr3count, xmpcount, dngcount, psdcount, jpegcount, pngcount, gifcount))
        print('---Video Files---')
        print('| MOV: %s | MP4: %s | AVI: %s |' % (movcount, mp4count, avicount))
        print('---Random---')
        print('| Python: %s | MP3: %s | VF: %s | SFK: %s | BAK: %s | WAV: %s |' % (pycount, mp3count, vfcount, sfkcount,
                                                                                   bakcount, wavcount))

        totaltransfer = filecount(source) - (pycount + mp3count + vfcount + sfkcount + bakcount + wavcount)
        print('Files Being Transfered: %s' % totaltransfer)
        return True
    if not proceed:
        print('Unknown File Type: %s' % (notknown))
        return False


def canonfiletatus(source):
    status = os.path.exists(source)
    # print(status)
    return status


def canon(source, model, date):
    year = (date[0:10].split(':')[0])
    month = (date[0:10].split(':')[1])
    day = (date[0:10].split(':')[2])

    cr2 = cr3 = xmp = dng = psd = source

    cr2file = cr2.replace('JPG', 'CR2')
    cr3file = cr3.replace('JPG', 'CR3')
    xmpfile = xmp.replace('JPG', 'XMP')
    dngfile = dng.replace('JPG', 'DNG')
    psdfile = psd.replace('JPG', 'PSD')

    filebuffer = [source]

    cr2switch = False

    if canonfiletatus(cr2file):
        filebuffer.append(cr2file)
    if canonfiletatus(cr3file):
        filebuffer.append(cr3file)
    if canonfiletatus(xmpfile):
        filebuffer.append(xmpfile)
    if canonfiletatus(dngfile):
        filebuffer.append(dngfile)
    if canonfiletatus(psdfile):
        filebuffer.append(psdfile)

    for i in range(len(filebuffer)):
        os.makedirs(config['PATHS']['Media'], exist_ok=True)
        filesfound = filebuffer[i]
        filename = (filesfound.split('\\')[(len(filesfound.split('\\')) - 1)])

        destination = '%s\%s\%s\%s\%s\%s' % (config['PATHS']['media'], model, year, day, month, filename)

        if filename.endswith('JPG'):
            destination = '%s\%s\%s\%s\%s\%s\%s' % (config['PATHS']['media'], model, year, day, month, 'JPG', filename)

        elif filename.endswith('CR2'):
            destination = '%s\%s\%s\%s\%s\%s\%s' % (config['PATHS']['media'], model, year, day, month, 'CR2', filename)
            cr2switch = True

        elif cr2switch == True:
            if filename.endswith('XMP'):
                destination = '%s\%s\%s\%s\%s\%s\%s' % (config['PATHS']['media'], model, year, day, month, 'CR2',
                                                        filename)

        else:
            print('Unknown Canon File Type: ' % (filesfound))


        # source
        # print(filesfound)
        # destination
        # print(destination)



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
                    # print(filelocation)
                    c = 1010

                for key, value in exifdata:
                    if key in TAGS:
                        # Use To See Exif Data
                        # print('-------')
                        # print('%s[%s] : %s' % (TAGS[key],key, value))
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
                    c = 10101


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    inputpath = config['PATHS']['input']
    mediapath = config['PATHS']['media']

    print('Input Path File Count: %s ' % (filecount(inputpath)))

    if knownfiletypes(inputpath):
        main(inputpath)
    print('Media Path File Count: %s ' % (filecount(mediapath)))
