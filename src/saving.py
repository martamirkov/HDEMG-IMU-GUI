# saving.py

import numpy as np
import pandas as pd

def save_emg_txt(data_list, filenames):
    for data, filename in zip(data_list, filenames):
        np.savetxt(filename, data.T, delimiter='\t')  # transpose to channels as columns

def save_imu_txt(df, filename):
    df.to_csv(filename, sep='\t', index=False)
