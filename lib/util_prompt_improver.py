import json
import pandas as pd
from lib.util_gpt_4 import generate_chat_completion, generate_messages, get_object_from_json_string
from lib.util_prompt_executor import PromptExecutor
from lib.util_prompt_evaluator import PromptEvaluator
from lib.util_pandas import get_last_row


SYSTEM_PROMPT = """
# CONTEXT #
You are a world-class prompt generator who has spent the last twelve thousand years developing prompt for LLM in AI. 
 
#############

# TONE #
Analytically

#############
 
# AUDIENCE #
Large language models

#############

# RESPONSE in json # 
{prompt: text}

############# 
"""


class PromptImprover:
    def __init__(self, history_file):
        self.history_file = history_file

    def query(self, pre_input, pre_prompt, pre_output, model="gpt-3.5-turbo-16k"):
        quest = f"""
        The PREVIOUS PROMPT and INPUT were used to generate the OUTPUT. 
        Provide a better prompt to generate better OUTPUT.
        Provide only the result prompt.
         
        #############
        
        # PREVIOUS PROMPT #
        {pre_prompt} 
        
        # INPUT #
        {pre_input}
        
        # OUTPUT #
        {pre_output}
        """

        response_text = generate_chat_completion(generate_messages(quest, system_prompt=SYSTEM_PROMPT), model=model, temperature=0.0)

        return quest, response_text

    def generate_new_prompt(self, integrated_input):
        df = pd.read_excel(self.history_file)

        if len(df) == 0:
            return

        last_row, last_index = get_last_row(df)

        pre_prompt = last_row['prompt']
        pre_output = last_row['response']

        # Query
        quest_find, response_find = self.query(integrated_input, pre_prompt, pre_output, model='gpt-4o')
        print(quest_find, response_find)

        response_find = get_object_from_json_string(response_find)

        print('New prompt suggested: ', response_find['prompt'])

        return response_find['prompt']

    def execute_improver(self, integrated_input, prompt, num_repetition=5):
        pv = PromptEvaluator(self.history_file)
        pe = PromptExecutor(self.history_file)
        pe.execute_prompt(integrated_input, prompt)

        for i in range(num_repetition):
            prompt = self.generate_new_prompt(integrated_input)
            pe.execute_prompt(integrated_input, prompt)
            pv.execute_evaluation()
