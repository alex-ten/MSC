from PDPATH import PDPATH
import reader as rd
from random import randint
import nltk
import collections
import pickle

class Vocab(object):
    def __init__(self, s2id, end_of_sequence='<eos>', unknown_string = '<unk>'):
        self.eos = end_of_sequence
        self.unk = unknown_string
        self.s2id = s2id
        self.id2s = {}
        for k,v in s2id.items():
            self.id2s[v[0]] = k

        if not self.unk in list(self.s2id.keys()):
            unk_id = max(list(self.id2s.keys())) + 1
            self.s2id[self.unk] = unk_id
            self.id2s[unk_id] = self.unk

    def getid(self, s):
        try:
            return self.s2id[s][0]
        except KeyError:
            try:
                return self.s2id[self.unk][0]
            except KeyError:
                return

    def getfreq(self, s_or_id, v=False):
        try:
            return self.s2id[s_or_id][1]
        except KeyError:
            try:
                return self.s2id[self.id2s[s_or_id]][1]
            except KeyError:
                try:
                    if v: print('{} was not found in the vocab, returning <unk> frequency'.format(s_or_id))
                    return self.s2id[self.unk][1]
                except KeyError:
                    return

    def getpos(self, s_or_id, v=False):
        try:
            return self.s2id[s_or_id][2]
        except KeyError:
            try:
                return self.s2id[self.id2s[s_or_id]][2]
            except KeyError:
                try:
                    if v: print('{} was not found in the vocab, returning <unk> POS'.format(s_or_id))
                    return self.s2id[self.unk][2]
                except KeyError:
                    return

    def gets(self, id):
        try:
            return self.id2s[id]
        except KeyError:
            print('ID {} is not in vocab'.format(id))


#
# print(end='\n\n\n')
# file = PDPATH('/train_data/ptb_word_data/test.txt')
#
# print('STEP 1. Convert raw corpus into a long list:')
# ALLSENTS = rd._read_words(file)
# i = randint(0, len(ALLSENTS)-20)
# sample = '...'
# for w in ALLSENTS[i:i+20]:
#     sample += ' ' + w
# sample += ' ...'
# print('  * A list of words of length {}'.format(len(ALLSENTS)))
# print('  * Here\'s a random sample of 120 items: "{}"'.format(sample))
#
# # print('\nSTEP 2. Build vocab (assign strings to IDs):')
# # vocab = rd._build_vocab(file)
# # print('  * Vocab has {} items'.format(len(vocab)))
# #
# # print('\nSTEP 3. Sort unique words (types) by frequency or alphabetically:')
# # uniques = rd._build_vocab(file, True)
# # n = len(uniques)
# # for i, w in enumerate(uniques[0:8]):print('  {}) {}'.format(i+1, w))
# # print('  ...\n')
# # for i, w in enumerate(uniques[n-3:]):print('  {}) {}'.format(i+n-2, w))
#
# print('\nSTEP 2. Tag items in the long list by POS:')
# ptb_sents = nltk.corpus.treebank.tagged_sents(tagset='universal')
# uni_tag = nltk.UnigramTagger(ptb_sents)
# tagged = uni_tag.tag(ALLSENTS)
# ALLTAGS = [x[1] for x in tagged]
#
# tally_word_tokens = collections.Counter(ALLSENTS)
# tally_pos_tokens =  collections.Counter(ALLTAGS)
#
# word_to_id_freq_pos = {}
# for k, v in word_to_id.items():
#     word_to_id_freq_pos[k] = (v, counter_words[k], uni_tag.tag([k]))


# MAINs
# ============================

def vocab_demo():
    v = rd.get_vocab('ptb.voc')
    items = ['the', 'dog', 'dogs', 'boy', 'boys', 'is','are','has','have','was','were']
    for i in items:
        print(i, v.getid(i))


def tag_corpus():
    file = PDPATH('/train_data/ptb_word_data/train.txt')
    s2id = rd._build_big_vocab(file)
    V = Vocab(s2id)
    tags = 'JJ'
    words_by_tags = dict(zip(tags, [[] for i in range(len(tags))]))
    adjectives = []

    for k, (id, f, pos) in s2id.items():
        if pos == tags:
            adjectives.append(k)
            with open('ptb_adjs', mode='+a') as f:
                f.write(','+k)
    print(len(adjectives))


if __name__=='__main__': tag_corpus()