import json
import os
import openai

from UniversalHandbook.prompts.system_prompts import sp_list, sp_detail
from apikeys import open_ai_key

openai.api_key = open_ai_key

exit_commands = [
    "/exit",
    "/quit",
    "/kill"
]


def make_initial_req(message: str):
    history = [{"role": "system", "content": sp_list},
               {"role": "user", "content": message}]

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    # print(resp)

    return resp["choices"][0]["message"]["content"]


def make_detail_req(objective: str, step_n: str, step_d: str):
    prompt = f"Objective: {objective}\n {step_n}{step_d}"

    history = [{"role": "system", "content": sp_detail},
               {"role": "user", "content": prompt}]

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    return resp["choices"][0]["message"]["content"]


resp_dict = {}

while True:
    usr_inp = input("Prompt: ")

    lower_inp = usr_inp.lower()

    if lower_inp in exit_commands:
        exit()

    if not usr_inp:
        print("Empty prompts are skipped.")

    resp = make_initial_req(usr_inp)

    print(resp)

    try:
        resp_dict = json.loads(resp)
    except:
        print("Something went wrong!")
        continue

    break

n = len(resp_dict["instructions"])

objective = resp_dict["instructions"][0]

for i in range(1, n):
    step: dict = resp_dict["instructions"][i]

    step_n = list(step.keys())
    step_n = step_n[0]
    step_d = step[step_n]

    print(make_detail_req(objective=objective, step_n=step_n, step_d=step_d))
