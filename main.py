import os
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


if __name__ == '__main__':
    print(create_structure(path=const.DESTINY_PATH, year_first=const.YEAR_FIRST, year_last=const.YEAR_LAST))
    a = [os.path.join(path, name) for path, subdirs, files in os.walk(const.SOURCE_PATH) for name in files]
    q = 0

    # for ruta, directorios, archivos in os.walk(const.SOURCE_PATH, topdown=True):
    #     print(ruta, directorios, archivos)
        # print('\nruta       :', ruta)
        # for elemento in archivos:
        #     num_archivos += 1
        #     archivo = ruta + os.sep + elemento
        #     estado = os.stat(archivo)
        #     tamaño = estado.st_size
        #     ult_acceso = datetime.fromtimestamp(estado.st_atime)
        #     modificado = datetime.fromtimestamp(estado.st_mtime)
        #     ult_acceso = ult_acceso.strftime(formato)
        #     modificado = modificado.strftime(formato)
        #     total += tamaño
        #     print(linea)
        #     print('archivo      :', elemento)
        #     print('modificado   :', modificado)
        #     print('último acceso:', ult_acceso)
        #     print('tamaño (Kb)  :', round(tamaño / 1024, 1))
