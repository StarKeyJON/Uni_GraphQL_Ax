import os, csv, shutil, sqlite3, pyodbc, numpy as np, pandas as pd, sqlalchemy as sq
import databaseconfig as cfg
from pandas.io import pytables

#find CSV files in current working directory, isolate only the CSV files
csv_files = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        csv_files.append(file)

#make a new directory
dataset_dir = 'datasets'
try:
    mkdir = 'mkdir {0}'.format(dataset_dir)
    os.system(mkdir)
except:
    pass

#move CSV files in the new directory
for csv in csv_files:
    shutil.move(csv, dataset_dir)

#read csv file into pandas dataframe
data_path = os.getcwd()+'/'+dataset_dir+'/'
df = {}
for file in csv_files:
    try:
        df[file] = pd.read_csv(data_path+file)
    except UnicodeDecodeError:
        df[file] = pd.read_csv(data_path+file, encoding="ISO-8859-1")
    print(file)

#clean table names
for k in csv_files:
    dataframe = df[k]

    clean_tbl_name = k.lower().replace(" ","_").replace("?","") \
                     .replace("-","_").replace(r"/","_").replace("\\","_").replace("@","") \
                     .replace(")","").replace(r"(","").replace("$","")

#remove .csv extension from clean_tbl_name
    tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])

#clean column names
    dataframe.columns = [x.lower().replace(" ","_").replace("?","") \
                     .replace("-","_").replace(r"/","_").replace("\\","_").replace("@","") \
                     .replace(")","").replace(r"(","").replace("$","") for x in dataframe.columns]

    print(dataframe)

# Loop through lists and remove "", {}, :, symbols and rearrange
    spec_chars = ['"',"'","(",")","{","}","name"]
    ops_chars = [" "]
    em_chars = [","]
    for char in spec_chars:
        dataframe['pair'] = dataframe['pair'].str.replace(char, '')
    for char in ops_chars:
        dataframe['pair'] = dataframe['pair'].str.replace(char, '_')
    for char in em_chars:
        dataframe['pair'] = dataframe['pair'].str.replace(char, ' ')        

    dataframe['pair'] = dataframe['pair'].str.split().str.join(" ") 

    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit ='s')
    print(dataframe['pair'])



#save df to csv

#open csv file, save it as an object

    # Using sqlalchemy to make the db connection
    # User, pw, and db are being imported from databaseconfig file to mask credentials
    con = sq.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                            .format(user=cfg.mysql["user"],pw=cfg.mysql["passwd"],db=cfg.mysql["db"]))

    frame = tbl_name
    # Insert the dataframe into the MySQL database table 'acct_activity'
    # use if_exists argument to 'replace' if you want to drop the table and replace
    # use if_exists argument to 'append' if you want to append new data to existing data
    dataframe.to_sql(frame, con, if_exists='append')
    filecount = len(csv_files)
    rowcount = format(len(dataframe.index))
    filecount = format(filecount)
    db = format(cfg.mysql["db"])

    print("SUCCESS: " + rowcount + " rows of data from " + filecount + " files imported to the " + db + " database.")

