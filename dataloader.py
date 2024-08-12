"""
This file contains operations related to data
author: Hitesh Vaidya
"""

# import libraries
import json
import os
import torch
import matplotlib.pyplot as plt

def load(path):
    """
    load the dataset at given path

    Args:
        path (str): file path

    Returns:
        [type]: [description]
    """
    names = []
    print("path: ", path)
    data = [json.loads(line) for line in open(path, 'r')]
    for obj in data:
        names.extend(obj['title'].split(' '))

    return names


def generate_name_corpus():
    names = []

    # load names of politicians
    names.extend(load("data/mr/mr_politicians.json"))

    # names of writers
    names.extend(load("data/mr/mr_writers.json"))

    # names of sportsmen
    names.extend(load("data/mr/mr_sportsman.json"))

    # eliminate duplicates
    names = list(set(names))

    return names  

def bigrams(data):
    bigrams = {}

    # characters in the dataset
    # sorted list of characters in the dataset
    chars = sorted(list(set(''.join(data))))

    # create a lookup table from char to int
    stoi = {s:i for i,s in enumerate(chars)}
    stoi['<S>'] = len(chars)
    stoi['<E>'] = len(chars) + 1

    # Maintain a matrix of [characters x characters] storing number of times a character in column follows the character in a row
    N = torch.zeros((len(stoi), len(stoi)), dtype=torch.int32)

    # go through each word and create a pair of every occurence of 2 characters in the dataset
    # make a dictionary that stores the count of number of times two characters occur in a particular order
    # ex: "hitesh" - ('h','i'), ('i', 't'), ...
    for word in data:
        # Add start and end character token
        chs = ['<S>'] + list(word) + ['<E>']
        for ch1, ch2 in zip(chs, chs[1:]):
            # Get the integer corresponding to the character
            ix1 = stoi[ch1]
            ix2 = stoi[ch2]
            # Since ch2 follows ch1, increment the corresponding count in N by 1
            N[ix1, ix2] += 1
            bigram = (ch1, ch2)
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
    
    # sort the bigrams in the descending order of number of times they occur in a particular order
    # ex. {('h','i'):3 , ('i', 't'): 1, ...}
    bigrams = sorted(bigrams.items(), key=lambda kv: -kv[1])

    itos = {v:k for k,v in stoi.items()}

    return N, bigrams, stoi, itos
    
def draw_bigram_matrix(N, itos):
    plt.figure(figsize=(32, 32))
    plt.imshow(N, cmap='Blues')
    for i in range(len(N)):
        for j in range(len(N)):
            chstr = itos[i] + itos[j]
            plt.text(j, i, chstr, ha='center', va='bottom', color='gray')
            plt.text(j, i, N[i, j].item(), ha='center', va='top', color='gray')
    plt.axis('off')

if __name__ == '__main__':
    names = generate_name_corpus()
    print("length of corpus: ", len(names))
    N, bigrams, stoi, itos = bigrams(names)
    draw_bigram_matrix(N, itos)
