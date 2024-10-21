#This module should take in a path in the run function,
# the file input gets processed by sleuthkit and a csv is created
# with the relevant information. 

import subprocess
import sqlite3
import csv
import re
import os

DATA_DIR = "data\\"
SLEUTH_DB = "data\\analys.db"
CSV_PATH = "data\\db.csv"

INTERESTING_TYPES =".exe|.msi|.docx|.png|.mp4|.jpeg" #files to put in the csv

def connect():
    con = sqlite3.connect(SLEUTH_DB)
    cur = con.cursor()
    return con, cur

#Check if the input file is valid
def check_input_file(target):
    print("Check "+ target)

def run_sleuth_on_file(target):
    print("Check "+ target)
    # subprocess.run(["rm",SLEUTH_DB], text=True)
    if os.path.exists(SLEUTH_DB):
        os.remove(SLEUTH_DB)
    # subprocess.run(["rm",CSV_PATH], text=True)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    res = subprocess.run(["tsk_loaddb.exe","-h","-d",SLEUTH_DB, DATA_DIR+target], shell=True)
    return res

def db_to_csv():
    con, cur = connect()
    res = cur.execute("SELECT * FROM tsk_files")
    db_files = res.fetchall()
    print("\ntsk_files\n")
    fields = ["meta_addr", "name", "dir_type", "size", "crtime", "parent_path"]
    files = []
    for file in db_files:
        name = file[5]
        if re.search(INTERESTING_TYPES,file[5]):
            files.append({"meta_addr":file[6], "name":file[5], "dir_type": file[12], "size":file[14], "crtime":file[16], "parent_path":file[25]})
        
    with open(CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(files)
    csvfile.close()

def run(disk_image_path):
    
    check_input_file(disk_image_path)
    run_sleuth_on_file(disk_image_path)
    db_to_csv()

    return CSV_PATH
