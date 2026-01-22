from ase import Atoms
from ase.io import read
import matplotlib.pyplot as plt
import numpy as np


atoms_list = read("./q4_q6_all_700K-NPT-2ns_rerun.dump", format="lammps-dump-text", index=":")
wl8_cutoff = 0.030
num_slices = 20  # Adjust as needed
ratio_cutoff = 0.7 # cut-off to tag the slab/slice as crystalline one

timestep = 0.0000005 # in ns,  0.0005 ps
steps_per_frame = 400 # check lammps run file 
t_conv_factor = timestep*steps_per_frame # frame to time (ns)


data_points_2 = []

output_file = "./frame-vs-slice-length-wl8.dat"
for frame in range(0, 10001, 50):  # initial, total n_frames, gap, Adjust to the total number of frames
    atoms = atoms_list[frame]
    wl8_values = atoms.arrays['c_wl_all[8]']
    z_coordinates = atoms.positions[:, 2]
    z_min, z_max = z_coordinates.min(), z_coordinates.max()
    slice_thickness = (z_max - z_min) / num_slices

    # Initialize list to store (z_slice, count)
    data_points = []

    for i in range(num_slices):

        slice_start = z_min + i * slice_thickness
        slice_end = slice_start + slice_thickness
        slice_center = slice_start + (slice_thickness/2.0)
        slice_mask = (z_coordinates >= slice_start) & (z_coordinates < slice_end)
        slice_wl8 = wl8_values[slice_mask]
        #print(i, slice_wl8) 
        slice_wl8_cryst = wl8_values[slice_mask][wl8_values[slice_mask] >= wl8_cutoff]
        slice_wl8_amorph = wl8_values[slice_mask][wl8_values[slice_mask] < wl8_cutoff]

        slice_wl8_cryst_count = len(slice_wl8_cryst)
        slice_wl8_amorph_count = len(slice_wl8_amorph)
        ratio = slice_wl8_cryst_count /(slice_wl8_cryst_count + slice_wl8_amorph_count)
       
        # Implement cutoff to tag slices as crystalline 
        #print(frame, slice_center, ratio) if  ratio >= ratio_cutoff else None
        if ratio >= ratio_cutoff:
            
            slice_center_sel, frame_sel =  slice_center, frame
            #print('frame= ', frame_sel,  'length =', slice_center_sel,  'slice index =', i)
            print('Time= ', frame_sel*t_conv_factor,  'length =', slice_center_sel,  'slice index =', i)
            data_points_2.append((frame_sel*t_conv_factor, slice_center_sel, i))

        #print(data_points_2) 

# Save to a text file
np.savetxt(output_file, data_points_2, fmt="%.6f", delimiter=" ")



##### SELECT SLICES (LENGTH) OF FIRST APPEARANCE OF CRYSTALLINE SLAB ########

from collections import defaultdict

# Input file name
filename01 = "./frame-vs-slice-length-wl8.dat"
output_file_2 = "./time-vs-slice-length-wl8-starting-crystalline-slices-only.dat"
# Dictionary to store results
# Keys = unique values from column 3
# Values = list of tuples of (col1, col2)
data_dict = defaultdict(list)

# Read the file
with open(filename01, 'r') as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) < 3:
            continue  # Skip lines that don't have at least 3 columns
        time, length, slice_idx = parts[0], parts[1], parts[2]
        data_dict[slice_idx].append((time, length))

#print(data_dict)

time_points = []
length_points = []
# Print or access the grouped data
for key in data_dict:
    #print(f"Group '{key}':")
    time_list = [item[0] for item in data_dict[key]]
    length_list = [item[1] for item in data_dict[key]]

    print(time_list[0], length_list[0])

    time_points.append(time_list[0])     # select 1st point of appearance
    length_points.append(length_list[0]) # select 1st point of appearance



# Save to file
with open(output_file_2, "w") as f:
    for col1, col2 in zip(time_points, length_points):
        f.write(f"{col1} {col2}\n")
