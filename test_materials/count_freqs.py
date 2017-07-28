import matplotlib.pyplot as plt
import pickle
import random
import PDPATH
import reader as rd

with open('POS/noun_anim.txt', 'r') as file:
    all = file.readlines()
    aNs = all[0][:-2].split(sep=',')
    aNp = all[1].split(sep=',')

with open('POS/noun_inanim.txt', 'r') as file:
    all = file.readlines()
    iNs = all[0][:-2].split(sep=',')
    iNp = all[1].split(sep=',')

with open('POS/verb_trans.txt', 'r') as file:
    all = file.readlines()
    tVs = all[0][:-2].split(sep=',')
    tVp = all[1].split(sep=',')

with open('POS/verb_intrans.txt', 'r') as file:
    all = file.readlines()
    iVs = all[0][:-2].split(sep=',')
    iVp = all[1].split(sep=',')

with open('ptb_adjs.txt', 'r') as file:
    A = file.readline().split(sep=',')


sample = random.randint(20,50)
print('Here are some singular samples:')
print('  Anim: {}\n  Inanim: {}\n  Trans: {}\n  Intrans: {}\n  Adj: {}\n'.format(aNs[sample], iNs[sample], tVs[sample], iVs[sample], A[sample]))
print('And ere are some plural samples:')
print('  Anim: {}\n  Inanim: {}\n  Trans: {}\n  Intrans: {}\n  Adj: {}\n'.format(aNp[sample], iNp[sample], tVp[sample], iVp[sample], A[sample+1]))

V = rd.get_vocab('big_ptb.voc')
