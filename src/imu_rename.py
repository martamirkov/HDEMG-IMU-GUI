import os
from tkinter import filedialog, Tk

# IMU code → body location mapping
imu_map = {
    '00B44890': 'foot',
    '00B44899': 'calf',
    '00B4489A': 'quad',
    '00B448A1': 'hip'
}

# Open folder picker
root = Tk()
root.withdraw()
folder = filedialog.askdirectory(title='Select IMU folder')

if not folder:
    print("No folder selected. Exiting.")
    exit()

# Loop through txt files
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        # Extract IMU code
        imu_code = filename[-12:-4]
        
        if imu_code in imu_map:
            # Extract trial number → between first '-' and second '-'
            parts = filename.split('-')
            trial_number = parts[3]  # e.g., '001'

            new_name = f"{trial_number}_{imu_map[imu_code]}.txt"
            src = os.path.join(folder, filename)
            dst = os.path.join(folder, new_name)
            os.rename(src, dst)
            print(f"Renamed: {filename} → {new_name}")
        else:
            print(f"Skipped (unknown code): {filename}")

print("Renaming complete!")
