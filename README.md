CLA
===

0. Setup
------------
In addition to standard Python libraries, the CLA project depends heavily on the ```unicodecsv``` module, a drop in replacement for the standard ```csv``` module. Although the script will not fail to run without unicodecsv installed (it will crash down to the standard ```csv``` module), unicode handling will be unpredictable, and it is frankly unlikely that it will run successfully. For any of the relational database elements of this project, a working sqlite installation and the ```sqlite3``` module are required.

1. Data processing
----------------
Download the formatted CLA spreadsheets from the DARMC Google Drive in the format ```cla_volume_XX.csv``` into the main project directory. Once all volumes are downloaded, execute ```$ python process_raw_cla_data.py```


2. Query Utility
----------------
