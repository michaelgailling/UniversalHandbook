import json
import os
import openai

from apikeys import open_ai_key

openai.api_key = open_ai_key

exit_commands = [
    "/exit",
    "/quit",
    "/kill"
]

sp_list = '''
You are the Universal Handbook generator.
You will generate a list of instructions for any skill, action, goal, or objective the user requests.
You will generate instruction specific to the users request domain.
You will generate at least 20 steps if possible, more detail is better. 
You will ignore obvious steps that would be an expected requirement for the task.
You will output the list as a JSON object in compliance with the following template.
ONLY OUTPUT JSON
DO NOT DEVIATE FROM THE TEMPLATE
{
"instructions": [
{"Objective: ": "How to..."},
{"Step 1:": "Instructions for step 1"}, 
{"Step 2:": "Instructions for step 2"}, 
{"Step 3:": "Instructions for step 3"}
]
}
DO NOT DEVIATE FROM THE TEMPLATE
ONLY OUTPUT JSON
'''



def make_initial_req(message: str):
    history = [{"role": "system", "content": sp_list},
               {"role": "user", "content": message}]

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    # print(resp)

    return resp["choices"][0]["message"]["content"]


sp_detail = '''
You are the Universal Handbook generator.
You generate detailed instructions for any skill, action, goal, or objective the user requests.
You will be provided with an objective and a step to that objective.
You will explain the step in detail using no less than a  paragraph.
You will only describe the step provided in the context of the objective.
You will not try to extrapolate other steps.
You will not try to explain things you do not understand.
You will output as a JSON object in compliance with the following template.
ONLY OUTPUT JSON
DO NOT DEVIATE FROM THE TEMPLATE
{
"objective": "Restate objective here...",
"step": "Step 1: Restate step here...",
"details": "Detailed explanation of step."
}
DO NOT DEVIATE FROM THE TEMPLATE
ONLY OUTPUT JSON
'''


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





