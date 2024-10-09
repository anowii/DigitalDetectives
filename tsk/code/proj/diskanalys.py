#This module should take in a path in the run function,
# the file input gets processed by sleuthkit and a csv is created
# with the relevant information. 

import subprocess
import sqlite3
import csv

TMP_DIR = "tmp_disk_analys/"
DATA_DIR = "/home/nalle/Documents/proj/data/"
SLEUTH_DB = "/home/nalle/Documents/proj/data/analys.db"
CSV_PATH = "/home/nalle/Documents/proj/data/db.csv"

def connect():
    con = sqlite3.connect(SLEUTH_DB)
    cur = con.cursor()
    return con, cur

#Check if the input file is valid
def check_input_file(target):
    print("Check "+ target)

def run_sleuth_on_file(target):
    print("Check "+ target)
    subprocess.run(["rm",SLEUTH_DB], text=True)
    subprocess.run(["rm",CSV_PATH], text=True)
    res = subprocess.run(["tsk_loaddb","-d",DATA_DIR+"analys.db", target, "-h"], text=True)
    return res

def db_to_csv():
    con, cur = connect()
    res = cur.execute("SELECT * FROM tsk_files")
    db_files = res.fetchall()
    print("\ntsk_files\n")
    fields = ["obj_id", "name", "meta_addr", "dir_flags" ,"size", "ctime", "crtime", "md5", "parent_path"]
    files = []
    for file in db_files:
        files.append({"obj_id":file[0], "name":file[5], "meta_addr":file[6], "dir_flags": file[12],"size":file[14], "ctime":file[15], "crtime":file[16], "md5":file[23], "parent_path":file[25]})
        
    
    with open(CSV_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(files)
    csvfile.close()

def run(disk_image_path):
    
    check_input_file(disk_image_path)
    subprocess.run(["mkdir", TMP_DIR], text=True)
    run_sleuth_on_file(disk_image_path)
    db_to_csv()
    subprocess.run(["rm","-r", TMP_DIR], text=True)
    return CSV_PATH

run("/home/nalle/Documents/diskanalys/data/2020JimmyWilson.dd")