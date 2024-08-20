import os


def get_file_list(folder_path):
    folder_path = os.path.abspath(folder_path)

    files = []

    for entry in os.listdir(folder_path):
        entry_path = os.path.join(folder_path, entry)

        if os.path.isfile(entry_path):
            files.append(entry)

    return files
