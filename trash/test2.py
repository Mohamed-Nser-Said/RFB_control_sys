import os
import shutil
import sys
from enum import Enum
import tables as tb
import numpy as np
import h5py


class Particle(tb.IsDescription):
    time_stamp = tb.StringCol(itemsize=22, dflt=" ", pos=0)
    pump_1_speed = tb.StringCol(itemsize=22, dflt=" ", pos=0)  # character String
    pump_1_speed = tb.Int16Col(dflt=1, pos=1)  # short integer
    voltage = tb.Float32Col(dflt=1, pos=2)  # single-precision


class DataBase:
    def __init__(self):
        self.data_dir = "hdf_database_file"
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        os.mkdir(self.data_dir)
        self.root_hdf5 = os.path.join(self.data_dir, "RootDatabase.h5")

    def __enter__(self):
        self.file = tb.open_file(self.root_hdf5, mode="w")
        return self.file

    def open_file(self):
        pass

    def create_group(self, name):
        self.file.create_group(self.file, name)

    def create_new_table(self, group):
        path = os.path.join(self.file.root, group)
        self.file.create_table(path)

    def create_data_set(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


with DataBase() as d:
    print(d.root)



