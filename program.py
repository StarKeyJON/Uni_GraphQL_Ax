# python3
import os
import os.path
import time


def get_credentials():
    print('''
        Hello, please enter your MySQL database configurations 
                and a file will be automatically generated to use. 
                    *********************
            Keep in mind, 
                these credentials will not be encrypted.
                    *********************
        Please, make sure to enter your database name exactly as is in the database.
    ''')
    host = input('Enter host name:')
    user = input('Enter user name:')
    pswd = input('Enter password:')
    db = input('Enter database name:')
    with open('./databaseconfig.py', 'w') as file:
        file.write('mysql = {')
        file.write('\n\t"host": ' + '"' + host + '",')
        file.write('\n\t"user": ' + '"' + user + '",')
        file.write('\n\t"passwd": ' + '"' + pswd + '",')
        file.write('\n\t"db": ' + '"' + db + '",')
        file.write('\n}')
    print('')
    print("Thank you!\nPreparing the data collection program for initiation.\nEnjoy!")
    time.sleep(1)
    import time_check
    time_check.check_time()


# Check if a databaseconfig file exists and run program if so, if not get_credentials
def initiate_program():
    file_name = "databaseconfig.py"
    cur_dir = os.getcwd()

    while True:
        file_list = os.listdir(cur_dir)

        if file_name in file_list:
            import time_check
            time_check.check_time()
        else:
            get_credentials()


initiate_program()
