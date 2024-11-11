# Installation and Configuration Manual

This documentation is tailored for a Windows system already configure with vscode and Python.

You will configure and install the following:
1. The Sleuth Kit
2. Ollama and the model llama3.18b
3. A virtual enviroment (Optional)

**Windows Powershell**: Can complain quite alot, make sure you run it as ADMIN. Sometimes it complains even if you are running it as admin, then this little code snippet might just solve your problems. 
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## The Sleuth Kit
**Installation**: Follow the link (https://www.sleuthkit.org/sleuthkit/download.php) and download **Windows Binaries**

You have to add the folder where TheSleuthKit keeps all the exe files to your Enviroment variables. If you already know how to do this, you can go ahead and do it.

In the windows serach bar search and choose `Edit the system enviroment variables` and continue from step 4, if that for some reason does not work follow the step-by-step guide. 

**Step 1.** Once installed, extract and move the folder to `C:\Program Files (x86)\sleuthkit-4.12.1-win32` \
**Step 2.** Enter `windows key + X` and choose System in the menue that pops up which takes you to Settings/System/About \
**Step 3.** Here you navigate to Advanced System Settings, which pop ups a new window System Properties \
**Step 4.** Click the Enviroment Variables and add the following 
```
Variable name: Choose and apporpriate one 
Variable value: C:\Program Files (x86)\sleuthkit-4.12.1-win32\bin
```
To make sure everything works as it should open up a powershell and run `fls -v` and it should look like this:

--- Add picture later ---

## Ollama 
Start by dowloading and installing Ollama from the link (https://ollama.com/download). 
When the installation is ready open up a powershell and run:
```
C:\Users\USERNAME> ollama pull llama3.1:8b 
```

## Virtual Enviroment 
You are going to want to replicate the enviroment that our program has been run in, the simplest way to do this is by downloading the code from (link to code) and open the code folder with vscode. The folder will contain a text file called `requirements.txt` which you will use to set up the enviroment. The text file ensures you have the exact same versions of the packages and dependencies as us. 

### Recreate the Virtual Environment on Another Machine (Windows):
**1. Create a Virtual Environment:**
  Open a terminal in vscode and run
  ```
  python -m venv venv
  ``` 

**2. Install the Dependencies from `requirements.txt`:**
Before you install the dependencies you'll want to activate the enviromnent by running the command below in the terminal, beware that you might have to change the command depending on your folder structure.
  ```
   venv\Scripts\activate
  ```
  As long as the enviroment is activated in the terminal you can install the dependencies from whatever folder you like, so navigate to the code       
  folder and run the command below. 
  ```
  pip install -r requirements.txt
  ```
**3. Run the code:** Everything should now be setup and you can run the code with the command `python ui_host.py` and follow the link that comes up in the terminal. When you're done remeber to deactivte the virtual enviroment by issuing the command deactivate in the terminal.

**Remove virtual enviroment:**
  If you would like to remove the enviroment when you're done just run the command
  ```
    Remove-Item -Recurse -Force venv
  ```
