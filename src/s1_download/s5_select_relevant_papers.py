from lib.util_gpt_4 import generate_chat_completion, generate_messages
import os
from pathlib import Path
from datetime import datetime
from lib.util_list import get_file_list
import pandas as pd
from src.configs import disease, method

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



def query(input, prompt_find, model="gpt-3.5-turbo-16k"):
    quest = f"""

{prompt_find}

#############

# INPUT #  
{input} 
"""

    response_text = generate_chat_completion(generate_messages(quest, system_prompt=SYSTEM_PROMPT), model=model, temperature=0.0)

    return quest, response_text


def select_relevant_papers(input_file, output_file=None):
    if not output_file:
        parsed = Path(input_file)
        tmp_dir = parsed.parent.parent / 'text-searched'
        os.makedirs(tmp_dir, exist_ok=True)
        output_file = tmp_dir / parsed.name.lower().replace('txt', 'csv')

    data = {
        'prompt': [],
        'response': [],
    }

    with open(input_file, 'r', encoding="utf8") as file:
        input = file.read()

        # S1. Check whether the paper is in the target topics
        topics = f'{", ".join(method)} in {", ".join(disease)}'

        prompt_check = f'check whether the Input include the topics {topics}. If it is, then say Yes. If not say No.'

        quest_check, response_check = query(input, prompt_check, model='gpt-4-turbo')
        print(response_check)

        # S2. Find contents
        if 'yes' in response_check.lower():
            prompt_find = f'Extract all contents for a reader.\nDo not include your assumption and explanation.'

            quest_find, response_find = query(input, prompt_find, model='gpt-4o')

            print(quest_find, response_find)

            data['prompt'].append(str(prompt_find))
            data['response'].append(str(response_find))

    df = pd.DataFrame(data)

    if len(df) != 0:
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file))


if __name__ == '__main__':
    folder = '../../data/text-filtered'
    file_list = get_file_list(folder)

    for input_file in file_list:
        print(f"{datetime.now()} : Find contents in {input_file}")
        input_file = f'{folder}/{input_file}'

        select_relevant_papers(input_file)
