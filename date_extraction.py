import os
import datetime as dt

import PIL
from PIL import Image

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.stream.input import NullStreamError


def creation_date(filename):
    parser = createParser(filename)
    metadata = extractMetadata(parser)
    return metadata.get('creation_date')


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
        except NullStreamError:
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
