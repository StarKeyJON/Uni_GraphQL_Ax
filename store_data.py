import os, shutil, pandas as pd, sqlalchemy as sq
import databaseconfig as cfg
# import time
from subprocess import check_output


# check to see if .csv files exist in directory
# if csv files exists, try to perform function, else trigger subprocess and sleep for 3 secs
def store_data():
    # If a directory doesn't exist, make a new directory
    is_directory = os.path.isdir('./datasets')
    dataset_dir = 'datasets'
    mkdir = 'mkdir {0}'.format(dataset_dir)
    if is_directory == False:
        try:
            os.system(mkdir)
        except:
            pass

    print('Storing CSV files into SQL database')
    # time.sleep(3)

    # Find CSV files in current working directory, isolate only the CSV files
    csv_files = []
    if len(os.listdir('./datasets')) == 0:
        for file in os.listdir(os.getcwd()):
            if file.endswith('.csv'):
                csv_files.append(file)
                shutil.move(file, dataset_dir)
            else:
                pass
    else:
        for file in os.listdir('./datasets'):
            if file.endswith('.csv'):
                csv_files.append(file)

    # Read csv file into pandas dataframe
    data_path = os.getcwd() + '/' + dataset_dir + '/'
    df = {}
    for file in csv_files:
        try:
            df[file] = pd.read_csv(data_path + file)
        except UnicodeDecodeError:
            df[file] = pd.read_csv(data_path + file, encoding="ISO-8859-1")
        print(file)

        # Clean table names
    
    for k in csv_files:
        dataframe = df[k]
        clean_tbl_name = k.lower().replace(" ", "_").replace("?", "") \
            .replace("-", "_").replace(r"/", "_").replace("\\", "_").replace("@", "") \
            .replace(")", "").replace(r"(", "").replace("$", "")

        # Remove .csv extension from clean_tbl_name
        tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])

        # Clean column names
        dataframe.columns = [x.lower().replace(" ", "_").replace("?", "") \
                                 .replace("-", "_").replace(r"/", "_").replace("\\", "_").replace("@", "") \
                                 .replace(")", "").replace(r"(", "").replace("$", "") for x in dataframe.columns]

        # Loop through lists and remove "", {}, :, symbols and rearrange
        spec_chars = ['"', "'", "(", ")", "{", "}", "name"]
        ops_chars = [" "]
        em_chars = [","]
        for char in spec_chars:
            dataframe['pair'] = dataframe['pair'].str.replace(char, '')
        for char in ops_chars:
            dataframe['pair'] = dataframe['pair'].str.replace(char, '_')
        for char in em_chars:
            dataframe['pair'] = dataframe['pair'].str.replace(char, ' ')

        dataframe['pair'] = dataframe['pair'].str.split().str.join(" ")

        dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='s')


        # Upload cleaned and prepared dataframes to SQL database
        
        # Using sqlalchemy to make the db connection
        # User, pw, and db are being imported from databaseconfig file
        engine = sq.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user=cfg.mysql["user"], pw=cfg.mysql["passwd"], db=cfg.mysql["db"]))
        con = engine.connect()
        frame = tbl_name
        # use if_exists argument to 'append' if you want to append new data to existing data
        dataframe.to_sql(frame,engine, if_exists='append')
        db = format(cfg.mysql["db"])
        print(' ' * 2, '$' * 12, ' ' * 2)
        print("Succesfuly uploaded " + file + " to " + db)                
        print(' ' * 2, '$' * 12, ' ' * 2)
        try:
            os.remove(data_path + '/' + file)
        except:
            pass
        print("SUCCESS: Removed " + (data_path + file))
        con.close()
store_data()
