# EMG + IMU Short Analysis Tool

A graphical user interface (GUI) tool for loading, visualizing, processing, and saving EMG and IMU data

## Features

- Select folder containing EMG (OTB+) and IMU (TXT) files  
- Plot all EMG channels so it matches electrode layout 
- Plot IMU signals by type (Acc, Quat, RPY) with time axis and grid  
- Toggle raw vs. processed EMG (bandpass, notch, lowpass filters)  
- Extract and save time-windowed data for both EMG and IMU  
- Plot individual EMG channel (by track and channel number) in a separate figure  
- Simple, modern PyQt5 interface with custom pastel purple theme

## Installation

1. Install required packages:

```bash
pip install pyqt5 matplotlib numpy pandas

## Running

python main_gui.py

## IMU rename

imu_rename.py -> MT_2025-05-05-001-000_00B44890.txt → 001_foot.txt
imu_map = {
    '00B44890': 'foot',
    '00B44899': 'calf',
    '00B4489A': 'quad',
    '00B448A1': 'hip'
}
