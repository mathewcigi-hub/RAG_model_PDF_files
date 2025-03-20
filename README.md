# RAG_model_PDF_files
For reading from PDF files stores in a folder using Gemini-1.5-pro-latest

If needs to changes the github repo to another account -> 
 - Go to Control panel -> Windows Credentials -> github.com -> chnage the username and password


 ## RAG model

 1. Downloads the package from "requirements.txt"
           python -r requirements.txt

 2. Run the "RAG_model.py" code 
 3. A UI will open which shows the "Folder_path" in which the location of the folder which contains the pdf files is given
 4. Ask a question in the "Ask a question" window.
 5. The answer will be displayed on the below text box


## NOTE
The API key was used in making the code was from free Gemini API. There by it can have limitations size and time.

The code is given a 10 sec delay between the question and answer, this is because the gemini API keys have a limit in the request to be made (limited number of request per time). To avoid that issue, the delay is given internally.
