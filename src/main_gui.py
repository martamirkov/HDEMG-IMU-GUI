# main_gui_pyqt.py

import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget, QFileDialog,
    QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox, QGridLayout
)
from loaders import load_emg_otb, load_imu_txt
from processing import process_emg
from plotting import plot_emg_tracks, plot_imu
from saving import save_emg_txt, save_imu_txt
from PyQt5.QtWidgets import QInputDialog, QComboBox
import matplotlib.pyplot as plt


import qdarkstyle

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class EMGIMUTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('EMG + IMU Tool')

        # Layouts
        main_layout = QVBoxLayout()
        folder_layout = QHBoxLayout()
        file_layout = QHBoxLayout()
        param_layout = QGridLayout()
        check_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Folder selection
        self.folder_label = QLabel('Folder:')
        self.folder_line = QLineEdit()
        self.folder_button = QPushButton('Browse')
        self.folder_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_line)
        folder_layout.addWidget(self.folder_button)

        # File lists
        self.emg_list = QListWidget()
        self.imu_list = QListWidget()
        file_layout.addWidget(self.emg_list)
        file_layout.addWidget(self.imu_list)

        # Params
        self.emg_fs_input = QLineEdit('2048')
        self.imu_fs_input = QLineEdit('30')
        self.start_input = QLineEdit('0')
        self.end_input = QLineEdit('100')
        self.bp_low_input = QLineEdit('20')
        self.bp_high_input = QLineEdit('450')
        self.notch_input = QLineEdit('50')
        self.lpf_input = QLineEdit('15')

        param_layout.addWidget(QLabel('EMG FS:'), 0, 0)
        param_layout.addWidget(self.emg_fs_input, 0, 1)
        param_layout.addWidget(QLabel('IMU FS:'), 0, 2)
        param_layout.addWidget(self.imu_fs_input, 0, 3)
        param_layout.addWidget(QLabel('Start (s):'), 1, 0)
        param_layout.addWidget(self.start_input, 1, 1)
        param_layout.addWidget(QLabel('End (s):'), 1, 2)
        param_layout.addWidget(self.end_input, 1, 3)
        param_layout.addWidget(QLabel('BP Low:'), 2, 0)
        param_layout.addWidget(self.bp_low_input, 2, 1)
        param_layout.addWidget(QLabel('BP High:'), 2, 2)
        param_layout.addWidget(self.bp_high_input, 2, 3)
        param_layout.addWidget(QLabel('Notch:'), 3, 0)
        param_layout.addWidget(self.notch_input, 3, 1)
        param_layout.addWidget(QLabel('LPF:'), 3, 2)
        param_layout.addWidget(self.lpf_input, 3, 3)

        # Checkboxes
        self.raw_checkbox = QCheckBox('Plot Raw EMG')
        self.acc_checkbox = QCheckBox('Acc')
        self.quat_checkbox = QCheckBox('Quat')
        self.rpy_checkbox = QCheckBox('RPY')
        check_layout.addWidget(self.raw_checkbox)
        check_layout.addWidget(self.acc_checkbox)
        check_layout.addWidget(self.quat_checkbox)
        check_layout.addWidget(self.rpy_checkbox)

        # Buttons
        self.plot_emg_btn = QPushButton('Plot EMG')
        self.plot_imu_btn = QPushButton('Plot IMU')
        self.process_save_btn = QPushButton('Process & Save')
        self.plot_single_btn = QPushButton('Plot Single Channel')
        button_layout.addWidget(self.plot_single_btn)
        
        button_layout.addWidget(self.plot_emg_btn)
        button_layout.addWidget(self.plot_imu_btn)
        button_layout.addWidget(self.process_save_btn)

        self.plot_emg_btn.clicked.connect(self.plot_emg)
        self.plot_imu_btn.clicked.connect(self.plot_imu)
        self.process_save_btn.clicked.connect(self.process_and_save)
        self.plot_single_btn.clicked.connect(self.plot_single_channel)
        

        # Add layouts
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(param_layout)
        main_layout.addLayout(check_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
        # Layout widgets
        self.layout_label = QLabel('Layout:')
        self.layout_combo = QComboBox()
        self.layout_combo.addItems(['13x5', '8x8', '4x4'])
        layout_layout = QHBoxLayout()
        layout_layout.addWidget(self.layout_label)
        layout_layout.addWidget(self.layout_combo)

        main_layout.addLayout(layout_layout)


    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folder_line.setText(folder)
            emg_files = [f for f in os.listdir(folder) if f.endswith('.otb+')]
            imu_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
            self.emg_list.clear()
            self.emg_list.addItems(emg_files)
            self.imu_list.clear()
            self.imu_list.addItems(imu_files)

    def plot_emg(self):
        folder = self.folder_line.text()
        selected = self.emg_list.currentItem()
        if not (folder and selected):
            QMessageBox.warning(self, 'Warning', 'Please select folder and EMG file')
            return
        filepath = os.path.join(folder, selected.text())
        tracks_data, freqs = load_emg_otb(filepath)
        fs = float(self.emg_fs_input.text())
        processed_flags = []
        processed_tracks = []
        for data in tracks_data:
            if self.raw_checkbox.isChecked():
                processed_tracks.append(data)
                processed_flags.append(False)
            else:
                proc_data = np.array([process_emg(ch, fs, float(self.bp_low_input.text()), float(self.bp_high_input.text()),
                                                      float(self.notch_input.text()), float(self.lpf_input.text())) for ch in data])
                processed_tracks.append(proc_data)
                processed_flags.append(True)
        
        #plot_emg_tracks(processed_tracks[:2], processed_flags[:2], [f'Track {i+1}' for i in range(min(2, len(tracks_data)))])
        layout_str = self.layout_combo.currentText()
        rows, cols = map(int, layout_str.split('x'))

        plot_emg_tracks(processed_tracks[:2], processed_flags[:2],
                [f'Track {i+1}' for i in range(min(2, len(tracks_data)))],
                rows, cols)



    def plot_imu(self):
        folder = self.folder_line.text()
        selected = self.imu_list.currentItem()
        if not (folder and selected):
            QMessageBox.warning(self, 'Warning', 'Please select folder and IMU file')
            return
        filepath = os.path.join(folder, selected.text())
        df = load_imu_txt(filepath)
        cols = []
        if self.acc_checkbox.isChecked():
            cols += [c for c in df.columns if 'Acc' in c]
        if self.quat_checkbox.isChecked():
            cols += [c for c in df.columns if 'Quat' in c]
        if self.rpy_checkbox.isChecked():
            cols += [c for c in df.columns if 'Roll' in c or 'Pitch' in c or 'Yaw' in c]
        if not cols:
            QMessageBox.warning(self, 'Warning', 'No IMU signals selected!')
            return
        plot_imu(df, cols)

    def process_and_save(self):
        folder = self.folder_line.text()
        selected_emg = self.emg_list.currentItem()
        selected_imu = self.imu_list.currentItem()

        if selected_emg:
            filepath = os.path.join(folder, selected_emg.text())
            tracks_data, freqs = load_emg_otb(filepath)
            fs = float(self.emg_fs_input.text())
            start = int(float(self.start_input.text()) * fs)
            end = int(float(self.end_input.text()) * fs)
            filenames = []
            processed_tracks = []
            for i, data in enumerate(tracks_data):
                proc_data = np.array([process_emg(ch[start:end], fs, float(self.bp_low_input.text()), float(self.bp_high_input.text()),
                                                          float(self.notch_input.text()), float(self.lpf_input.text())) for ch in data])
                processed_tracks.append(proc_data)
                filenames.append(filepath.replace('.otb+', f'_track{i+1}_processed.txt'))
            save_emg_txt(processed_tracks, filenames)
            QMessageBox.information(self, 'Done', 'Saved EMG files!')

        if selected_imu:
            filepath = os.path.join(folder, selected_imu.text())
            df = load_imu_txt(filepath)
            imu_fs = float(self.imu_fs_input.text())
            imu_start = int(float(self.start_input.text()) * imu_fs)
            imu_end = int(float(self.end_input.text()) * imu_fs)
            cropped_df = df.iloc[imu_start:imu_end]
            imu_outfile = filepath.replace('.txt', '_cropped.txt')
            save_imu_txt(cropped_df, imu_outfile)
            QMessageBox.information(self, 'Done', 'Saved IMU file!')
            


    def plot_single_channel(self):
        folder = self.folder_line.text()
        selected = self.emg_list.currentItem()
    
        if not (folder and selected):
            QMessageBox.warning(self, 'Warning', 'Please select folder and EMG file')
            return
    
        # ask user which track: 1 or 2
        track_idx, ok = QInputDialog.getInt(self, 'Select Track', 'Track number (1 or 2):', 1, 1, 2)
        if not ok:
            return
    
        # ask user for channel number
        ch_idx, ok = QInputDialog.getInt(self, 'Select Channel', 'Channel number (1-64):', 1, 1, 64)
        if not ok:
            return
    
        filepath = os.path.join(folder, selected.text())
        tracks_data, freqs = load_emg_otb(filepath)
    
        if track_idx > len(tracks_data):
            QMessageBox.warning(self, 'Warning', f'Track {track_idx} not available.')
            return
    
        data = tracks_data[track_idx - 1]
        fs = float(self.emg_fs_input.text())
    
        if ch_idx > data.shape[0]:
            QMessageBox.warning(self, 'Warning', f'Channel {ch_idx} not available.')
            return
    
        signal = data[ch_idx - 1]
    
        if not self.raw_checkbox.isChecked():
            signal = process_emg(signal, fs, float(self.bp_low_input.text()), float(self.bp_high_input.text()),
                                 float(self.notch_input.text()), float(self.lpf_input.text()))
    
        time = np.arange(len(signal)) / fs
    
        plt.figure(figsize=(12, 4))
        plt.plot(time, signal)
        plt.xlabel('Time (s)')
        plt.ylabel(f'Track {track_idx} - Channel {ch_idx}')
        plt.title(f'{"Processed" if not self.raw_checkbox.isChecked() else "Raw"} Signal')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EMGIMUTool()
    window.show()
    window.setStyleSheet("""
        QWidget {
            background-color: #f6f0f9;  /* soft lavender background */
            color: #3d2b4f;
            font-family: Arial;
            font-size: 11pt;
        }
        QPushButton {
            background-color: #e0c3fc;  /* pastel purple button */
            color: #3d2b4f;
            border: 1px solid #c4a4e5;
            border-radius: 8px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d1b3ff;  /* slightly darker on hover */
        }
        QLineEdit, QListWidget {
            background-color: #fdfaff;  /* almost white with purple tint */
            border: 1px solid #c4a4e5;
            padding: 4px;
        }
        QCheckBox {
            padding: 2px;
        }
        QLabel {
            color: #4b3354;  /* darker purple for labels */
        }
    """)


    sys.exit(app.exec_())
