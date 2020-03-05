# cognitive-episode

The files on this repo are scripts made for my TFG in an attempt to simplify calculations.

- **aminas_alejandro** contains a python script which can read .xyz files corresponding to cyclic enamines, find the coordinates of the enamine nitrogen and its sorrounding three C atoms and then find the plane between the 3 atoms and its distance to the N atom.

- **diedros_alejandro** reads .xyz files and calculates the dihedral angle between 4 given atoms.

- **energy_collector** reads gaussian16 .log result files and collects energy values, orders them in a table and creates a .svg grid with the molecules used for calculations. WIP.

- **obminimize** is a small testing script which uses open babel empirical energy minimization methods in an attempt to find the lowest energy conformer of a molecule, although it is not always useful because the empirical methods cannot consider some long range interactions present in our set of molecules.
