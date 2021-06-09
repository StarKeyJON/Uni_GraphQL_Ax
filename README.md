# Uni_GraphQL_Ax
Live swaps scraper that creates csv files and uploads into sql database.

This is currently a hard coded configuration,
you will need to have the latest version of node.js and python installed, also it is using My SQL database.

Create a new folder on your desktop and transfer all the files into the new folders.

Open the configuration file and enter in your MySQL info, save the file.

Open up the command line and cd (change directory) to the newly created project folder that contains the files.

Run the python script to initiate the automated program, by typing "python3 store_data.py".

This will call the javascript file to fetch all of the requests asyncronously and return new csv files in the project folder, wait (3) the function to complete, then,
it will run the python script to parse the data and upload it to SQL database.
