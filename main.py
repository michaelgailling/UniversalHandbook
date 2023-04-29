import json
import os
import openai
import time


from UniversalHandbook.prompts.system_prompts import sp_list, sp_detail
from apikeys import open_ai_key

openai.api_key = open_ai_key

exit_commands = [
    "/exit",
    "/quit",
    "/kill"
]

affirmative_words = [
    "affirmative",
    "sure",
    "ok",
    "yeah",
    "yea",
    "yes",
    "ye",
    "y"

]

def input_to_list():
    while True:
        print('Phrase your prompt like a "how to..." book, or a "...for dummies" book.')
        usr_inp = input("Prompt: ")

        lower_inp = usr_inp.lower()

        if lower_inp in exit_commands:
            exit()

        if not usr_inp:
            print("Empty prompts are skipped.")
            continue

        resp_dict = get_summary_list(usr_inp)
        break
    return resp_dict


def get_summary_list(usr_inp: str):
    resp_dict = {}
    while True:
        resp = make_list_req(usr_inp)

        print(resp)

        try:
            resp_dict = json.loads(resp)
        except:
            print("GPT returned poorly formatted JSON.")
            time.sleep(1)
            continue
        break
    return resp_dict


def make_list_req(message: str):
    history = [{"role": "system", "content": sp_list},
               {"role": "user", "content": message}]

    while True:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history
            )
        except:
            print("OpenAI had a problem.")
            time.sleep(1)
            continue
        return resp["choices"][0]["message"]["content"]


def get_step_details(resp_dict: dict):
    objective = resp_dict["instructions"][0]

    full_handbook = []

    for i in range(1, len(resp_dict["instructions"])):
        step: dict = resp_dict["instructions"][i]

        step_n = list(step.keys())
        step_n = step_n[0]
        step_d = step[step_n]

        details = make_detail_req(objective=objective, step_n=step_n, step_d=step_d)
        print(details)
        full_handbook.append(details)
    return full_handbook


def make_detail_req(objective: str, step_n: str, step_d: str):
    prompt = f"Objective: {objective}\n {step_n}{step_d}"

    history = [{"role": "system", "content": sp_detail},
               {"role": "user", "content": prompt}]
    while True:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history
            )
        except:
            print("OpenAI had a problem.")
            time.sleep(1)
            continue
        return resp["choices"][0]["message"]["content"]

def save_handbook(handbook: list):
    while True:
        usr_inp = input("Would you like to save this handbook?: ")

        if not usr_inp:
            print("Empty prompts are skipped.")
            continue

        lower_inp = usr_inp.lower()

        if lower_inp in exit_commands:
            exit()

        if lower_inp in affirmative_words:
            while True:
                filename = input("Filename: ")
                if filename:
                    break
                print("Invalid filename!")

            write_file(handbook, filename)
            break
        else:
            break


def write_file(handbook: list, filename: str):
    handbook_str = ""

    for step in handbook:
        handbook_str = f"{handbook_str}\n{step}"

    with open(f"./handbooks/{filename}.txt", 'w') as f:
        f.write(handbook_str)

while True:
    list_of_steps = input_to_list()

    full_handbook = get_step_details(list_of_steps)

    save_handbook(full_handbook)






