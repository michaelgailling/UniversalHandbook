import openai

from UniversalHandbook.apikeys import open_ai_key

openai.api_key = open_ai_key


class Neuron:
    def __init__(self, system_prompt):
        # History acts as a state holder
        self.history = [{"role": "system", "content": system_prompt}]

    def add_context_prompt(self, context_message: str):
        # The context prompt is like dendrites accepting input
        self.history.append({"role": "user", "content": context_message})

    def think(self):
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history
        )

        self.history.append(resp["choices"][0]["message"])

    def __call__(self):
        # Calling behaves like an axon producing the current output state of the neuron
        return self.history[-1]
