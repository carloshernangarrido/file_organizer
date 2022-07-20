import os
import shutil
import datetime as dt
import zipfile

import PIL
from PIL import Image

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

import const


def creation_date(filename):
    parser = createParser(filename)
    metadata = extractMetadata(parser)
    return metadata.get('creation_date')


def mkdir_ifnotexists(path):
    """Create a directory and fail silently if exists"""
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def create_structure(path, year_first, year_last):
    mkdir_ifnotexists(path)
    years = [str(y) for y in list(range(year_first, year_last + 1))]
    for year in years:
        mkdir_ifnotexists(os.path.join(path, year))
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            mkdir_ifnotexists(os.path.join(path, year, str(month)))
    return years


def unzip_all(file_list):
    for file in file_list:
        if zipfile.is_zipfile(file):
            print('unziping ', file, '...')
            dirname = os.path.splitext(file)[0]
            if not os.path.exists(dirname):
                os.mkdir(dirname)
                with zipfile.ZipFile(file, "r") as z:
                    z.extractall(dirname)
                print('File', file, 'correctly extracted')
            else:
                print('File', file, 'was already extracted')


def get_year_month_day(file):
    if os.path.splitext(file)[1] == '.zip' or os.path.splitext(file)[1] == '.json':
        return False, None, None, None
    try:
        time_stamp = PIL.Image.open(file).getexif()[306]
    except PIL.UnidentifiedImageError:
        try:
            time_stamp = creation_date(file)
        except ValueError:
            time_stamp = None
        except AttributeError:
            time_stamp = None
    except KeyError:
        time_stamp = None
    if time_stamp is not None:
        if type(time_stamp) is str:
            return True, time_stamp[0:4], time_stamp[5:7], time_stamp[8:10]
        elif type(time_stamp) is dt.datetime:
            return True, \
                   str(time_stamp.year).zfill(4), str(time_stamp.month).zfill(2), str(time_stamp.day).zfill(2)
    else:
        return False, None, None, None


def organize_all(file_list, dest):
    noncopied_files = []
    number_copied_files = 0
    for file in file_list:
        ismedia, year, month, day = get_year_month_day(file)
        if ismedia:
            print('copying ', file, ' to ', os.path.join(dest, year, month))
            if not os.path.exists(os.path.join(dest, year)):
                os.mkdir(os.path.join(dest, year))
            if not os.path.exists(os.path.join(dest, year, month)):
                os.mkdir(os.path.join(dest, year, month))
            if not os.path.exists(os.path.join(dest, year, month, os.path.basename(file))):
                shutil.copy(file, os.path.join(dest, year, month))
                number_copied_files += 1
        else:
            if os.path.splitext(file)[1] == '.zip':
                print('skiping', file)
            else:
                print('copying ', file, ' to ', const.NONCOPIED_PATH)
                noncopied_files.append(file)
                if not os.path.exists(const.NONCOPIED_PATH):
                    os.mkdir(const.NONCOPIED_PATH)
                shutil.copy(file, const.NONCOPIED_PATH)
    return noncopied_files, number_copied_files


if __name__ == '__main__':
    # years_created = create_structure(path=const.DESTINY_PATH, year_first=const.YEAR_FIRST, year_last=const.YEAR_LAST)
    # print(years_created)
    files = [os.path.join(path, name) for path, subdirs, files in os.walk(const.SOURCE_PATH) for name in files]
    unzip_all(files)
    not_copied, n_copied = organize_all(files, const.DESTINY_PATH)
    print(f'*** {n_copied} copied files of {len(files)}')
    q = 0
