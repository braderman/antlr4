# Copyright (c) 2012-2023 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.

import sys
from typing import Optional, List, Iterator
from Transition import Transition
from ATN import ATN

# The following images show the relation of states and
# {@link ATNState#transitions} for various grammar constructs.
#
# <ul>
#
# <li>Solid edges marked with an &#0949; indicate a required
# {@link EpsilonTransition}.</li>
#
# <li>Dashed edges indicate locations where any transition derived from
# {@link Transition} might appear.</li>
#
# <li>Dashed nodes are place holders for either a sequence of linked
# {@link BasicState} states or the inclusion of a block representing a nested
# construct in one of the forms below.</li>
#
# <li>Nodes showing multiple outgoing alternatives with a {@code ...} support
# any number of alternatives (one or more). Nodes without the {@code ...} only
# support the exact number of alternatives shown in the diagram.</li>
#
# </ul>
#
# <h2>Basic Blocks</h2>
#
# <h3>Rule</h3>
#
# <embed src="images/Rule.svg" type="image/svg+xml"/>
#
# <h3>Block of 1 or more alternatives</h3>
#
# <embed src="images/Block.svg" type="image/svg+xml"/>
#
# <h2>Greedy Loops</h2>
#
# <h3>Greedy Closure: {@code (...)*}</h3>
#
# <embed src="images/ClosureGreedy.svg" type="image/svg+xml"/>
#
# <h3>Greedy Positive Closure: {@code (...)+}</h3>
#
# <embed src="images/PositiveClosureGreedy.svg" type="image/svg+xml"/>
#
# <h3>Greedy Optional: {@code (...)?}</h3>
#
# <embed src="images/OptionalGreedy.svg" type="image/svg+xml"/>
#
# <h2>Non-Greedy Loops</h2>
#
# <h3>Non-Greedy Closure: {@code (...)*?}</h3>
#
# <embed src="images/ClosureNonGreedy.svg" type="image/svg+xml"/>
#
# <h3>Non-Greedy Positive Closure: {@code (...)+?}</h3>
#
# <embed src="images/PositiveClosureNonGreedy.svg" type="image/svg+xml"/>
#
# <h3>Non-Greedy Optional: {@code (...)??}</h3>
#
# <embed src="images/OptionalNonGreedy.svg" type="image/svg+xml"/>
class ATNState:
    INITIAL_NUM_TRANSITIONS = 4

    # constants for serialization
    INVALID_TYPE = 0
    BASIC = 1
    RULE_START = 2
    BLOCK_START = 3
    PLUS_BLOCK_START = 4
    STAR_BLOCK_START = 5
    TOKEN_START = 6
    RULE_STOP = 7
    BLOCK_END = 8
    STAR_LOOP_BACK = 9
    STAR_LOOP_ENTRY = 10
    PLUS_LOOP_BACK = 11
    LOOP_END = 12

    serializationNames = [
        "INVALID",
        "BASIC",
        "RULE_START",
        "BLOCK_START",
        "PLUS_BLOCK_START",
        "STAR_BLOCK_START",
        "TOKEN_START",
        "RULE_STOP",
        "BLOCK_END",
        "STAR_LOOP_BACK",
        "STAR_LOOP_ENTRY",
        "PLUS_LOOP_BACK",
        "LOOP_END"
    ]

    INVALID_STATE_NUMBER = -1

    # Which ATN are we in?
    atn: Optional[ATN] 
    ruleIndex: int # at runtime, we don't have Rule objects
    transitions: List[Transition] # Track the transitions emanating from this ATN state.
    nextTokenWithinRule: IntervalSet
    stateNumber: int
    nextTokenWithinRule: IntervalSet # Used to cache lookahead during parsing, not used during construction
    epsilonOnlyTransitions: bool

    def __init__(self):
        self.stateNumber = self.INVALID_STATE_NUMBER
        self.atn = None
        self.epsilonOnlyTransitions = False
        self.transitions = []

    def __hash__(self):
        return self.stateNumber

    def __eq__(self, other):
        if isinstance(other, ATNState):
            return self.stateNumber = other.stateNumber
        else:
            return False

    @property
    def IsNonGreedyExitState(self) -> bool:
        return False

    def __str__(self):
        return str(self.stateNumber)

    @property
    def Transitions(self) -> Iterator[Transition]:
        return iter(self.transitions)

    @property
    def NumberOfTransitions(self) -> int:
        return len(self.transitions)
    
    def addTransition(self, e: Transition):
        self.addTransitionAtIndex(len(self.transitions), e)

    def addTransitionAtIndex(self, index: int, e: Transition):
        if len(self.transitions) == 0: 
            self.epsilonOnlyTransitions = e.IsEpsilon
        elif self.epsilonOnlyTransitions != e.IsEpsilon:
            sys.stderr.write(f"ATN state {self.stateNumber} has both epsilon and non-epsilon transitions.\n")
            self.epsilonOnlyTransitions = False
        
        alreadyPresent = False

        for t in self.transitions:
            if t.target.stateNumber == e.target.stateNumber:
                if t.Label is not None and e.Label is not None and t.Label == e.Label:
                    # sys.stderr.write(f"Repeated transition upon {e.Label} from {self.stateNumber}->{t.target.stateNumber}\n")
                    alreadyPresent = True
                    break
                elif t.IsEpsilon and e.IsEpsilon:  
                    # sys.stderr.write(f"Repeated epsilon transition from {self.stateNumber}->{t.target.stateNumber}\n")
                    alreadyPresent = True
                    break
        if not alreadyPresent: 
            self.transitions.insert(index, e)

    def transition(self, i: int) -> Transition:
        return self.transitions[i]

    def setTransition(self, i: int, e: Transition):
        self.transitions[i] = e

    def removeTransition(self, index: int) -> Transition:
        retVal = self.transitions[index]
        del self.transitions[index]
        return retVal

    @property
    def StateType(self) -> int:
        raise NotImplementedError()
    
    @property
    def OnlyHasEpsilonTransitions(self) -> bool:
        return self.epsilonOnlyTransitions

    def setRuleIndex(self, ruleIndex:int): 
        self.ruleIndex = ruleIndex
