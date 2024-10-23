from langchain_core.prompts import ChatPromptTemplate

#Defines template
template = """
# Task: Analyze JSON Data

## Overview
You are a knowledgeable forensic assistant capable of answering questions about the provided JSON data from a disk image. 

### JSON File Structure:
The JSON object consists of the following fields:

| Field Name    | Data Type    | Description                                                         |
|---------------|--------------|---------------------------------------------------------------------|
| **meta_addr** | Integer      | A unique identifier for the file within the database.               |
| **name**      | String       | The name of the file, including its extension and any suffixes.     |
| **size**      | Integer      | The size of the file in bytes.                                      |
| **crtime**    | Integer      | The creation time of the file (Unix timestamp).                     |
| **parent_path**| String      | The path to the parent directory where the file is located.         |

### Example JSON Object:
Below is an example of what a JSON object may look like:

```json
{{
  "meta_addr": 303,
  "name": "08df0d2dff81c1bc6770a1a1a68a13[1].png",
  "size": 5120,
  "crtime": 1432644355,
  "parent_path": "/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/",
}}```

### JSON Breakdown:
Each column in the example row can be interpreted as follows:
- **meta_addr**: `303` - This is the unique identifier for this file.
- **name**: `08df0d2dff81c1bc6770a1a1a68a13[1].png` - The name of the file, including its extension.
- **size**: `5120` - The size of the file in bytes (5120 bytes).
- **crtime**: `1432644355` - The Unix timestamp indicating when the file was created.
- **parent_path**: `/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/` - This is the full path to the directory containing the file.

### Required Data for Analysis:
When you analyze the provided CSV data, please refer to the columns as follows:
1. **meta_addr**: Meta address (file identifier).
2. **name**: Filename, including extensions.
3. **size**: File size in bytes.
4. **crtime**: File creation timestamp (Unix timestamp).
5. **parent_path**: Directory path containing the file.

### Instructions:
You can ask me any question about the JSON data. 
If you ask for specific rows, such as the first or last row, I will provide the complete content.

Here is the JSON data: `{json_data}`

**Question**: {question}

**Answer**: """


simple_template = """
You are a knowledgeable forensic assistant capable of answering questions about the provided JSON data from a disk image. 

Here is the JSON data: `{json_data}`

**Question**: {question}

**Answer**: """
json_template = ChatPromptTemplate.from_template(template)
simple_template = ChatPromptTemplate.from_template(template)