# import openai
# from dotenv import find_dotenv,load_dotenv
# import os
# import time
# # import logging
# # from datetime import datetime
# from fastapi import FastAPI,UploadFile,File,HTTPException
# from schemas import Assist
# from fastapi.responses import JSONResponse


# assistant_id='asst_RIYccBzR9s2Pi2TizRsTnF5r'

# app=FastAPI()


# load_dotenv()

# client=openai.OpenAI()


# @app.post("/create_thread")
# def create_thread():
# # Create a thread with a message.
#     thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             # Update this with the query you want to use.
                  
#         }
#     ]
# )
#     return (f"created successfully,your thread_id:{thread.id}.Copy this use it in running thread")

# @app.post("/run_thread")
# def run_thread(request: Assist):
#     try:
#         run = client.beta.threads.runs.create(
#             thread_id=request.thread_id,
#             assistant_id=os.getenv('ASSISTANT_ID'),
#             instructions=f"Please address the user as {request.name}. The user has a premium account."
#         )
#         return {"message": f"Run created successfully with ID: {run.id}"}
#     except openai.OpenAIError as e:
#         raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
    

# @app.post("/send_msg")
# def send_msg(message,file: UploadFile = File(...)):
#     global uploaded_file_id
#     message=client.beta.threads.messages.create(
#             thread_id=Assist.thread_id,
#             role= "user",
#             # Update this with the query you want to use.
#             content= {message},
#             file_ids=file.id      
#     )
#     uploaded_file_id=file.id
     
#     run = client.beta.threads.runs.create(thread_id=Assist.thread_id, assistant_id=Assist.ASSISTANT_ID)
#     print(f"👉 Run Created: {run.id}")

#     max_iterations = 5  # Set a reasonable maximum number of iterations
#     iteration_count = 0

#     while iteration_count < max_iterations:
#      run_status = client.beta.threads.runs.retrieve(thread_id=Assist.thread_id, run_id=run.id)
#      print(f"🏃 Run Status: {run_status.status}")
#      if run_status.status == "completed":
#         print(f"🏁 Run Completed!")
#         break
#     iteration_count += 1
#     time.sleep(1)

#     # Get the latest message from the thread.
#     message_response = client.beta.threads.messages.list(thread_id=Assist.thread_id)
#     messages = message_response.data

# # Print the latest message.
#     latest_message = messages[0]
#     print(f"💬 Response: {latest_message.content[0].text.value}")




# @app.delete('/delete_file')
# def del_file():
#     client.files.delete(uploaded_file_id)
#     return(f"File with ID has been deleted.")

# @app.get('/get_files')
# async def get_files():
#     try:
#         # List all files using the OpenAI API
#         files_list = client.files.list()

#         # Display file information
#         if files_list:
#             file_info_list = [
#                 {"file_id": file_info.id, "filename": file_info.filename}
#                 for file_info in files_list
#             ]
#             return JSONResponse(content=file_info_list)
#         else:
#             return JSONResponse(content={"message": "No files found"}, status_code=404)

#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
   



import openai
from dotenv import load_dotenv
import os
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from schemas import Assist
from typing import List

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

# Variable to store uploaded file ID
uploaded_file_id = None
thread_id=None

# Route to create a thread
@app.post("/create_thread")
def create_thread():
    # Create a thread with a message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": "Answer the users question,Act as an Virtual doctor",
            }
        ]
    )
    global thread_id
    thread_id=thread.id
    print(thread.id)
    return {"message": f"Thread created successfully. Thread ID: {thread.id}"}
     
   

# Route to run a thread
@app.post("/run_thread")
def run_thread(request: Assist):
    global thread_id
    try:
        thread_id = request.thread_id

        if thread_id is None:
            raise HTTPException(status_code=400, detail="Thread ID not provided in the request.")

        run = client.beta.threads.runs.create(                     
            thread_id=thread_id,
            assistant_id=os.getenv('ASSISTANT_ID'),
            instructions=f"Please address the user as {request.name}. The user has a premium account."
        )
        return {"message": f"Run created successfully with ID: {run.id}"}
    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")




#send msg and file
@app.post("/send_msg")
def send_msg(message: str, file: UploadFile = File(None)):
    global thread_id
    try:
        # Check if file is provided
        if file is not None:
            # Check file type and size
            allowed_file_types = ["application/pdf", "text/plain"]
            if file.content_type not in allowed_file_types:
                raise HTTPException(
                    status_code=400, detail="Only PDF and plain text files are allowed."
                )

            if file.size > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400, detail="File size exceeds the maximum limit of 10MB."
                )

            # Save the uploaded file
            with open(file.filename, "wb") as f:
                f.write(file.file.read())

            # Create a file on OpenAI
            file_id = client.files.create(file=open(file.filename, "rb"), purpose="assistants").id
            print(f"File ID: {file_id}")

            # Send a user message to the thread with the file
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
                file_ids=[file_id]
            )

            # Clean up the local file
            os.remove(file.filename)

        else:
            # Send a user message to the thread without the file
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
            )

        # Create a run for the thread
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=os.getenv('ASSISTANT_ID'))

        # Wait for the run to complete
        max_iterations = 5
        iteration_count = 0
        while iteration_count < max_iterations:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == "completed":
                break
            iteration_count += 1
            time.sleep(1)

        # Get the latest message from the thread
        message_response = client.beta.threads.messages.list(thread_id=thread_id)
        messages = message_response.data

        # Print the latest message content
        latest_message = messages[0]
        print( "Message sent and assistant run completed successfully.")

        return {f"💬 Response: {latest_message.content[0].text.value}"}

    except Exception as e:
        # Clean up the local file in case of an error
        if file is not None and os.path.exists(file.filename):
            os.remove(file.filename)
        
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Route to delete the uploaded file
@app.delete('/delete_files')
def del_files(file_ids: List[str]):
    try:
        for file_id in file_ids:
            # Attempt to delete each file
            client.files.delete(file_id)
        
        return {"message": f"Files with IDs {file_ids} have been deleted."}

    except openai.OpenAIError as e:
        # Handle OpenAI API error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
   
      

# Route to get a list of files
@app.get('/get_files')
async def get_files():
    try:
        # List all files using the OpenAI API
        files_list = client.files.list()

        # Display file information
        if files_list:
            file_info_list = [
                {"file_id": file_info.id, "filename": file_info.filename}
                for file_info in files_list
            ]
            return JSONResponse(content=file_info_list)
        else:
            return JSONResponse(content={"message": "No files found"}, status_code=404)

    except openai.OpenAIError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    

    

    

    



    
