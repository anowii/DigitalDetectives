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
Make sure everything that everything works, Open up a powershell and run `fls -v`. The result should look like this: 

--- Add picture later ---

## Ollama 
Start by dowloading and installing Ollama from the link (https://ollama.com/download). 
When the installation is ready open up a powershell and run:
```
C:\Users\USERNAME> ollama pull llama3.1:8b 
```

## Virtual Enviroment 
To replicate the environment our program was run in, download the code from (link to code) and open the code folder with VS Code. Inside, you'll find a file called `requirements.txt`, which you can use to set up the environment. This file ensures you have the exact same versions of packages and dependencies as we do.

### Recreate the Virtual Environment on Another Machine (Windows):
**1. Create a Virtual Environment:**
  Open a terminal in vscode and run
  ```
  python -m venv venv
  ``` 

**2. Install the Dependencies from `requirements.txt`:**
Before installing the dependencies, activate the environment by running the command below in the terminal. Note that you may need to adjust the command based on your folder structure.
  ```
   venv\Scripts\activate
  ```
As long as the environment is activated in the terminal, you can install dependencies from any folder. Navigate to the code folder and run the command below.
  ```
  pip install -r requirements.txt
  ```
**3. Run the code:** Everything should now be set up, and you can run the code with the command `python ui_host.py`. Follow the link that appears in the terminal. When you're finished, deactivate the virtual environment by entering the `deactivate` command in the terminal.

**Remove virtual enviroment:**
 To remove the enviroment completely, run the command below.
  ```
    Remove-Item -Recurse -Force venv
  ```
