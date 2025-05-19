# processing.py

from scipy.signal import butter, filtfilt, iirnotch

def bandpass_filter(signal, fs, lowcut, highcut, order=4):
    b, a = butter(order, [lowcut/(fs/2), highcut/(fs/2)], btype='band')
    return filtfilt(b, a, signal)

def notch_filter(signal, fs, notch_freq, quality=30):
    b, a = iirnotch(notch_freq, quality, fs)
    return filtfilt(b, a, signal)

def lowpass_filter(signal, fs, cutoff, order=4):
    b, a = butter(order, cutoff / (fs/2), btype='low')
    return filtfilt(b, a, signal)

def process_emg(signal, fs, lowcut, highcut, notch_freq, lp_cutoff):
    filtered = bandpass_filter(signal, fs, lowcut, highcut)
    filtered = notch_filter(filtered, fs, notch_freq)
    rectified = abs(filtered)
    envelope = lowpass_filter(rectified, fs, lp_cutoff)
    return envelope
