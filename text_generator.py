from nltk.tokenize import regexp_tokenize
from nltk.util import trigrams
from random import choice
from random import choices
import string

file_name = 'corpus.txt'
data_file = open(file_name, 'r', encoding='utf-8')

data_list = regexp_tokenize(data_file.read(), r'[\S]+')

trgrms = list(trigrams(data_list))


def condition_checker(input_word):
    return any(['.' in input_word, '!' in input_word, '?' in input_word])


# FINDING THE MOST PROBABLE TAIL
def common_dict(heads):
    tails_dict = {}
    for triple in trgrms:
        if heads[0] == triple[0] and heads[1] == triple[1]:
            tails_dict.setdefault(triple[2], 0)
            tails_dict[triple[2]] += 1
    return tails_dict


def sentence_maker(heads):
    output = []
    next_couple = list(heads)
    while True:
        if not condition_checker(next_couple[0]) and not condition_checker(next_couple[1]):
            dict_tail = common_dict(next_couple)
            tail = choices(list(dict_tail.keys()), list(dict_tail.values()))[0]
            if (next_couple[0], next_couple[1], tail) in trgrms:
                output.append(next_couple[0])
            next_couple = [next_couple[1], tail]
        elif condition_checker(next_couple[0]):
            return sentence_maker(
                choice([triples[:2] for triples in trgrms if triples[0][0] in string.ascii_uppercase]))
        elif condition_checker(next_couple[1]) and len(output) < 5:
            return sentence_maker(
                choice([triples[:2] for triples in trgrms if triples[0][0] in string.ascii_uppercase]))
        elif condition_checker(next_couple[1]) and len(output) >= 5:
            output.append(next_couple[0])
            output.append(next_couple[1])
            return ' '.join(output)


text = []
for j in range(10):
    text.append(sentence_maker(choice([triples[:2] for triples in trgrms if triples[0][0] in string.ascii_uppercase])))

print('\n'.join(text))
