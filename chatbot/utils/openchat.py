import base64
import re
from time import sleep
from config.settings import OPENAI_KEY
from openai.types.beta.threads import MessageContentImageFile
from openai import OpenAI

class ChatBotAI:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_KEY)
        self.asistant_id = "asst_5pJN9YC3RfFT7CmETflEzAaI"
        self.instructions = "Answering any programming questions and thoroughly reviewing problems and providing solutions and recommendations to make the code work more optimally and efficiently."
        self.assistant_title = "Rozievich AI"

    def create_thread(self, content, file=None):
        messages = [
            {
                "role": "user",
                "content": content,
            }
        ]
        if file is not None:
            messages[0].update({"file_ids": [file.id]})
        thread = self.client.beta.threads.create(messages=messages)
        return thread
    
    def create_message(self, thread, content, file=None):
        file_ids = []
        if file is not None:
            file_ids.append(file.id)
        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=content, file_ids=file_ids
        )
    
    def create_run(self, thread):
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=self.assistant_id, instructions=self.instructions
        )
        return run

    def create_file_link(self, file_name, file_id):
        content = self.client.files.content(file_id)
        content_type = content.response.headers["content-type"]
        b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
        link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
        return link_tag
    
    def get_message_value_list(self, messages):
        messages_value_list = []
        for message in messages:
            message_content = ""
            if not isinstance(message, MessageContentImageFile):
                message_content = message.content[0].text
                annotations = message_content.annotations
            else:
                image_file = self.client.files.retrieve(message.file_id)
                messages_value_list.append(
                    f"Click <here> to download {image_file.filename}"
                )
            citations = []
            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(
                    annotation.text, f" [{index}]"
                )

                if file_citation := getattr(annotation, "file_citation", None):
                    cited_file = self.client.files.retrieve(file_citation.file_id)
                    citations.append(
                        f"[{index}] {file_citation.quote} from {cited_file.filename}"
                    )
                elif file_path := getattr(annotation, "file_path", None):
                    link_tag = self.create_file_link(
                        annotation.text.split("/")[-1], file_path.file_id
                    )
                    message_content.value = re.sub(
                        r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_content.value
                    )

            message_content.value += "\n" + "\n".join(citations)
            messages_value_list.append(message_content.value)
            return messages_value_list
    
    def get_message_list(self, thread, run):
        completed = False
        while not completed:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print("run.status:", run.status)
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            print("messages:", "\n".join(self.get_message_value_list(messages)))
            if run.status == "completed":
                completed = True
            elif run.status == "failed":
                break
            else:
                sleep(1)

        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        return self.get_message_value_list(messages)
    
