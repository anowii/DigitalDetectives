# Digital Detectives 


**Everytime I open a new terminal I have to add the following:**
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
```
.\.venv\Scripts\activate       
```
## Virtual Enviroment 

In a virtual environment, you can generate a `requirements.txt` file that lists all the dependencies of your project (`pip freeze > requirements.txt`). Anyone else can use that file to install the exact same versions of the packages (`pip install -r requirements.txt`), ensuring reproducibility.

### Recreate the Virtual Environment on Another Machine (Windows):
**1. Create a Virtual Environment:**
  ```
  python -m venv venv
  ```
  ```
  venv\Scripts\activate
  ```
**2. Install the Dependencies from `requirements.txt`:**
  ```
  pip install -r requirements.txt
  ```
