# from engine.ipp_spectrogram_lib.pybind11_lib_ipp_spectrogram import *
# import numpy as np
# from typing import Tuple
#
#
# class IppSpectrogramCalculator:
#     def __init__(self):
#         self._calculator = SpectrogramCalculator()
#
#     def generate_random_image(self, img_shape: Tuple[int, int]):
#         img = self._calculator.GenerateRandomImage(img_shape)
#         rgb_img = self.convert_img_to_rgb(img)
#         return rgb_img
#
#     def calculate_spectrogram(self, iq_samples: np.ndarray,
#                               sampling_frequency: float, img_shape: Tuple[int, int]):
#         fig = self._calculator.CalculateSpectrogram(iq_samples, sampling_frequency, img_shape)
#         rgb_fig = self.convert_img_to_rgb(fig)
#         return rgb_fig
#
#     @staticmethod
#     def convert_img_to_rgb(img):
#         img = np.array(img)
#         rgb_img = np.zeros(shape=img.shape + (3,), dtype=np.uint8)
#         rgb_img[:, :, 0] = img & 255
#         rgb_img[:, :, 1] = (img >> 8) & 255
#         rgb_img[:, :, 2] = (img >> 16) & 255
#         return rgb_img


import numpy as np
from typing import Tuple


class IppSpectrogramCalculator:
    def __init__(self):
        self.color_map_ = dict()
        self.color_map_[0] = "#352a86"
        self.color_map_[1] = "#353093"
        self.color_map_[2] = "#36369f"
        self.color_map_[3] = "#353cac"
        self.color_map_[4] = "#2b4ac6"
        self.color_map_[5] = "#1f52d3"
        self.color_map_[6] = "#0f5bdd"
        self.color_map_[7] = "#0262e0"
        self.color_map_[8] = "#046ce0"
        self.color_map_[9] = "#0870de"
        self.color_map_[10] = "#0c74dc"
        self.color_map_[11] = "#1078da"
        self.color_map_[12] = "#1380d5"
        self.color_map_[13] = "#1484d3"
        self.color_map_[14] = "#1389d2"
        self.color_map_[15] = "#108ed2"
        self.color_map_[16] = "#0898d1"
        self.color_map_[17] = "#069ccf"
        self.color_map_[18] = "#06a0cc"
        self.color_map_[19] = "#05a3c9"
        self.color_map_[20] = "#06a9c1"
        self.color_map_[21] = "#09abbd"
        self.color_map_[22] = "#0faeb8"
        self.color_map_[23] = "#15b0b4"
        self.color_map_[24] = "#25b4a9"
        self.color_map_[25] = "#2db7a3"
        self.color_map_[26] = "#37b89d"
        self.color_map_[27] = "#41ba97"
        self.color_map_[28] = "#58bd8b"
        self.color_map_[29] = "#64be85"
        self.color_map_[30] = "#70be80"
        self.color_map_[31] = "#7cbf7b"
        self.color_map_[32] = "#91be72"
        self.color_map_[33] = "#9bbe6e"
        self.color_map_[34] = "#a5be6a"
        self.color_map_[35] = "#aebd67"
        self.color_map_[36] = "#bfbc60"
        self.color_map_[37] = "#c8bb5c"
        self.color_map_[38] = "#d0ba59"
        self.color_map_[39] = "#d8ba55"
        self.color_map_[40] = "#e9b94e"
        self.color_map_[41] = "#f0b949"
        self.color_map_[42] = "#f8ba43"
        self.color_map_[43] = "#fdbe3d"
        self.color_map_[44] = "#fdc832"
        self.color_map_[45] = "#fbcd2d"
        self.color_map_[46] = "#f9d229"
        self.color_map_[47] = "#f7d825"
        self.color_map_[48] = "#f4e41c"
        self.color_map_[49] = "#f4eb18"
        self.color_map_[50] = "#f6f213"
        self.color_map_[51] = "#fcf807"
        self.color_map_[52] = "#fffb00"

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def calculate_spectrogram(self, iq_samples: np.ndarray,
                              sampling_frequency: float, img_shape: Tuple[int, int]):

        img = np.zeros(img_shape)
        for j in range(img_shape[1]):
            len2 = int(len(iq_samples) / img_shape[1])
            skip2 = int(j * len(iq_samples) / img_shape[1])

            AA2 = iq_samples[skip2:skip2 + len2]

            AA2fft = np.fft.fftshift(np.fft.fft(AA2))
            # AA2fft = np.abs(AA2fft)
            AA2fft = np.log10(AA2fft)
            AA2fft = np.abs(AA2fft)

            AA3 = np.zeros(img_shape[0])
            for k in range(img_shape[0]):
                AA3[k] = AA2fft[int(k * (len2 - 1) / img_shape[0])]

            img[:, j] = AA3

        mx = np.max(img)
        img = img / mx * 52

        img3 = np.zeros((img_shape[0], img_shape[1], 3))

        for x in range(img_shape[0]):
            for y in range(img_shape[1]):
                v = self.hex_to_rgb(self.color_map_[int(img[x, y])])
                img3[x, y, 2] = v[0]
                img3[x, y, 1] = v[1]
                img3[x, y, 0] = v[2]

        return img3

    @staticmethod
    def convert_img_to_rgb(img):
        img = np.array(img)
        rgb_img = np.zeros(shape=img.shape + (3,), dtype=np.uint8)
        rgb_img[:, :, 0] = img & 255
        rgb_img[:, :, 1] = (img >> 8) & 255
        rgb_img[:, :, 2] = (img >> 16) & 255
        return rgb_img

