import os
from pathlib import Path
import json
from datetime import datetime
from lib.util_list import get_file_list


def filter_text(input_file, output_file=None):
    if not output_file:
        parsed = Path(input_file)
        tmp_dir = parsed.parent.parent / 'text-filtered'
        os.makedirs(tmp_dir, exist_ok=True)
        output_file = tmp_dir / parsed.name.lower().replace('json', 'txt')

    with open(input_file, 'r', encoding="utf8") as file:
        data = json.load(file)

    texts = []
    selected = ['title', 'body', 'heading', 'abstract']

    for item in data['paragraphs']:
        role = item['paragraph']['role']
        text = item['paragraph']['text']
        if item['paragraph']['role'] in selected:
            texts.append(role + ': ' + text)

    texts = '\n'.join(texts)

    with open(output_file, 'w', encoding="utf8") as output:
        output.write(texts)


if __name__ == '__main__':
    folder = '../../data/text'
    file_list = get_file_list(folder)

    for input_file in file_list:
        print(f"{datetime.now()} : Filter {input_file}")
        input_file = f'{folder}/{input_file}'

        filter_text(input_file)
