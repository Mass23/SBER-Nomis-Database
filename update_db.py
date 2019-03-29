#!/usr/bin/python3
import pandas as pd
import glob
import os
import time

################ Functions ################
def add_row(df, row):
    df.loc[-1] = row
    df.index = df.index + 1
    return df.sort_index()

def LogUpdate(log):
    log.write('-----------------------------')
    log.write('Database update:')
    log.write('\n')

    # Print the date and time
    localtime = str(time.asctime( time.localtime(time.time())))
    log.write('  - ')
    log.write(localtime)
    log.write('\n')

    # Print the username
    log.write('  - Username:')
    log.write(str(os.getlogin()))
    log.write('\n')
    log.write('-----------------------------')
    log.write('\n')

def GetAvailableGlaciers(file):
    with open(file) as f:
        glaciers_list = []

        for glacier in f.readlines():
            glaciers_list.append(glacier.rstrip('\n'))

        return(glaciers_list)

################ Main #####################
def main():
    with open('database.log', 'w') as log:
        # 0. Write some basic information on the log file, create the table
        LogUpdate(log)

        glaciers_list = GetAvailableGlaciers('glacier_list.tsv')

        data_table = pd.DataFrame(columns = ['glacier', 'location', 'patch'])

        for glacier in glaciers_list:
            add_row(data_table, [glacier,'UP',1])
            add_row(data_table, [glacier,'UP',2])
            add_row(data_table, [glacier,'UP',3])
            add_row(data_table, [glacier,'DN',1])
            add_row(data_table, [glacier,'DN',2])
            add_row(data_table, [glacier,'DN',3])

        log.write('  - ')
        log.write(str(len(glaciers_list)))
        log.write(' glaciers')
        log.write('\n\n')

        # 1. List all files and subdirectories
        list_sub = glob.glob('*')

        dirs = [i for i in list_sub if os.path.isdir(i) == True]
        files = [i for i in list_sub if os.path.isfile(i) == True]

        samples_metrics = ['BA', 'BP', 'Chl-a', 'DNA', 'DOC', 'DOM', 'EEA', 'EGM', 'EPS', 'Ions', 'mDOM', 'minerals', 'Nutrients', 'Resp']

if __name__== "__main__":
    main()
