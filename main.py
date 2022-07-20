import os
import zipfile

import PIL
from PIL import Image
import ffmpeg

import const


def mkdir_ifnotexists(path):
    """Create a directory and fail silently if exists"""
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def create_structure(path, year_first, year_last):
    mkdir_ifnotexists(path)
    years = [str(y) for y in list(range(year_first, year_last+1))]
    for year in years:
        mkdir_ifnotexists(os.path.join(path, year))
        for month in range(1, 12+1):
            mkdir_ifnotexists(os.path.join(path, year, str(month)))
    return years


def unzip_all(file_list):
    for file in file_list:
        if zipfile.is_zipfile(file):
            print('unziping ', file, '...')
            dirname = os.path.splitext(file)[0]
            try:
                os.mkdir(dirname)
                with zipfile.ZipFile(file, "r") as z:
                    z.extractall(dirname)
            except FileExistsError:
                print('File', file, 'was already extracted')


def organize_all(file_list):
    for file in file_list:
        try:
            time_stamp = PIL.Image.open(file).getexif()[306]
            print(file, time_stamp)
        except PIL.UnidentifiedImageError:
            print(file, 'is not an image')
            # try:
            p = ffmpeg.probe(file)
            print(p)
            # except



if __name__ == '__main__':
    print(create_structure(path=const.DESTINY_PATH, year_first=const.YEAR_FIRST, year_last=const.YEAR_LAST))
    files = [os.path.join(path, name) for path, subdirs, files in os.walk(const.SOURCE_PATH) for name in files]
    unzip_all(files)
    organize_all(files)
    q = 0
