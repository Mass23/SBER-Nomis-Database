import pandas as pd
import glob
import os

list_sub = glob.glob(*)

dirs = [i for i in list_sub if os.path.isdir(i) == True]
files = [i for i in list_sub if os.path.isfile(i) == True]
