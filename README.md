CLA
===

0. Setup
------------
In addition to standard Python libraries, the CLA project depends heavily on the ```unicodecsv``` module, a drop in replacement for the standard ```csv``` module. ```unicodecsv``` is distributed through the PyPI and can be installed using ```$ pip install unicodecsv```. For any of the relational database elements of this project, a working sqlite installation and the ```sqlite3``` module are required. This should be available by default on a Mac or Linux system. Instructions for setting up SQLite on Windows can be found online, although you will have to build and set path variables for it to work correctly.

1. Data processing
----------------
Download the full CLA spreadsheet from the DARMC Google Drive, DARMC/CLA/Complete CLA Database as a csv file and place it in the CLA project directory. As of January 2014, the CLA database has been moved to a new format Google Spreadsheet and no longer requires multiple files to be processed and combined because the limit of 400,000 cells has been removed (new limit appears to be 2.1m cells). 

Then, run ```$ python process_raw_cla_data.py``` or run the two processing scripts directly using ```$ python generate_cla_database_segments.py && python generate_edge_table.py```. You will get four output files from these scripts:
(1)
(2)
(3)
(4)


2. Visualization
----------------
The CLA database is currently optimized to be used for analysis in Gephi and ArcGIS. 

3. Relational Database
---------------------

Finally, the CLA process outputs a simple SQLite database containing manuscript attributes and movements to allow data to be extracted using traditional SQL query and join methods.  
