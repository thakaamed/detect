# file_upload/tasks.py

from celery import shared_task

@shared_task
def process_uploaded_file(file):
    # Process the uploaded file here
    # For example, save it to the database or perform some processing
    print("file", file)
    
    pass
