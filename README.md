# Uni_GraphQL_Ax
Live swaps scraper that creates csv files and uploads into sql database.

You will need to have the latest version of node.js and python installed, also it is using My SQL database.

Create a new folder on your desktop and transfer all the files into the new folders.

Database configuration settings will be prompted if none are found and a new config file will be created.

Open up the command line and change directory to the newly created project folder that contains the files.

Run the python script to initiate the automated program, by typing "python3 program.py".

This will initiate the program. The majority of the operations are done by time_check.py as it creates new directories and queries the current time stamps in batches of (50), and then compares the first, middle and last for changes. If time changes are noticed, then the full swap data is queried, prepared and stored in the SQL database.

After a few runs, batches of (50) seemed like an adequate comparison, as the csv reports are only in batches of (100), and after monitoring of the database, the uploaded swaps overlap seem to be reduced to a minimal.

If you need to quit the program, press ctrl+c.
If there are errors upon running it again after an abrupt halt, 
delete the "/newtimesets" and "/oldtimesets" directories and contents, and try to restart the program.
