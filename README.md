# Uni_GraphQL_Ax

I was approached on Telegram by an anonymous individual to build them a program that queries for live swap events and then saves them to a database. They requested it to be without any api keys, so I decided to use TheGraph.
This was my first attempt at building such a program, and I would probably just write it all in python next time.

I built the codebase and managed a remote Linux server for them to store the data.

Live swaps scraper that creates csv files and uploads into sql database.

You will need to have the latest version of node.js and python installed, also it is using My SQL database.

Create a new folder on your desktop and transfer all the files into the new folders.

Database configuration settings will be prompted if none are found and a new config file will be created.

Open up the command line and change directory to the newly created project folder that contains the files.

Run the python script to initiate the automated program, by typing "python3 program.py".

This will initiate the program. The majority of the operations are done by time_check.py as it creates new directories and queries the current time stamps in batches of (50), and then compares the first, middle and last for changes. If time changes are noticed, then the full swap data is queried, prepared and stored in the SQL database.

After a few runs, batches of (50) seemed like an adequate comparison, as the csv reports are only in batches of (100), and after monitoring of the database, the uploaded swaps are queried at up to current datetime.

If you need to quit the program, press ctrl+c.
If there are errors upon running it again after an abrupt halt, 
delete the "/newtimesets" and "/oldtimesets" directories and contents, and try to restart the program.
