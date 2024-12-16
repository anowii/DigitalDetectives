# This module should take in a path in the run function,
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
USER_DB = "data\\user.db"
CSV_PATH = "data\\db.csv"

# Files types that will be included in CSV
INTERESTING_TYPES = ".exe|.msi|.docx|.png|.jpeg|.txt|.dat" 

VIRUSTOTAL_TYPES =".exe|.msi"
VIRUSTOTAL_APIKEY = "4e4140ca9678a7e353a618f2f9aa7dd3a1ff5d70c6eaf812391bb5649b80039e"
ALLOWED_FIELDS = ["name","size", "crtime", "parent_path", "malware_class", "delete_flag"]

    ############################################
    #  delete_flag == dir_flag in tsk_files    #
    #  tsk_files {allocated, 1} = NOT deleted  #
    #  in delete_flag: 0 == not deleted        #
    #                                          #
    #  tsk_files {unallocated, 2} = deleted    #
    #  in delete_flag: 1 == deleted            #     
    ############################################


def check_with_virustotal(hash):
   
    try:
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
            print("Exept 2")
            return "None"

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
        return prime_category if prime_category != "nan" else "None"
    except TypeError:
        print("Error: Hash value is None and cannot be concatenated to the URL")
        return "None"

# Connects to Slueth_kit database
def connect():
    con = sqlite3.connect(SLEUTH_DB)
    cur = con.cursor()
    return con, cur

# Check if the input file is 
def check_input_file(target):
    print("Check "+ target)

def run_sleuth_on_file(target):
    print("Check "+ target)
    if os.path.exists(SLEUTH_DB):
        os.remove(SLEUTH_DB)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    res = subprocess.run(["tsk_loaddb","-h","-d", SLEUTH_DB, target], shell=True)
    return res

def db_to_csv():
    
    con, cur = connect()
    res = cur.execute("SELECT * FROM tsk_files")
    db_files = res.fetchall()
    con.close()

    print("\ntsk_files\n")
    global ALLOWED_FIELDS
    files = []
    for file in db_files:
        if re.search(INTERESTING_TYPES,file[5]) and file[5].find("slack") == -1:
      
            prime_category = check_with_virustotal(file[23])
            print(prime_category)
            
            #Ensure delete_flag is correctly assigned
            delete_flag = -1
            if file[13] == 1:
                delete_flag = 0
            elif file[13] == 2:
                delete_flag = 1

            csv_row = {
                "name": file[5], 
                "size": file[15], 
                "crtime": file[17], 
                "parent_path": file[25],
                "malware_class" : prime_category,
                "delete_flag": delete_flag
            }
            files.append(csv_row)
        
    with open(CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ALLOWED_FIELDS)
        writer.writeheader()
        writer.writerows(files)
    csvfile.close()

def create_database_from_csv(csv_path):

    global ALLOWED_FIELDS
   # Remove the database file if it already exists
    if os.path.exists(USER_DB):
        os.remove(USER_DB)
        print(f"Existing database '{USER_DB}' has been removed.")
   
   # Define column types 
    column_types = {
        "name": "TEXT",
        "size": "INTEGER",
        "crtime": "INTEGER",
        "parent_path": "TEXT",
        "malware_class": "TEXT",
        "delete_flag": "INTEGER"
    }

    # Connect to SQLite database (it will create a new database if it doesn't exist)
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()

    # Open the CSV file and read data
    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Skip header row
        

        if(ALLOWED_FIELDS == header): 
            # Build the columns and types for the table
            columns = ', '.join([f"{col} {column_types.get(col, 'TEXT')}" for col in header])

            # Create table based on the CSV header
            cursor.execute(f"CREATE TABLE IF NOT EXISTS file_table ({columns})")
            print(f"Table created with columns: {columns}")

            for row in reader:
                # Replace empty fields with None (which will be NULL in SQLite)
                row_with_nulls = [None if (field == 'None' or field == '') else field for field in row]

                # Create placeholders for the values
                placeholders = ', '.join(['?'] * len(row))
                cursor.execute(f"INSERT INTO file_table ({', '.join(header)}) VALUES ({placeholders})", row_with_nulls)
    csv_file.close()

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{USER_DB}' created successfully from '{csv_file}'.")



def run(disk_image_path):
    check_input_file(disk_image_path)
    run_sleuth_on_file(disk_image_path)
    db_to_csv()
    create_database_from_csv(CSV_PATH)

    return CSV_PATH