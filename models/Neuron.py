from datetime import time

import openai

from UniversalHandbook.apikeys import open_ai_key

openai.api_key = open_ai_key

# Premise behind Neuron object:
# The neuron object is modeled upon a biological neuron.
# Tokens on their own do not have the complexity to represent neurons.
# Groups of tokens can be an appropriate analog for neuro-transmitters.
# Tokens are collected through the context prompt till and activation threshold is reached.
# Then GPT is forced to think about what it sees and produce a response.
# That response is then forwarded to other neurons which repeat the process.


class Neuron:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        # History acts as a state holder
        self.history = [{"role": "system", "content": system_prompt}]

    def add_context_prompt(self, context_message: str):
        # The context prompt is like dendrites accepting input
        self.history.append({"role": "user", "content": context_message})

    def think(self):
        while True:
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.history
                )
            except:
                print("OpenAI had a problem.")
                time.sleep(1)
                continue
            break

        return resp["choices"][0]["message"]

    def __call__(self):
        # Calling behaves like an axon producing the current output state of the neuron
        if len(self.history) >= 2:
            thought = self.think()
            # Clear the history and load default system prompt
            self.history = [{"role": "system", "content": self.system_prompt}]
            return thought
        return None

