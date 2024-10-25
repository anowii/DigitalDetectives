#name,size,crtime,parent_path,virus(true or false),
import csv
import random
from random import randrange

def create_a_csv(csv_file_path="test.csv", length=10):
    name_arg = ["totally_legit.exe", 
                "banana.png", 
                "passionfruit.png", 
                "Fresh_Apples_on_Kitchen_Counter.jpeg",
                "Bowl_of_Fresh_Fruit_Salad.jpeg",
                "Ripe_Bananas_on_Tree.jpeg",
                "Strawberry_Picking_Adventure.jpeg",
                "Juicy_Oranges_on_Stand.jpeg",
                "Watermelon_Slices_on_Summer_Picnic.jpeg",
                "Mango_Orchard_Visit.jpeg",
                "Colorful_Fruit_Platter_for_Party.jpeg",
                "Pineapple_in_Garden.jpeg",
                "Cherry_Blossoms_and_Fruit.jpeg",
                "Coconut_Open_on_Beach.jpeg",
                "Berries_Collection_in_Garden.jpeg",
                "Kiwi_Cut_in_Half.jpeg",
                "Fruit_Smoothie_Bowl.jpeg",
                "Grapes_on_Vine.jpeg",
                "Avocado_Garden_Photos.jpeg",
                "Blueberry_Bush_Harvest.jpeg",
                "Dark Souls III.exe",
                "Sekiro: Shadows Die Twice.exe",
                "The Witcher 3: Wild Hunt.exe",
                "Final Fantasy VII Remake.exe",
                "Cyberpunk 2077.exe",
                "Persona 5.exe",
                "Dragon Age: Inquisition.exe",
                "Divinity: Original Sin 2.exe",
                "Skyrim.exe",
                "Call of Duty: Modern Warfare.exe",
                "Counter-Strike: Global Offensive.exe",
                "ILOVEYOU.exe",
                "MyDoom.exe",
                "Conficker.exe",
                "Melissa.exe",
                "Sasser.exe",
                "Nimda.exe",
                "Blaster.exe",
                "Klez.exe",
                "CryptoLocker.exe",
                "WannaCry.exe",
                "Zeus.exe",
                "Stuxnet.exe",
                "Shylock.exe",
                "Gamarue.exe",
                "Locky.exe",
                "Emotet.exe",
                "Sasser.exe",
                "Ramnit.exe",
                "Ransomware.exe",
                "Bad Rabbit.exe",
                "Dridex.exe",
                "Cabal.exe",
                "Qakbot.exe",
                "TrickBot.exe",
                "Tinba.exe",
                "Bait and Switch.exe",
                "Bouncy.exe",
                "Kronos.exe",
                "SpyEye.exe",
                "John_Doe_Birthday_Party_2024-10-09.jpeg",
                "Vacation_Paris_2024-06-15.jpeg",
                "Wedding_Ceremony_Jane_&_Mark_2024-05-22.jpeg",
                "Family_Reunion_2023-08-13.jpeg",
                "Sunset_Beach_California_2024-07-18.jpeg",
                "Graduation_Ceremony_Emma_2024-05-01.jpeg",
                "Hiking_Trip_Mountains_2024-09-10.jpeg",
                "Christmas_Eve_Family_2023-12-24.jpeg",
                "New_Year_Celebration_2024-01-01.jpeg",
                "Beach_Vacation_Florida_2024-03-15.jpeg",
                "Picnic_in_the_Park_2023-07-20.jpeg",
                "Concert_Night_Rock_Band_2024-04-12.jpeg",
                "Dog_Park_Day_2023-09-05.jpeg",
                "Skiing_Trip_Colorado_2024-02-10.jpeg",
                "Thanksgiving_Dinner_2023-11-23.jpeg",
                "Graduation_Party_Mike_2024-05-30.jpeg",
                "Summer_Festival_2024-08-01.jpeg",
                "Baby_Shower_Susan_2024-03-25.jpeg",
                "Camping_Weekend_Lake_2024-06-18.jpeg",
                "Valentine's_Day_Dinner_2024-02-14.jpeg",
                "Family_Photo_Thanksgiving_2023-11-24.jpeg",
                "Road_Trip_to_Grand_Canyon_2024-07-05.jpeg",
                "Pet_Birthday_Party_Fido_2024-09-15.jpeg",
                "Birthday_Surprise_For_Alice_2024-10-01.jpeg",
                "Visit_to_Grandparents_2023-10-10.jpeg",
                "Easter_Egg_Hunt_2024-04-20.jpeg",
                "Halloween_Costume_Party_2023-10-31.jpeg",
                "Nature_Hike_Spring_2024-05-15.jpeg",
                "Cooking_Class_2024-03-10.jpeg",
                "First_Day_of_School_Jake_2024-09-01.jpeg",
                "Flower_Show_2024-06-25.jpeg",
                "Weekend_Getaway_to_NYC_2024-04-28.jpeg",
                "homepage.html",
                "style_main.css",
                "script_utilities.js",
                "user_data.json",
                "app_config.yaml",
                "data_analysis.py",
                "main_controller.java",
                "api_server.js",
                "app_styles.scss",
                "schema_definition.sql",
                "README_Installation.md",
                "requirements_project.txt",
                "Dockerfile_service",
                "package_frontend.json",
                "Visual Studio Code.exe",
                "Sublime Text.exe",
                "Atom.exe",
                "Notepad++.exe",
                "Brackets.exe",
                "Vim.exe",
                "Emacs.exe",
                "TextMate.exe",
                "NetBeans.exe",
                "Eclipse.exe",
                "Bluefish.exe",
                "Kate.exe",
                "Coda.exe"
                
                ]
    size_arg = [64, 128, 4096, 1024, 512, 2048, 8192, 1347, 1273, 1268]
    crtime_arg = 1432644354 #make a random minus or plus for this number
    path_arg = ["/", "/Documents", "/Music", "/Downloads", "/Documents/School", "/Temp", "/"]
    mal_arg = ["Undetected", "Detected", "Suspicious"]
    mal_type_arg = ["Trojan", "Worm", "Keylogger", "Adware", "Ransomware", "Spyware", ]
    

    data = [[]]

    data[0] = ["name", "size", "crtime", "parent_path", "mal", "mal_type"]
    for i in range(length):
        temp_data = []
        
        temp = random.choice(name_arg)
        while(True):
            exists = False
            for i in data:
                if i[0] == temp:
                    exists = True
            if exists == False:
                break
            else:
                temp = random.choice(name_arg)

        temp_data.append(temp)
        temp_data.append(random.choice(size_arg))
        temp_data.append(crtime_arg+randrange(-2000, 2000))
        temp_data.append(random.choice(path_arg))

        #if file is .exe random if virus
        if (temp[temp.find(".")::] == ".exe"):
            if (randrange(0, 100) < 40):
                temp_data.append(mal_arg[randrange(1, 3)])
                temp_data.append(random.choice(mal_type_arg))
            else:
                temp_data.append(mal_arg[0])
                temp_data.append("None")
        else:
            temp_data.append(mal_arg[0])
            temp_data.append("None")


        data.append(temp_data)

    # Open the file in write mode
    with open(csv_file_path, mode='w', newline='') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerows(data)

    # Print a confirmation message
    print(f"CSV file '{csv_file_path}' created successfully.")

if __name__ == "__main__":

    
    create_a_csv("test_10.csv", 10)
    create_a_csv("test_15.csv", 15)
    create_a_csv("test_20.csv", 20)
    create_a_csv("test_30.csv", 30)
    create_a_csv("test_40.csv", 40)
    create_a_csv("test_50.csv", 50)
