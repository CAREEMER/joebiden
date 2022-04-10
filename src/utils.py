import os


def get_arts() -> list[str]:
    arts_directory = os.path.join(os.getcwd(), "arts")
    arts = []

    for file_name in os.listdir(arts_directory):
        if not file_name.endswith(".txt"):
            continue
        with open(os.path.join(arts_directory, file_name)) as file:
            arts.append(file.read())

    return arts


def get_pics() -> list[str]:
    arts_directory = os.path.join(os.getcwd(), "arts")
    arts = []

    for file_name in os.listdir(arts_directory):
        if file_name.endswith(".txt"):
            continue
        arts.append(os.path.join("arts", file_name))

    print(arts)
    return arts