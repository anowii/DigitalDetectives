# Install and Configuration

This documentation is tailored for a Windows system already configure with VScode and Python.

You will configure and install the following:
1. The Sleuth Kit
2. Ollama and the model llama3.18b
3. A virtual enviroment (Optional)


**Just in case I forget:**
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Virtual Enviroment 

In a virtual environment, you can generate a `requirements.txt` file that lists all the dependencies of your project (`pip freeze > requirements.txt`). Anyone else can use that file to install the exact same versions of the packages (`pip install -r requirements.txt`), ensuring reproducibility.

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
