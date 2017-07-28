import os
from random import randint

def voc(path):
    return os.getcwd()+'/'+path


class Word(object):
    def __init__(self, str):
        self.str = str

    def express(self):
        return self.str


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
    def __init__(self, vocab, name='det', id=None):
        super().__init__(vocab, name)
        self.id = id


class Noun(POS):
    def __init__(self, vocab, gnum=None):
        super().__init__(vocab, name='noun')
        self.feature = gnum


class Verb(POS):
    def __init__(self, vocab, gnum=None, argstr=None):
        super().__init__(vocab, name='verb')
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


class PrepP(Phrase):
    def __init__(self, P, NP):
        super().__init__(P, NP)
        self.N = NP
        self.P = P
        self.structure = [P, NP]


class NounP(Phrase):
    def __init__(self, det, N, A = None, PP = None, RC = None):
        self.det = det
        self.N = N
        self.A = A
        self.PP = PP
        self.RC = RC
        super().__init__(self.det, self.N)
        self.gnum = N.feature
        if A is not None:
            self._add_adj(A)
        if PP is not None:
            self._add_PrepP(PP)
        if RC is not None:
            self._add_RelC(RC)

    def _add_adj(self, A):
        i = self.structure.index(self.N)
        self.structure.insert(i, A)

    def _add_PrepP(self, PP):
        self.PP = PP
        i = self.structure.index(self.N) + 1
        self.structure.insert(i + 1, self.PP)
        return self

    def _add_RelC(self, RC):
        self.RC = RC
        if self.PP is None:
            i = self.structure.index(self.N) + 1
        else:
            i = self.structure.index(self.PP) + 1
        self.structure.insert(i + 1, self.RC)

    def with_adj(self, A):
        return NounP(self.det, self.N, A=A, PP=self.PP, RC=self.RC)

    def with_PrepP(self, PP):
        return NounP(self.det, self.N, A = self.A, PP=PP, RC=self.RC)

    def with_RelC(self, RC):
        return NounP(self.det, self.N, A = self.A, PP=self.PP, RC=RC)


class VerbP(Phrase):
    def __init__(self, V, NP=None):
        self.V = V
        self.NP = NP
        if self.NP is None:
            super().__init__(self.V)
        else:
            super().__init__(self.V, self.NP)


class RelC(Phrase):
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
class Sentence(object):
    def __init__(self, NP, VP):
        self.NP = NP
        self.VP = VP
        self.structure = [NP, VP]

    def express(self):
        s = ''
        for phrase in self.structure:
            s = s + ' ' + phrase.express()
        self.expression = s[1:]
        return self.expression


# MAINs
# ============================
def main():
    anim  = voc('POS/noun_anim.txt')
    inanim = voc('POS/noun_inanim.txt')
    trans  = voc('POS/verb_trans.txt')
    intrans  = voc('POS/verb_intrans.txt')
    # opt = voc('POS/verb_opt.txt')

    det  = Det(voc('POS/det.txt'))
    prep = POS(voc('POS/prep.txt'), 'prep')
    pron = POS(voc('POS/pron.txt'), 'prop')
    A    = POS(voc('POS/adj.txt'), 'adj')

    snn = svn = 0   # head noun number and its verb number must agree
    ppnn = 0        # prepositional phrase noun number
    rcnn = rcvn = 1 # relative clause noun number and its verb number must agree
    subrcnn = subrcvn = 0 #subrelative clause noun number and its verb number must agree


    aNP = NounP(det = det, N = Noun(anim, gnum=snn))
    iNP = NounP(det = det, N = Noun(inanim, gnum=snn))

    iVP = VerbP(Verb(intrans, gnum=svn))
    tVP_w_iNP = VerbP(Verb(trans, gnum=svn), NounP(det = det, N = Noun(inanim, gnum=rcnn)))

    PP  = PrepP(P = prep, NP = NounP(det = det, N = Noun(inanim, gnum=ppnn)))
    RC1 = Phrase(pron, VerbP(Verb(intrans, gnum=svn)))
    RC2 = Phrase(pron, VerbP(Verb(trans, gnum=svn), NounP(det = det, N = Noun(inanim, gnum=rcnn))))
    RC3 = Phrase(pron, NounP(det = det, N = Noun(anim, gnum=rcnn)), Verb(trans, gnum=rcvn, argstr='trans'))
    ARC2 = Phrase(pron, VerbP(Verb(trans, gnum=svn), NounP(det = det, N = Noun(inanim, gnum=rcnn)).with_adj(A)))
    ARC3 = Phrase(pron, NounP(det = det, N = Noun(anim, gnum=rcnn)).with_adj(A), Verb(trans, gnum=rcvn, argstr='trans'))
    RC4 = Phrase(pron,
                 VerbP(
                     Verb(trans, gnum=svn),
                     NounP(det = det, N = Noun(inanim, gnum=subrcnn)).with_RelC(RC = Phrase(pron, VerbP(Verb(intrans, gnum=subrcvn))))))

    PROMPT = Word('???')

    # Simple:
    C_A  = Sentence(NP = aNP, VP = PROMPT)
    C_B  = Sentence(NP = aNP.with_RelC(RC = pron), VP = PROMPT)
    C_C  = Sentence(NP = aNP.with_RelC(RC = RC1), VP = PROMPT)
    C_D  = Sentence(NP = aNP.with_PrepP(PP), VP = PROMPT)
    C_E1 = Sentence(NP = aNP.with_RelC(RC = RC2), VP = PROMPT)
    C_E2 = Sentence(NP = iNP.with_RelC(RC = RC3), VP = PROMPT)
    C_F1 = Sentence(NP = aNP.with_RelC(RC = ARC2), VP = PROMPT)
    C_F2 = Sentence(NP = iNP.with_RelC(RC = ARC3), VP = PROMPT)
    C_G  = Sentence(NP = aNP.with_RelC(RC = RC4), VP = PROMPT)

    for i in range(1):
        print(C_A.express())
        print(C_B.express())
        print(C_C.express())
        print(C_D.express())
        print(C_E1.express())
        print(C_E2.express())
        print(C_F1.express())
        print(C_F2.express())
        print(C_G.express())


if __name__=='__main__': main()
