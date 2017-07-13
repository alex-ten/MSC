from random import random
import pickle



# FSM
# =====================================================
State = type('State', (object,), {})
class IntState(State):
    def __init__(self, *args, **kwargs):
        args = list(args)
        self.id = args.pop(0)
        super(IntState, self).__init__(*args, **kwargs)

    def disp(self):
        print('state '+str(self.id))


Transition = type('Transition', (object,), {})
class SimpleTransition(Transition):
    def __init__(self, *args, **kwargs):
        args = list(args)
        self.to = args.pop()
        self.from_ = args.pop()
        self.label = kwargs.pop('label')
        self.probability = kwargs.pop('probability')
        super(SimpleTransition, self).__init__()

    def disp(self):
        print('{1}({0}::{2})'.format(self.from_.id, self.label, self.to.id))


class FSM():
    def __init__(self, states, transitions):
        self.start = ''
        self.end = '\n'
        self.states = states
        self.transitions = transitions
        self.num_states = len(states)
        self.in_state = states[0]
        self.in_trans = None
        self.state_history = []
        self.trans_history = []
        self.composition = self.start
        self.trans_set = list(set([t.label for t in transitions] + [self.start, self.end]))

    def transition(self, record = False):
        fork, CPs, = [], []
        sum_ = 0
        for t in self.transitions:
            if t.from_ == self.in_state:
                fork.append(t)
                sum_ += t.probability
                CPs.append(sum_)
        if len(CPs) == 1: CPs = [1.00]
        i1 = len(fork)
        X = random()
        i0 = sum([X < cp for cp in CPs])
        choice = fork[i1 - i0]
        self.composition += choice.label
        if record:
            self.state_history.append(self.in_state)
            self.trans_history.append(choice.label)
        self.in_state = choice.to

    def utter(self, max_units):
        self.reset()
        for step in range(max_units):
            self.transition()
            if self.in_state == self.states[-1]: break
        self.composition += '\n'
        print(self.composition)
        return self.composition

    def chatter(self, num_utterances, max_chars):
        chatter_log = []
        for i in range(num_utterances):
            chatter_log.append(self.utter(max_chars))
        chatter_log.append(self.trans_set)
        return chatter_log

    def reset(self):
        self.in_state = self.states[0]
        self.composition = self.start


def make_states(l):
    return [IntState(s) for s in l]


def make_transitions(states, map, uniform=True):
    if uniform:
        froms = [k[0] for k in map.keys()]
        transitions = []
        for k,v in map.items():
            label, probability = v, 1/froms.count(k[0])
            transitions.append(SimpleTransition(states[k[0]], states[k[1]], label = label, probability = probability))
        return transitions
    else:
        return [SimpleTransition(states[k[0]], states[k[1]], label=v[0], probability=v[1]) for k,v in map.items()]



# I/O
# =====================================================
def pickle_random_chatter(log, path):
    pickle.dump(log, open(path, 'wb'))


def save_txt(log, path):
    with open(path+'new_file', 'w') as f:
        for line in log:
            f.write(str(line))



# MAINS
# =====================================================
def Reber():
    l = list(range(0,6))
    states = make_states(l)
    td = {(states[0],states[1]): 'T ',
          (states[2],states[2]): 'T ',
          (states[1],states[1]): 'S ',
          (states[3],states[5]): 'S ',
          (states[1],states[3]): 'X ',
          (states[3],states[2]): 'X ',
          (states[2],states[4]): 'V ',
          (states[4],states[5]): 'V ',
          (states[4],states[3]): 'P ',
          (states[0],states[2]): 'P ',
          }
    transitions = make_transitions(td)

    FSG = FSM(states, transitions)
    chatter_log = FSG.chatter(240,50)
    # save_txt(chatter_log, '/Users/alexten/Projects/PDP/SRN/sandbox/simple-examples/toy_data/')


def FSG_NP_uniform():
    states = make_states(list(range(0,8)))
    t_map = {
                (0,1): 'det ' ,
                (2,0): 'prep ',
                (3,0): 'prep ',
                (4,0): 'prep ',
                (5,0): 'prep ',
                (1,2): 'NS1 ' ,
                (6,2): 'NS1 ' ,
                (1,3): 'NO1 ' ,
                (6,3): 'NO1 ' ,
                (1,4): 'NS2 ' ,
                (6,4): 'NS2 ' ,
                (1,5): 'NO2 ' ,
                (6,5): 'NO2 ' ,
                (1,6): 'adj ' ,
                (6,6): 'adj ' ,
                (2,7): '.'    ,
                (5,7): '.'    ,
            }
    transitions = make_transitions(states, t_map)
    # for t in transitions: print('{}::{}, {}, p = {}'.format(t.from_.id, t.to.id, t.label, t.probability))
    FSG = FSM(states, transitions)
    chatter_log = FSG.chatter(5, 50)


def FSG_NP_nonuniform():
    NP_states = make_states(list(range(0,8)))
    NP_map = {
                (0,1): ('det ' , 1.00),
                (3,0): ('prep ', 0.20),
                (4,0): ('prep ', 0.20),
                (5,0): ('prep ', 0.20),
                (6,0): ('prep ', 0.20),
                (3,7): (''     , 0.80),
                (4,7): (''     , 0.80),
                (5,7): (''     , 0.80),
                (6,7): (''     , 0.80),
                (1,3): ('NS1 ' , 0.22),
                (2,3): ('NS1 ' , 0.22),
                (1,4): ('NS2 ' , 0.22),
                (2,4): ('NS2 ' , 0.22),
                (1,5): ('NO1 ' , 0.22),
                (2,5): ('NO1 ' , 0.22),
                (1,6): ('NO2 ' , 0.22),
                (2,6): ('NO2 ' , 0.22),
                (1,2): ('adj ' , 0.12),
                (2,2): ('adj ' , 0.12),
            }
    transitions = make_transitions(NP_states, NP_map, uniform=False)
    NP_FSG = FSM(NP_states, transitions)
    NP_FSG.utter(50)


if __name__=='__main__': FSG_NP_nonuniform()

