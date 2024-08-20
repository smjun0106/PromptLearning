import os
import pandas as pd
from lib.util_gpt_4 import generate_chat_completion, generate_messages, get_object_from_json_string
from lib.util_pandas import save_to_excel
from lib.util_pandas import get_last_row, add_item_with_new_column

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

# RESPONSE in json# 
{ 
    Last_Output: {Score: value, Rational: text}, 
    Current_Output: {Score: value, Rational: text}
}


############# 
"""


class PromptEvaluator:
    def __init__(self, history_file):
        self.history_file = history_file

    def query(self, last_output, cur_output, last_score, model="gpt-3.5-turbo-16k"):
        if last_score:
            quest = f"""
            Compare the Last Output and the Current Output. 
            Score the current Output on a scale from 0 to 100 by comparing to the the Last Output with the Last Output Score.
            Include the rational for scoring. 
              
            #############
            
            # Last Output #
            {last_output} 
              
            # Last Output Score #
            {last_score}
            
            # Current Output #
            {cur_output}  
            """
        else:
            quest = f"""
            Compare the Last Output and the Current Output. 
            Score both on a scale from 0 to 100.
            Include the rational for scoring. 
              
            #############
            
            # Last Output #
            {last_output} 
            
            # Current Output #
            {cur_output} 
            """

        response_text = generate_chat_completion(generate_messages(quest, system_prompt=SYSTEM_PROMPT), model=model, temperature=0.0)

        return quest, response_text

    def execute_evaluation(self):
        """
        :return:    True if the current output is better than the last output
        """
        df = pd.read_excel(self.history_file, engine='openpyxl')

        if len(df) == 0:
            return

        last_row, last_index = get_last_row(df, reverse_index=-2)
        cur_row, cur_index = get_last_row(df)

        last_prompt = last_row['prompt']
        last_output = last_row['response']
        last_score = last_row['score'] if 'score' in last_row else None

        cur_prompt = cur_row['prompt']
        cur_output = cur_row['response']
        cur_score = cur_row['score'] if 'score' in cur_row else None

        # Query
        quest, response = self.query(last_output, cur_output, last_score, model='gpt-4o')
        print(quest, response)

        response_object = get_object_from_json_string(response)
        last_output = response_object['Last_Output']
        current_output = response_object['Current_Output']

        print('Last_Output_Score: ', last_output)
        print('Current_Output_Score: ', current_output)

        add_item_with_new_column(df, last_output['Score'], last_index, 'score')
        add_item_with_new_column(df, current_output['Score'], cur_index, 'score')
        add_item_with_new_column(df, response, cur_index, 'reason')

        save_to_excel(df, self.history_file, replace=True)

        return last_output['Score'] <= current_output['Score']


"""
    Test
"""
# pv = PromptEvaluator('../data/prompt-history/prompt_history.xlsx')
# print(pv.execute_evaluation())
