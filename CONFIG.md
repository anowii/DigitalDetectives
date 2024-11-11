# Installation and Configuration Manual

This documentation is tailored for a Windows system already configured with VSCode and Python.

You will configure and install the following:
1. The Sleuth Kit
2. Ollama and the model llama3.18b
3. A virtual enviroment (Optional)

**Windows Powershell** can sometimes be fussy, so make sure to run it as an administrator. If you still encounter issues even with admin privileges, try running the following command to resolve them:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
This command sets the execution policy for the current user to allow running scripts, which may help clear up common permission-related issues.

## The Sleuth Kit
**Installation**: Follow the link (https://www.sleuthkit.org/sleuthkit/download.php) and download **Windows Binaries**.

You'll need to add the folder containing The Sleuth Kit's `.exe` files to your environment variables. If you're already familiar with this process, you can go ahead and do it.

Otherwise, search for Edit the system environment variables in the Windows search bar and start from step 4. If that doesn't work for any reason, follow the step-by-step guide below.

**Step 1.** After installation, extract the files and move the folder to `C:\Program Files (x86)\sleuthkit-4.12.1-win32` \
**Step 2.** Press the `Windows key + X` and select _System_ from the menu, which takes you to _Settings_>_System_>_About_ \
**Step 3.** Navigate to _Advanced System Settings_, which will open a new window titled _System Properties_ \
**Step 4.** Click _Enviroment Variables_ and add the following path ` C:\Program Files (x86)\sleuthkit-4.12.1-win32\bin `

Make sure everything that everything works, Open up a powershell and run `fls -v`. The result should look somthing like this: 
```
system> fls -v
Missing image name
usage: C:\Program Files (x86)\sleuthkit-4.12.1-win32\bin\fls.exe
[-adDFlhpruvV] [-f fstype] [-i imgtype] [-b dev_sector_size]
[-m dir/] [-o imgoffset] [-z ZONE] [-s seconds] image [images] [inode]
        If [inode] is not given, the root directory is used
        -a: Display "." and ".." entries
        -d: Display deleted entries only
        -D: Display only directories
            ....
            ....
            ....
        -V: Print version
        -z: Time zone of original machine (i.e. EST5EDT or GMT) (only useful with -l)
        -s seconds: Time skew of original machine (in seconds) (only useful with -l & -m)
        -k password: Decryption password for encrypted volumes
```

## Ollama 
Start by dowloading and installing Ollama from the link (https://ollama.com/download). 
When the installation is ready open up a powershell and run:
```
> ollama pull llama3.1:8b 
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
