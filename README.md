# Digital Detectives 

**Rules**
- Create your own branch 
- Commit,pull, etc. to your own branch 
- We create a **main** branch to commit to when final results have been reached
- Comment code and commits
-  Add requierments.txt
- Going forward only push actual code and req.txt onto git

**Everytime I open a new terminal I have to add the following:**
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
```
.\.venv\Scripts\activate       
```

**Run Application** 
Make sure it runs on the right port, create config.yaml in **./ollama** and add **port: 11434**
```
python app.py
```
```
ollmama serve
```
```
ollama run llama3.1 (unsure if this is nessacary)
```
