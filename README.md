# Team 1: Digital Detectives 
Our team consists of 6 members: 
- Anna Almgren
- Jacob Nawrouzi
- Adrian Adborn
- Viktor Listi
- William Knutsson
- David Tammpere _(team leader and scrum master)_

### Project focus 
Our project aims to develop an LLM-powered forensic tool capable of parsing all files and objects extracted from an HDD image. Additionally, it provides the functionality to answer questions about the disk image.

### GitHub and Branch Structure
There are three branches, on for each sprint.

- **master/**
  - **Pre-study/**: Testing done in the pre-study
  - **Final-program/**: The final project 
  - `installation_manual.md`: Installation and configuration manual
  - **Usage Manual**: is provided in the final documentation:`7.Usage`
  - **reports/**: Download the report to veiw it in the correct format
    - OWASP ZAP: `2024-12-09-ZAP-Report-.html`
- **project-sprint1/**
  - Branch for work done in sprint 1
- **project-sprint2/**
  - Branch for work done in sprint 2
- **project-sprint3/**
  - Branch for work done in sprint 3

## Final Program: Overview

### Folders
- **data\\**: Stores uploaded disk image/csv, user.db and analysis.db which SleuthKit creates.
- **static\\**: Javascript files
- **templates\\** HTML files
- **test-data\\**: Feel free to use the provided testfiles
    -  `test_10.csv`
    -  `test_20.csv`
    -  `test_30.csv`
    -  `test_40.csv`
    -  `test_50.csv`
      
### Other Test Data
A disk image from CFReDS was also used to prefrom some of the testing: 
- Link to the disk image in EO1 format ➡️ [disk image](https://cfreds.nist.gov/all/DFIR_AB/ForensicsImageTestimage)
- Link to the disk image converted to .dd format on our drive ➡️ [.dd Format Link](https://drive.google.com/file/d/1Fd1pX1r4waRkD6Z2O8J5cRZyeSNU5-SY/view)

### Important Files
- `diskanalysis.py`: Runs Sleuth Kit and Virustotal, also creates user.db
- `requirements.txt`: Requirements for running the program
- `templates.py`: Prompt templates for the LLM
- `messages.json`: Logs the messages written during a session
- `ui_backend.py`: Backend functionality to ui_host.py
- `ui_host.py`: Hosts the webb application 

### Folder Overveiw
```
Program
├── data
|   |── assets
|   |   |── brain.svg 
├── static
│   ├── chat.js
│   ├── context_btn.js 
│   ├── delete_button.js
│   ├── download_chat.js
│   ├── file_submit.js
│   ├── home.css
│   ├── login.css
├── templates
│   ├── home.html
│   ├── index.html
├── diskanalysis.py
├── messages.json
├── requirements.txt
├── templates.py
├── ui_backend.py
├── ui_host.py
```
