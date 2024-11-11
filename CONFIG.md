# Install and Configuration

This documentation is tailored for a Windows system already configure with vscode and Python.

You will configure and install the following:
1. The Sleuth Kit
2. Ollama and the model llama3.18b
3. A virtual enviroment (Optional)

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

## Virtual Enviroment 

In a virtual environment, you can generate a `requirements.txt` file that lists all the dependencies of your project (`pip freeze > requirements.txt`). Anyone else can use that file to install the exact same versions of the packages (`pip install -r requirements.txt`), ensuring reproducibility.

**Just in case I forget:**
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Remove virtual enviroment:**
  ```
    Remove-Item -Recurse -Force .venv
  ```
**List all dependencies to file:**
  ```
  pip freeze > requirements.txt
  ```
### Recreate the Virtual Environment on Another Machine (Windows):
**1. Create a Virtual Environment:**
  ```
  python -m venv .venv
  ```
  ```
 .\.venv\Scripts\activate
  ```
**2. Install the Dependencies from `requirements.txt`:**
  ```
  pip install -r requirements.txt
  ```
