# plotting.py

import matplotlib.pyplot as plt
import numpy as np

def plot_emg_tracks(tracks_data, processed_flags, track_names, nrows=5, ncols=13):

    for i, data in enumerate(tracks_data):
        n_channels = data.shape[0]
        fig, axs = plt.subplots(nrows, ncols, figsize=(20, 8))
        fig.suptitle(f"{track_names[i]} {'(Processed)' if processed_flags[i] else '(Raw)'}")

        for ch in range(n_channels):
            row = ch // ncols
            col = ch % ncols
            axs[row][col].plot(data[ch])
            axs[row][col].set_title(f"Ch {ch+1}", fontsize=8)
            axs[row][col].set_xticks([])
            axs[row][col].set_yticks([])

        # Turn off unused subplots if fewer than 65
        for ch in range(n_channels, nrows * ncols):
            row = ch // ncols
            col = ch % ncols
            axs[row][col].axis('off')

        plt.tight_layout()
        plt.show()



def plot_imu(df, columns, fs=200):
    time = np.arange(len(df)) / fs
    fig, axs = plt.subplots(len(columns), 1, figsize=(12, len(columns) * 2), sharex=True)

    if len(columns) == 1:
        axs = [axs]  # ensure list if single subplot

    # define color palette
    color_list = plt.cm.tab10.colors  # or any matplotlib colormap
    # extend color list if more signals
    while len(color_list) < len(columns):
        color_list += color_list

    for i, (ax, col) in enumerate(zip(axs, columns)):
        ax.plot(time, df[col], color=color_list[i], label=col)
        ax.set_ylabel(col)
        ax.grid(True)
        ax.legend(loc='upper right', fontsize=8)

    axs[-1].set_xlabel('Time (s)')
    plt.tight_layout()
    plt.show()