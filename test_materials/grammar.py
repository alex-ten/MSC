import os
from random import randint

def voc(path):
    return os.getcwd()+'/'+path


# Parts of speech
# ============================
class POS(object):
    # BaseClass for a part of speech (e.g. nouns, verbs, pronouns, etc.)
    def __init__(self, vocab, name):
        self.vocab = vocab
        self.name = name
        self.feature = None

    def express(self):
        tokens = []
        with open(self.vocab, 'r') as file:
            if self.feature is None:
                for line in file.readlines():
                    tokens += [token for token in line.strip('\n').split(',')]
            else:
                line = file.readlines()[self.feature]
                tokens = line.strip('\n').split(',')
        return tokens[randint(0, len(tokens) - 1)]


class Det(POS):
    def __init__(self, vocab, name, id=None):
        super().__init__(vocab, name)
        self.id = id


class Noun(POS):
    def __init__(self, vocab, name, gnum=None):
        super().__init__(vocab, name)
        self.feature = gnum


class Verb(POS):
    def __init__(self, vocab, name, gnum=None, argstr=None):
        super().__init__(vocab, name)
        self.feature = gnum
        self.argstr = argstr


# Phrases
# ============================
class Phrase(object):
    def __init__(self, *args):
        self.structure = list(args)
        self.expression = None

    def express(self):
        phrase = ''
        for i in self.structure:
            phrase = phrase + ' ' + i.express()
        self.expression = phrase[1:]
        return self.expression

class PP(Phrase):
    def __init__(self, P, NP):
        super().__init__(P, NP)
        self.N = NP
        self.P = P
        self.structure = [P, NP]


class NP(Phrase):
    def __init__(self, det, N):
        super().__init__(det, N)
        self.det = det
        self.N = N
        self.gnum = N.feature

    def add_adj(self, A):
        i = self.structure.index(self.N)
        self.structure.insert(i, A)
        return self

    def add_PP(self,PP):
        i = self.structure.index(self.N) + 1
        for j,w in enumerate(PP.structure):
            self.structure.insert(i+j, w)
        return self

class VP(Phrase):
    def __init__(self, V, NP):
        super().__init__(V, NP)
        self.V = V
        self.NP = NP
        self.structure = [self.V, self.NP]


class RC(Phrase):
    def __init__(self, PN, V, NP):
        super().__init__(V, NP)
        self.PN = PN
        self.V = V
        self.NP = NP
        if V.argstr == 1:
            self.structure = [self.PN, self.V, self.NP]
        elif V.argstr == 2:
            i = randint(0,1)
            self.structure = [self.PN, self.V, self.NP][0:3-i]
        else:
            self.V.gnum = self.NP.gnum
            self.structure = [self.PN, self.NP, self.V,]


# Sentences
# ============================
class SimpleSentence(object):
    def __init__(self, NP, VP):
        self.NP = NP
        self.VP = VP
        self.structure = [NP, VP]

    def add_RC(self,RC):
        i = self.structure.index(self.NP)
        self.structure.insert(i+1, RC)
        return self

    def express(self):
        s = ''
        for phrase in self.structure:
            s = s + ' ' + phrase.express()
        self.expression = s[1:]
        return self.expression


# MAINs
# ============================
def main():
    det  = Det(voc('det.txt'), 'det')
    prep = POS(voc('prep.txt'), 'prep')
    A    = POS(voc('adj.txt'), 'adj')


    NP0 = NP(det = det,
             N = Noun(voc('noun_anim.txt'), 'noun', gnum=1))
    VP1 = VP(Verb(voc('verb_dor.txt'), 'verb', gnum=1),
             NP0)
    PP_ = PP(P = prep,
             NP = NP(
                 det = det,
                 N = Noun(voc('noun_anim.txt'), 'noun', gnum=1)))

    SS = SimpleSentence(NP0, VP1).add_RC(
        RC = RC(
            PN = POS(voc('pron.txt'), 'pronoun'),
            V = Verb(voc('verb_dor.txt'), 'verb', gnum=1, argstr=1),
            NP = NP0
        )
    )

    for i in range(10):
       print(SS.express())

if __name__=='__main__': main()
