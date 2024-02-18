from time import sleep
from config.settings import OPENAI_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_KEY)

def create_file(file):
    response = client.files.create(
        file=open(file, 'rb'),
        purpose='assistants'
    )
    return response.id


def delete_file(file_id: str):
    response = client.files.delete(
        file_id=file_id,
    )
    return response.deleted


def get_file(file_id: str):
    response = client.files.retrieve(
        file_id=file_id
    )
    return response


def create_asistant():
    response = client.beta.assistants.create(
        name="Rozievich AI",
        instructions="Analyzing user submitted files and providing business development advice and guidance.",
        tools=[{"type": "retrieval"}],
        model="gpt-4",
        file_ids=[],
    )
    return response.id

def create_thread(message=None):
    if message:
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user", "content": message
                },
            ]
        )
        return thread.id
    else:
        thread = client.beta.threads.create()
        return thread

def create_run(thread_id, asistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=asistant_id
    )
    return run.id

def get_run(thread_id, run_id):
    runs = client.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread_id)
    while runs.status != 'completed':
        runs = client.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread_id)
        sleep(1)
        if runs.status == 'failed':
            return runs
    else:
        message_response = client.beta.threads.messages.list(thread_id=thread_id)
        return reversed(message_response)
    
