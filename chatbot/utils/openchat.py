import os
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
    return response

