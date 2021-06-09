import os, shutil, pandas as pd, sqlalchemy as sq
import databaseconfig as cfg
import time
from subprocess import check_output

#check to see if .csv files exist in directory
def store_data():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.csv'):
            try:
            #if csv files exists, try to perform function, else trigger subprocess and sleep for 3 secs

                #Find CSV files in current working directory, isolate only the CSV files
                csv_files = []
                for file in os.listdir(os.getcwd()):
                    if file.endswith('.csv'):
                        csv_files.append(file)

                #Make a new directory
                dataset_dir = 'datasets'
                try:
                    mkdir = 'mkdir {0}'.format(dataset_dir)
                    os.system(mkdir)
                except:
                    pass

                #Move CSV files in the new directory   
                for csv in csv_files:
                    shutil.move(csv, dataset_dir)

                #Read csv file into pandas dataframe
                data_path = os.getcwd()+'/'+dataset_dir+'/'
                df = {}
                for file in csv_files:
                    try:
                        df[file] = pd.read_csv(data_path+file)
                    except UnicodeDecodeError:
                        df[file] = pd.read_csv(data_path+file, encoding="ISO-8859-1")

                #Clean table names
                for k in csv_files:
                    dataframe = df[k]
                    clean_tbl_name = k.lower().replace(" ","_").replace("?","") \
                                     .replace("-","_").replace(r"/","_").replace("\\","_").replace("@","") \
                                     .replace(")","").replace(r"(","").replace("$","")

                #Remove .csv extension from clean_tbl_name
                    tbl_name = '{0}'.format(clean_tbl_name.split('.')[0])

                #Clean column names
                    dataframe.columns = [x.lower().replace(" ","_").replace("?","") \
                                     .replace("-","_").replace(r"/","_").replace("\\","_").replace("@","") \
                                     .replace(")","").replace(r"(","").replace("$","") for x in dataframe.columns]

                #Loop through lists and remove "", {}, :, symbols and rearrange
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

                    #Upload cleaned and prepared dataframes to SQL database
                    for file in csv_files:
                            try:
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
                                filecount = format(filecount)
                                db = format(cfg.mysql["db"])
                                del csv_files
                                print("SUCCESS: files imported to the " + db + " database and current state cleared.")
                            except Exception:
                                print("Error: Check that your SQL database is running.")  

                    #Delete the succefully uploaded files
                    for new_file in csv_files:
                        try:
                            os.remove(data_path+new_file)
                        except Exception:
                            print('Error: deletion failed')

            except:
                check_output(['node', './getData.js'])

                time.sleep(2)

                store_data()  
store_data()
