## Final Delivery Project

**Folders**
- **data\\**: Stores uploaded disk image/csv, user.db and analysis.db which SleuthKit creates.
- **static\\**: Javascript files
- **templates\\** HTML files

**Important Files**
- `diskanalysis.py`: Runs Sleuth Kit and Virustotal, also creates user.db
- `requirements.txt`: Requirements for running the program
- `templates.py`: Prompt templates for the LLM
- `messages.json`: Logs the messages written during a session
- `ui_backend.py`: Backend functionality to ui_host.py
- `ui_host.py`: Hosts the webb application 

**Folder Overveiw**
```
Program
├── data
|   |── assets
|   |   |── brain.svg 
│   ├── analys.db
│   ├── user.db
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
├── requirements.txt
├── ui_backend.py
├── ui_host.py
```
