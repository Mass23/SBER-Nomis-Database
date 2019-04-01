#!/usr/bin/python3
import pandas as pd
import os
import glob
import time
import statistics.stdev as stdev

################ Logfile functions ################
def LogUpdate(log):
    log.write('-----------------------------')
    log.write('\n')
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

################ Check IDs functions ################
def StrInt(string):
    try:
        int(string)
        return(True)
    except ValueError:
        return(False)

def CheckGlacierID(glacier_id):
    if glacier_id.startswith('GL') and StrInt(glacier_id.replace('GL','')) and not glacier_id.replace('GL','').startswith('0'):
        return(True)
    else:
        return(False)

def CheckLocation(location):
    if location in ['UP','DN']:
        return(True)
    else:
        return(False)

def CheckPatchID(patch_id):
    if patch_id in [1,2,3]:
        return(True)
    else:
        return(False)

################ Table management functions ################
def AddRow(table, row):
    table.loc[-1] = row
    table.index = table.index + 1
    return table.sort_index()

#def AppendData(table, data_to_append):

################ Data query functions ################
def GetAvailableGlaciers(file):
    with open(file) as f:
        glaciers_data = pd.read_csv(f, delimiter = '\t', header = 0, names = ['glacier', 'location', 'patch'])
        print(glaciers_data)
        glaciers_list = []

        for index, row in enumerate(glaciers_data.itertuples()):
            print(row)
            glaciers_list.append(row.glacier)

        return(sorted(list(set(glaciers_list))))

def LoadTSV(file):
    with open(file, 'r') as f:
        data = pd.read_csv(f, sep = '\t', header = 1)

################ Main #####################
def main():
    with open('database.log', 'w') as log:

        # 0. Write some basic information on the log file
        LogUpdate(log)

        # 1. Check that directories are present for all the metrics
        directories = [i for i in glob.glob(*) if os.isdir(i)]
        files = [i for i in glob.glob(*) if os.isfile(i)]

        field_parameters = 'field_data.tsv'
        if field_parameters not in files:
            log.write('Field parameters file not found! exiting...')
            return(-1)

        lab_parameters = ['BA','Chl-a','DOC','EEA','EPS','BP','DOM','EGM','mDOM','Resp']
        for i in lab_parameters:
            if i not in directories:
                log.write('Following parameter directory not found: ' + i)

        dna_parameters = ['DNA']

        # 2. Create the dataframe
        glaciers_list = GetAvailableGlaciers(field_parameters)
        data_table = pd.DataFrame(columns = ['glacier', 'location', 'patch'])

        for glacier in glaciers_list:
            AddRow(data_table, [glacier,'UP',1])
            AddRow(data_table, [glacier,'UP',2])
            AddRow(data_table, [glacier,'UP',3])
            AddRow(data_table, [glacier,'DN',1])
            AddRow(data_table, [glacier,'DN',2])
            AddRow(data_table, [glacier,'DN',3])

        log.write(str(len(glaciers_list)))
        log.write('glaciers:')
        for i in glaciers_list:
            log.write(' - ' + i)
        log.write('\n\n')

        # 3. Add columns with values

if __name__== "__main__":
    main()
