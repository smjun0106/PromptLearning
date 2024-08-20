import subprocess
import os
from pathlib import Path
import json
from datetime import datetime
from lib.util_list import get_file_list


def load_pdf(input_file, output_file=None):
    print(f"{datetime.now()} : pdfact STARTED")

    if not output_file:
        parsed = Path(input_file)
        tmp_dir = parsed.parent.parent / 'text'
        os.makedirs(tmp_dir, exist_ok=True)
        output_file = tmp_dir / parsed.name.lower().replace('pdf', 'json')

    pdfact_path = Path(__file__).resolve().parent.parent.parent / "lib/bin/pdfact/pdfact.jar"

    roles = '--include-roles figure,appendix,keywords,heading,page-header,footer,acknowledgments,caption,toc,abstract,footnote,body,itemize-item,title,reference,affiliation,general-terms,formula,categories,table,authors'
    cmd = f"java -jar {pdfact_path} --format json {roles} {input_file} {output_file}"

    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"{datetime.now()} : ERR => {e}")
        return

    print(f"{datetime.now()} : pdfact ENDED")

    with open(output_file, 'r', encoding="utf8") as file:
        doc = json.load(file)


if __name__ == '__main__':
    folder = '../../data/downloaded_pdfs'
    file_list = get_file_list(folder)

    for input_file in file_list:
        print(f"{datetime.now()} : Convert {input_file}")
        input_file = f'{folder}/{input_file}'

        load_pdf(input_file)
