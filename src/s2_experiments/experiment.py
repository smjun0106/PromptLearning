import os
from datetime import datetime
from lib.util_list import get_file_list
from lib.util_prompt_improver import PromptImprover
import pandas as pd
from src.configs import disease, method


def integrate_contents(input_file, integrated):
    df = pd.read_csv(input_file)

    if len(df) == 0:
        return

    prompt = df.iloc[0]['prompt']
    response = df.iloc[0]['response']

    print(input_file)
    print(response)

    integrated.append(response)


if __name__ == '__main__':
    # Prepare inputs
    folder = '../../data/text-searched'
    file_list = get_file_list(folder)

    integrated_input = []
    for input_file in file_list:
        print(f"{datetime.now()} : Get contents in {input_file}")
        input_file = f'{folder}/{input_file}'

        integrate_contents(input_file, integrated_input)

    integrated_input = ''.join(integrated_input)

    # Define the initial prompt
    topics = f'{", ".join(method)} in {", ".join(disease)}'
    prompt = f'List all topics {topics} in the Input.'

    # Prepare an output file
    tmp_dir = '../../data/prompt-history'
    os.makedirs(tmp_dir, exist_ok=True)
    history_file = tmp_dir + f'/prompt_history_experiment_{str(datetime.now().strftime("%Y-%m-%d_%H-%M"))}.xlsx'

    if os.path.exists(history_file):
        os.remove(history_file)

    # Run Prompt Improver
    pe = PromptImprover(history_file)
    pe.execute_improver(integrated_input, prompt, 10)

