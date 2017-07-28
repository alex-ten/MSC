SOURCE = 'ptb_verbs.txt'
with open('log', 'r') as file:
    start = int(file.readlines()[0])
print('STARTING FROM ITEM {}\n'.format(start+1))

def append_to(path, item):
    if type(path) is tuple:
        for p in path:
            with open(p, '+a') as file:
                file.write(item.lower()+',')
    else:
        with open(path, '+a') as file:
            file.write(item.lower() + ',')

def log_last(i):
    with open('log', 'w') as file:
        file.write(str(i))

with open(SOURCE, 'r') as file:
    all_verbs = file.readlines()
    singular, plural = all_verbs[0].split(sep=','), all_verbs[1].split(sep=',')

    to_classify = len(plural)
    for i, item in enumerate(plural[start:]):
        log_last(i + start)
        x = input('{}/{}) {} -> '.format(i + 1 + start, to_classify, item))
        if x == 't':
            path = 'POS/verb_trans.txt'
        elif x == 'i':
            path = 'POS/verb_intrans.txt'
        elif x == 'o':
            path = ('POS/verb_trans.txt','POS/verb_intrans.txt','POS/verb_opt.txt')
        elif x == '':
            path = 'POS/bin.txt'
        elif x == 'q':
            print('\nSTOPPED ON ITEM {}: \'{}\''.format(i + 1 + start, item))
            break
        else:
            continue
        append_to(path, item,)

