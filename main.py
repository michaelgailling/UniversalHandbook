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
        break

    return resp["choices"][0]["message"]["content"]


def get_step_detail(resp_dict: dict):
    objective = resp_dict["instructions"][0]

    for i in range(1, len(resp_dict["instructions"])):
        step: dict = resp_dict["instructions"][i]

        step_n = list(step.keys())
        step_n = step_n[0]
        step_d = step[step_n]

        print(make_detail_req(objective=objective, step_n=step_n, step_d=step_d))


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
        break

    return resp["choices"][0]["message"]["content"]


while True:
    resp_dict = input_to_list()

    print(get_step_detail(resp_dict))




