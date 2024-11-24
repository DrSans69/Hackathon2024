import os
import openai
from pathlib import Path
import re
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    frontend_url: str

    class Config:
        env_file = ".env"


settings = Settings()
openai.api_key = settings.api_key
completion = openai.chat


def get_html_from_str(string: str):
    pattern = r"<!DOCTYPE html>.*?</html>"
    match = re.search(pattern, string, re.DOTALL)
    modified_string = re.sub(pattern, "", string, flags=re.DOTALL)
    html_document = match.group(0)
    return (modified_string, html_document)


def document_type(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You need to determine what the topic is in the given HTML document"""},
            {"role": "assistant", "content":  "The topic is an email"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def topics(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Determine the overral document structure simmiliar to the given document"""},
            {"role": "assistant", "content":  "The "},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def analyze(prompt, standart, history: list):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You are a helpful assistant who needs to analyze and validate documents given
            documents against this standard: {standart} of user's organisation and general look of documents of such types. You
            need to recommend autofill suggestions for
            incomplete sections is they are present, and if there is some  historical data: {history}, base it on it. Give the user's document overall score out of 10.
            Print your recommendations, suggest what other things the user may add based on the topic and type of the document."""},
            {"role": "assistant", "content":  """The provided document is a ... It's overlall score is: 10/10. Recommendations for Autofill Suggestions: ..."""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content


def human_correction(prompt, answer, text, history):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You have to modify the original document {text}
             based on the points the user wants to modify. All the available
             points are here: {answer}. Take into account
             history of prompts and answers: {history}. Print the whole modified document as an answer"""},
            # {"role" : "assistant", "content" :  """<"""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content
