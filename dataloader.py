"""
This file contains operations related to data
author: Hitesh Vaidya
"""

# import libraries
import json
import os

def load(path):
    """
    load the dataset at given path

    Args:
        path (str): file path

    Returns:
        [type]: [description]
    """
    data = [json.loads(line) for line in open("data/mr/mr_politicians.json", 'r')]
    return data

def generate_name_corpus(data):
    data = load("data/mr/mr_politicians.json")
    names = generate_name_corpus(data)

    data = load("data/mr/mr_politicians.json")
    names.extend(generate_name_corpus(data))

    data = load("data/mr/mr_sportsman.json")
    names.extend(generate_name_corpus(data))

    return names

if __name__ == '__main__':
    data = load("data/mr/mr_politicians.json")
    names = generate_name_corpus(data)

    data = load("data/mr/mr_politicians.json")
    names.extend(generate_name_corpus(data))

    data = load("data/mr/mr_sportsman.json")
    names.extend(generate_name_corpus(data))

    