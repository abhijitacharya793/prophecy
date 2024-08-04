template = """
Answer the question below

Here is the conversation history: {context}

Question: {question}

Answer: 
"""

path_example = """
Example:
Correct:
/path/to/file1.java
/path/to/file2.java

Incorrect:
1. /path/to/file1.java
2. /path/to/file2.java\n
"""

prompt_get_controller_path = "Given the set of files, which of them most likely are api server controller files? The " \
                             "file path may have words like controller, client, api in them. Do not include any " \
                             "extra text, bullets, or numbering. Just list the file paths separated by a new line."

prompt_get_curl_commands = "Analyze the code and identify all instances of API endpoints with their respective HTTP " \
                           "methods. Additionally, consider any dynamic paths or variables within the annotations. " \
                           "Please extract and return the list of these endpoints as curl command separated by " \
                           "newlines and dont print any help text."
