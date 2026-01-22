import numpy as np
import matplotlib.pyplot as plt
from ase.io.lammpsrun import read_lammps_dump
from ase.visualize import view
from ase import Atoms

# Read the LAMMPS dump file
dump_file = "q4_q6_all_700K-NPT-2ns_rerun.dump"
atoms = read_lammps_dump(dump_file, index=0)  # Read the 1st frame
#atoms = read_lammps_dump(dump_file, index=-1)  # Read the last frame

# Check available properties
print("Available atom properties:", atoms.arrays.keys())

# Choose a specific property (e.g., 'c_myproperty') from the dump
property_name = "c_wl_all[8]"  # Replace with your column name
if property_name not in atoms.arrays:
    raise ValueError(f"Property '{property_name}' not found in dump file!")

property_values = atoms.arrays[property_name]

#max_value = property_values.max()
#min_value = property_values.min()
max_value =  0.08 # from combined w8 distribution of pure systems
min_value = -0.06 # from combined w8 distribution of pure systems

# Create a scatter plot with colormap
fig, ax = plt.subplots()

#3D
#ax = fig.add_subplot(111, projection='3d')
#sc = ax.scatter(atoms.positions[:, 0], atoms.positions[:, 1], atoms.positions[:, 2], c=property_values, cmap="viridis", edgecolors='k', s=100, vmin=0, vmax=1)

#2D
#sc = ax.scatter(atoms.positions[:, 1], atoms.positions[:, 2], c=property_values, cmap="viridis", edgecolors='k', s=100, vmin=min_value, vmax=max_value)
sc = ax.scatter(atoms.positions[:, 1], atoms.positions[:, 2], c=property_values, cmap="magma", edgecolors='k', s=100, vmin=min_value, vmax=max_value)
plt.colorbar(sc, label=r"$W_{8}$")
ax.set_xlabel("Y Position (Å)")
ax.set_ylabel("Z Position (Å)")
# Set equal aspect ratio
ax.set_aspect('equal')
ax.set_title(fr"Atomic Distribution Colored by $W_{8}$")
plt.savefig('first-frame-wl8-colormap.png', dpi=500, bbox_inches='tight')
#plt.savefig('last-frame-wl8-colormap.png', dpi=500, bbox_inches='tight')
plt.show()

# View in ASE GUI with colors
#view(atoms, viewer="ngl")  # Use nglview for better visualization

