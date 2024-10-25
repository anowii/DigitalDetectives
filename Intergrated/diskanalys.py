#This module should take in a path in the run function,
# the file input gets processed by sleuthkit and a csv is created
# with the relevant information. 

import subprocess
import sqlite3
import csv
import re
import os
import requests

DATA_DIR = "data\\"
SLEUTH_DB = "data\\analys.db"
CSV_PATH = "data\\db.csv"

INTERESTING_TYPES =".exe|.msi|.docx|.png|.mp4|.jpeg" #files to put in the csv

VIRUSTOTAL_TYPES =".exe|.msi"
VIRUSTOTAL_APIKEY = "4e4140ca9678a7e353a618f2f9aa7dd3a1ff5d70c6eaf812391bb5649b80039e"

def check_with_virustotal(hash):
    # Send request
    url = "https://www.virustotal.com/api/v3/files/" + hash
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUSTOTAL_APIKEY
    }
    response = (requests.get(url, headers=headers)).json()

    # If virustotal returns an error, return undetected
    try:
        vendor_results = response['data']['attributes']['last_analysis_results']
        popular_threat_classification = response['data']['attributes']['popular_threat_classification']['popular_threat_category']
    except:
        return "undetected"

    # Get all vendor results, along with their frequency
    result_list = []
    count_list = []
    for vendor in vendor_results.items():
        category = vendor[1]['category']
        if category not in result_list:
            result_list.append(category)
            count_list.append(0)
        count_list[result_list.index(category)] += 1
    categories = sorted(zip(result_list, count_list), key=lambda x: x[1], reverse=True)
    prime_category = categories[0]

    # Prioritize malicious then suspicious category, if they have a count over 5 (arbitrary)
    for category, count in categories:
        if (category == 'malicious' or category == 'suspicious') and count > 5:
            prime_category = category
            break
    return prime_category + "(" + popular_threat_classification[0]['value'] + ")"

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
    res = subprocess.run(["tsk_loaddb.exe","-h","-d",SLEUTH_DB, target], shell=True)
    return res

def db_to_csv():
    con, cur = connect()
    res = cur.execute("SELECT * FROM tsk_files")
    db_files = res.fetchall()
    print("\ntsk_files\n")
    fields = ["meta_addr", "name","size", "crtime", "parent_path"]
    files = []
    for file in db_files[:800]:
        name = file[5]
        if re.search(INTERESTING_TYPES,file[5]):
            files.append({"meta_addr":file[6], "name":file[5], "size":file[14], "crtime":file[16], "parent_path":file[25]})
        
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
