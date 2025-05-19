# loaders.py

import numpy as np
import pandas as pd
from OTBiolabInterface import OpeningOtbPlusFile


def load_emg_otb(filepath):
    tracks = OpeningOtbPlusFile(filepath)
    data_list = []
    frequencies = []
    for i, track in enumerate(tracks):
        ch_data = np.array([ch.data for ch in track.sections[0].channels])
        data_list.append(ch_data)
        frequencies.append(track.frequency)
    return data_list, frequencies

def load_imu_txt(filepath):
    df = pd.read_csv(filepath, sep='\t', comment='/', skip_blank_lines=True)
    df = df.dropna(axis=1, how='all')  # drop empty columns
    return df
