import os


def get_arts() -> list[str]:
    arts_directory = os.path.join(os.getcwd(), "arts")
    arts = []

    for file_name in os.listdir(arts_directory):
        with open(os.path.join(arts_directory, file_name)) as file:
            arts.append(file.read())

    return arts
