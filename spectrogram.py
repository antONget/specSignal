from support.load_signals import *
from support.ipp_spectrogram_calculator import *
from pathlib import Path
import cv2
import os
import math

# папка к читаемым сигналам
###src_rf_signals_folder = 'E:/NoveltyDetection/NoveltyDetection/signalTest/background400'
src_rf_signals_folder = 'E:/NoveltyDetection/NoveltyDetection/signalTest/background'
# частота дискретизации
Fs = 100e6
# длительность куска
duration = 0.050
# размер картинки
img_size = 512

# ================================================================================
# получаем список файлов
files = os.listdir(src_rf_signals_folder)

calculator = IppSpectrogramCalculator()

dst_folder = src_rf_signals_folder + "/" + 'Spectrogramm'

if not (Path(dst_folder).exists()):
    Path(dst_folder).mkdir()

for n in range(len(files)):
    # имя файла
    src_rf_signal = src_rf_signals_folder + "/" + files[n]
    #
    folder_name = str(Path(files[n]).with_suffix(''))

    print(src_rf_signal)

    # dst_folder = src_rf_signals_folder + "/_" + folder_name
    #
    # if not (Path(dst_folder).exists()):
    #     Path(dst_folder).mkdir()

    skip = 0
    slice_len = int(duration * Fs)
    siz = int(Path(src_rf_signal).stat().st_size / 4)
    img_shape = (img_size, img_size)
    print('Choosed rf signal samples: %d' % siz)
    i = 0
    while skip < siz:

        len000 = slice_len
        if skip + slice_len > siz:
            len000 = siz - skip

        AA = read_iq_16bit(Path(src_rf_signal),
                           num_samples=len000,
                           num_first_samples_to_skip=skip,
                           inversion=False)

        cols_count = img_shape[1]
        flag = 1
        if len000 < slice_len:
            flag = 0
            cols_count = math.floor(img_shape[1] * len000 / slice_len)

        img3 = calculator.calculate_spectrogram(AA, Fs, [img_shape[0], cols_count])

        index = '%d' % i
        while len(index) < 4:
            index = '0' + index

        img_file_name = dst_folder + '/'+ str(n) + '_' + index + '.png'
        if flag:
            cv2.imwrite(img_file_name, img3)

        print(i)

        skip = skip + slice_len
        i = i + 1

    # description_str = ""
    #
    # description_str = description_str + 'filename ' + folder_name + '\n'
    # description_str = description_str + 'Fs %d\n' % Fs
    # description_str = description_str + 'duration %d\n' % int(duration * 1000)
    # description_str = description_str + 'img_shape %d\n' % int(img_size)
    # description_str = description_str + 'last_img_cols_count %d\n' % cols_count
    #
    # f = open(dst_folder + '/img_parameters.txt', 'w')
    # f.write(description_str)
    # f.close()
