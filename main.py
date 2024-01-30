# import openai
# from dotenv import find_dotenv,load_dotenv
# import time
# import logging
# from datetime import datetime

# load_dotenv()

# client=openai.OpenAI()
# # model='gpt-3.5-turbo-16k'

# # #creating our assistant
# # personal_doctor_assis=client.beta.assistants.create(
# #     name="personal-doctor",
# #     instructions="you are the best doctor,Given a patient's symptoms and medical history, provide a detailed diagnosis, recommended treatment plan, and any additional relevant information",
# #     model=model )

# # assistant_id=personal_doctor_assis.id
# assistant_id='asst_RIYccBzR9s2Pi2TizRsTnF5r'

# # print(assistant_id)

# #creating thread
# # thread=openai.beta.threads.create(
# #     messages=[{
# #         "role":"user",
# #         "content":"i have severe cold.how to get rid on this "
# #     }]
# # )

# # thread_id=thread.id
# # print(thread_id)

# thread_id='thread_H6gBqg3H0sUkX3kFbMCanvgy'


# #asst_RIYccBzR9s2Pi2TizRsTnF5r
# #thread_H6gBqg3H0sUkX3kFbMCanvgy

# #setting msg

# message="i have severe cold.how to get rid on this"
# message=client.beta.threads.messages.create(
#     thread_id=thread_id,
#     role='user',
#     content=message
# )

# #run the asssist

# run = client.beta.threads.runs.create(
#   thread_id=thread_id,
#   assistant_id=assistant_id,
#   instructions="Please address the user as decaprio. The user has a premium account."
# )

# # def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
# #     while True:
# #         try:
# #             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
# #             if run.completed_at:
# #                 elapsed_time = run.completed_at - run.created_at
# #                 formatted_elapsed_time = time.strftime(
# #                     "%H:%M:%S", time.gmtime(elapsed_time)
# #                 )
# #                 print(f"Run completed in {formatted_elapsed_time}")
# #                 logging.info(f"Run completed in {formatted_elapsed_time}")
# #                 break
# #         except Exception as e:
# #             logging.error(f"An error occurred while retrieving the run: {e}")
# #             break
        
# #         try:
# #             messages = client.beta.threads.messages.list(thread_id=thread_id)
# #             last_message = messages.data[0]
# #             response = last_message.content[0].text.value
# #             print(f"Assistant Response: {response}")
# #         except Exception as e:
# #             logging.error(f"An error occurred while retrieving messages: {e}")

# #         logging.info("Waiting for run to complete...")
# #         time.sleep(sleep_interval)



# def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
#     """

#     Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
#     :param thread_id: The ID of the thread.
#     :param run_id: The ID of the run.
#     :param sleep_interval: Time in seconds to wait between checks.
#     """
#     while True:
#         try:
#             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#             if run.completed_at:
#                 elapsed_time = run.completed_at - run.created_at
#                 formatted_elapsed_time = time.strftime(
#                     "%H:%M:%S", time.gmtime(elapsed_time)
#                 )
#                 print(f"Run completed in {formatted_elapsed_time}")
#                 logging.info(f"Run completed in {formatted_elapsed_time}")
#                 # Get messages here once Run is completed!
#                 messages = client.beta.threads.messages.list(thread_id=thread_id)
#                 last_message = messages.data[0]
#                 response = last_message.content[0].text.value
#                 print(f"Assistant Response: {response}")
#                 break
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the run: {e}")
#             break
#         logging.info("Waiting for run to complete...")
#         time.sleep(sleep_interval)

# # # run wait function
# #         wait_for_run_completion(client,thread_id,run_id,)         

# # #steps
# # run_steps = client.beta.threads.messages.list(
# #   thread_id=thread_id,
# #  )

# # print(f'steps---->{run_steps.data}')
        
#         wait_for_run_completion(client=client, thread_id=thread_id,run_id=run.id)

# # ==== Steps --- Logs ==
# # run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)

# # print(f'steps---->{run_steps.data}')

# messages = client.beta.threads.messages.list(
#   thread_id=thread_id
# )
# msg=messages.data

# latest_msg=msg[0]
# print(f"response:{latest_msg.content[0].text.value}")



import time
from openai import OpenAI
import streamlit as st

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_RIYccBzR9s2Pi2TizRsTnF5r"
thread_id='thread_H6gBqg3H0sUkX3kFbMCanvgy'

# Make sure your API key is set as an environment variable.
client = OpenAI()

#upload file to assistant
# filepath='./PatientAssessment.pdf'
# file_object=client.files.create(file=open(filepath,'rb'),purpose='assistants')

# print(f"File ID: {file_object.id}")
# print(f"File Purpose: {file_object.purpose}")

#Create a thread with a message.
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             # Update this with the query you want to use.
#             "content": "i got severe fevere,how to get rid on this",
#             "file_ids":file_object.id
#         }
#     ]
# )

# message="can you summarize the patient details,given in below document?"
# message=client.beta.threads.messages.create(
#     thread_id=thread_id,
#     role='user',
#     content=message,
#     file_ids=[file_object.id]
# )


#deleting file
# client.files.delete('file-EFYXnMHXe5fhffMqJUTBpsJY')

# print(f"File with ID has been deleted.")

# Submit the thread to the assistant (as a new run).
run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=ASSISTANT_ID)
print(f"👉 Run Created: {run.id}")



# Wait for run to complete.
# while run.status != "completed":
#     run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
#     print(f"🏃 Run Status: {run.status}")
#     time.sleep(1)
# else:
#     print(f"🏁 Run Completed!")

max_iterations = 5  # Set a reasonable maximum number of iterations
iteration_count = 0

while iteration_count < max_iterations:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    print(f"🏃 Run Status: {run_status.status}")

    if run_status.status == "completed":
        print(f"🏁 Run Completed!")
        break

    iteration_count += 1
    time.sleep(1)


    # List all files
files_list = client.File.list()

# Display file information
if files_list:
    for file_info in files_list:
       print(f"File ID: {file_info.id}, Filename: {file_info.filename}")

# Get the latest message from the thread.
message_response = client.beta.threads.messages.list(thread_id=thread_id)
messages = message_response.data

# Print the latest message.
latest_message = messages[0]
print(f"💬 Response: {latest_message.content[0].text.value}")

