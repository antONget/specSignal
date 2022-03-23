from pathlib import Path
import numpy as np
import datetime as dt
import re
import os


def read_iq_16bit(file_path: Path,
                  num_samples: int = -1,
                  num_first_samples_to_skip: int = 0,
                  inversion: bool = True) -> np.array:
    """
    Read IQ samples of rf-signal (coded in 16 bit)
    @type file_path: path of fr-signal file
    @type num_samples: count of samples, which is necessary to read (read all by default)
    @type num_first_samples_to_skip: count of samples, which is necessary to skip
                                     from the start of the file (no skip by default)
    @type inversion: IQ inversion, if inversion = 0 - no inversion (True by default)
    @return signal: np.array of iq-samples
    """
    if not file_path.exists():
        raise FileNotFoundError(f'file "{file_path}" is not a exist')
    sample_type = np.dtype([("i", np.int16), ("q", np.int16)])
    offset = sample_type.itemsize * num_first_samples_to_skip
    min_file_size = sample_type.itemsize * (num_samples + num_first_samples_to_skip)
    if file_path.stat().st_size < min_file_size:
        raise ProcessLookupError(f'file size ={file_path.stat().st_size} bytes is'
                                 f' too small for load {num_samples} samples. It '
                                 f'is necessary at least {min_file_size} bytes')
    iq_samples = np.fromfile(file_path, dtype=sample_type,
                             count=num_samples, offset=offset)
    complex_iq_samples = np.zeros(shape=(len(iq_samples)), dtype=np.complex64)
    if inversion:
        complex_iq_samples[:] = iq_samples[:]["i"] + iq_samples[:]["q"] * 1j
    else:
        complex_iq_samples[:] = iq_samples[:]["q"] + iq_samples[:]["i"] * 1j
    return complex_iq_samples


def write_iq_16bit(file_path: Path,
                   complex_iq_samples: np.array = [],
                   inversion: bool = False):

    sample_type = np.dtype([("i", np.int16), ("q", np.int16)])
    iq_samples = np.zeros(shape=(len(complex_iq_samples)), dtype=sample_type)

    if inversion:
        iq_samples[:]["i"] = np.real(complex_iq_samples[:])
        iq_samples[:]["q"] = np.imag(complex_iq_samples[:])
    else:
        iq_samples[:]["q"] = np.real(complex_iq_samples[:])
        iq_samples[:]["i"] = np.imag(complex_iq_samples[:])

    iq_samples.tofile(file_path)


def num_samples_iq_16bit(file_path):
    sample_type = np.dtype([("i", np.int16), ("q", np.int16)])
    return int(os.path.getsize(file_path)/sample_type.itemsize)


def get_factor(factor_char: str) -> float:
    if factor_char == 'G':
        factor = 1e9
    elif factor_char == 'M':
        factor = 1e6
    elif factor_char == 'K':
        factor = 1e3
    else:
        factor = 1.0
    return factor


def calc_frequency(freq_str: str) -> float:
    last_ind = len(freq_str) - 1
    freq_factor = freq_str[last_ind]
    factor = get_factor(freq_factor)
    if factor == 1.0:
        last_ind += 1
    freq_str_cut = freq_str[:last_ind]
    freq = float(freq_str_cut)
    frequency = freq * factor
    return frequency


def get_central_frequency_from_name(filename: str) -> float:
    match = re.search(r'\d*\.?\d*\SHz', filename)
    if not match:
        raise ValueError(f'Could not infer central frequency'
                         f' from signal file name = "{filename}"')
    result = match.group()
    freq_str = result[:len(result) - 2]
    return calc_frequency(freq_str)


def get_sampling_frequency_from_name(filename: str) -> float:
    match = re.search(r'\d*\.?\d*\SSps', filename)
    if not match:
        raise ValueError(f'Could not infer sampling frequency'
                         f' from signal file name = "{filename}"')
    result = match.group()
    freq_str = result[:len(result) - 3]
    return calc_frequency(freq_str)


def get_sig_duration_from_name(filename: str) -> float:
    match = re.search(r'duration=\d*\.?\d*ms', filename)
    if not match:
        raise ValueError(f'Could not signal duration'
                         f' from signal file name = "{filename}"')
    result = match.group()
    val_str = result[9:len(result) - 2]
    return float(val_str) / 1000.0


def get_feature_type_from_name(filename: str, features_types_list):
    for feature_type in features_types_list:
        if re.search(r''+feature_type, filename):
            return feature_type
    return None


date_time_masks = \
    {
        r'\d{2}.\d{2}.\d{2}_\d{2}-\d{2}-\d{2}': '%d.%m.%y_%H-%M-%S',
        r'\d{2}.\d{2}.\d{4}_\d{2}-\d{2}-\d{2}': '%d.%m.%Y_%H-%M-%S',
        r'\d{2}.\d{2}.\d{4} \d{2}_\d{2}_\d{2}': '%d.%m.%Y %H_%M_%S',
        r'\d{2}.\d{2}.\d{4} \d{2}-\d{2-\d{2}': '%d.%m.%Y %H-%M-%S',
    }


def get_datetime_from_name(filename: str) -> dt.datetime:
    global date_time_masks
    for reg_exp, mask in date_time_masks.items():
        match = re.search(reg_exp, filename)
        if match:
            mask = date_time_masks[reg_exp]
            date_time_str = match.group()
            date_time = dt.datetime.strptime(date_time_str, mask)
            return date_time
    raise ValueError(f'Could not infer datetime from'
                     f' signal file name = "{filename}"')
