CLA
===

0. Setup
------------
Everything in the CLA project is pretty modular (read: disorganized), and so there isn't a great deal to build, set up, or 'install' in any sense of the word. As of last count, the complete list of python dependencies for this project is as follows:

Stuff you already have:
os
glob
unicodecsv
sys
time

Stuff you don't:
unicodecsv
sqlite3

If you don't already have a working sqlite build on your machine, go make that happen. It's not too complicated on Mac and other unix systems. I hear it can be kind of a pain on Windows systems, but I've never tried. Don't rule out running a simple Ubuntu box under emulation to save yourself the hassle.

Before you do anything else, just run ```$ set_up_sqlite_database.py``` in your project directory. That will create 