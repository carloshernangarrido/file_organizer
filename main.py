import os
import shutil
import zipfile
import const
from date_extraction import get_year_month_day


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


def organize_all(file_list, dest):
    noncopied_files = []
    number_copied_files = 0
    for file in file_list:
        ismedia, year, month, day = get_year_month_day(file)
        if ismedia:
            if not os.path.exists(dest):
                os.mkdir(dest)
            if not os.path.exists(os.path.join(dest, year)):
                os.mkdir(os.path.join(dest, year))
            if not os.path.exists(os.path.join(dest, year, month)):
                os.mkdir(os.path.join(dest, year, month))
            if not os.path.exists(os.path.join(dest, year, month, os.path.basename(file))):
                print('copying', file, 'to', os.path.join(dest, year, month), 'because does not exists')
                shutil.copy(file, os.path.join(dest, year, month))
                number_copied_files += 1
            else:
                if os.stat(os.path.join(dest, year, month, os.path.basename(file))).st_size < os.stat(file).st_size:
                    print('copying', file, 'to', os.path.join(dest, year, month), 'because existing is smaller')
                    shutil.copy(file, os.path.join(dest, year, month))
                    number_copied_files += 1
                else:
                    print('skiping', file, 'because existing is larger')
        else:
            if os.path.splitext(file)[1] == '.zip':
                print('skiping', file)
            else:
                print('copying', file, 'to', const.NONCOPIED_PATH)
                noncopied_files.append(file)
                if not os.path.exists(const.NONCOPIED_PATH):
                    os.mkdir(const.NONCOPIED_PATH)
                shutil.copy(file, const.NONCOPIED_PATH)
    return noncopied_files, number_copied_files


if __name__ == '__main__':
    files = [os.path.join(path, name) for path, subdirs, files in os.walk(const.SOURCE_PATH) for name in files]
    unzip_all(files)
    noncopied, n_copied = organize_all(files, const.DESTINY_PATH)
    print(f'*** {n_copied} copied files of {len(files)} ***')

