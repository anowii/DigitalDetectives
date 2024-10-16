**Issues**
- Prompt template is way to large, i've added template called small template (see templates.py) that also allows for testing with json format

**Changes made 2024-10-16**
  - Change a little bit in forward_message_llm
  - Added load_json_data(filename), only static

```plaintext
│   .flaskenv                       //Only if you wanna be use: flask run (not needed)
│   conversation_history.json
│   diskanalys.py    
│   templates.py                    //Prompt templates are defined here
│   ui_backend.py
│   ui_host.py
│
├───static
│       chat.js
│       file_submit.js
│       home.css
│       login.css
│
├───tempfiles
│       MOCK_DATA2.csv
│
├───templates
│       home.html
│       login.html

```
