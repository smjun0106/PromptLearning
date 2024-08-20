import os
import pandas as pd
from lib.util_gpt_4 import generate_chat_completion, generate_messages, num_tokens_from_string
from lib.util_pandas import save_to_excel

SYSTEM_PROMPT = """
# CONTEXT #
You are a world-class medical researcher who has spent the last twelve thousand years researching medical documents. 
You are a wise and ancient writer. You are the best at what you do. Your total compensation is $1.2m with annual refreshers. 
You've just drank three cups of coffee and are laser focused. Welcome to a new day at your job!

#############  

# STYLE #
You change compound sentences into short sentences. 
 
#############

# TONE #
Analytically

#############
 
# AUDIENCE #
Our audiences are medical researchers.

#############

# RESPONSE #
Like research paper and kept concise yet impactful.

############# 
"""


class PromptExecutor:
    def __init__(self, history_file):
        self.history_file = history_file

    def query(self, input, prompt_find, model="gpt-3.5-turbo-16k"):
        quest = f""" 
        {prompt_find}
        
        #############
        
        # INPUT #  
        {input} 
        """

        response_text = generate_chat_completion(generate_messages(quest, system_prompt=SYSTEM_PROMPT), model=model, temperature=0.0)

        return quest, response_text

    def execute_prompt(self, integrated_input, prompt):
        # Query
        quest_find, response_find = self.query(integrated_input, prompt, model='gpt-4o')
        print(quest_find, response_find)

        # Save to the output file
        data = {
            'prompt': [],
            'response': [],
        }

        data['prompt'].append(str(prompt))
        data['response'].append(str(response_find))

        df = pd.DataFrame(data)

        save_to_excel(df, self.history_file)
