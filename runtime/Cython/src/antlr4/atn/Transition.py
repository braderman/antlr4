# Copyright (c) 2012-2023 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.

from typing import Dict, Optional
from ..misc import IntervalSet
from ATNState import ATNState

# An ATN transition between any two ATN states.  Subclasses define
# atom, set, epsilon, action, predicate, rule transitions.
# 
# <p>This is a one way link.  It emanates from a state (usually via a list of
# transitions) and has a target state.</p>
# 
# <p>Since we never have to change the ATN transitions once we construct it,
# we can fix these transitions as specific classes. The DFA transitions
# on the other hand need to update the labels as it adds transitions to
# the states. We'll use the term Edge for the DFA to distinguish them from
# ATN transition
class Transition:
    # constants for serialization
    EPSILON			= 1
    RANGE			= 2
    RULE			= 3
    PREDICATE		= 4 # e.g., {isType(input.LT(1))}?
    ATOM			= 5
    ACTION			= 6
    SET				= 7 # ~(A|B) or ~atom, wildcard, which convert to next 2
    NOT_SET			= 8
    WILDCARD		= 9
    PRECEDENCE		= 10

    serializationNames = [
        "INVALID",
        "EPSILON",
        "RANGE",
        "RULE",
        "PREDICATE",
        "ATOM",
        "ACTION",
        "SET",
        "NOT_SET",
        "WILDCARD",
        "PRECEDENCE"
    ]

    serializationTypes: Dict[type, int] =
    {
        EpsilonTransition: EPSILON,
        RangeTransition: RANGE,
        RuleTransition: RULE,
        PredicateTransition: PREDICATE,
        AtomTransition: ATOM,
        ActionTransition: ACTION,
        SetTransition: SET,
        NotSetTransition: NOT_SET,
        WildcardTransition: WILDCARD,
        PrecedencePredicateTransition: PRECEDENCE
    }

    # The target of this transition.

    target: ATNState
    
    def __init__(self, target_: Optional[ATNState]):
        if target_ is None:
            raise RuntimeError("target cannot be null.")
        
        self.target = target_

    @property
    def SerializationType(self) -> int:
        raise NotImplementedError()

    # 
    # Determines if the transition is an "epsilon" transition.
    # 	<p>The default implementation returns {@code false}.</p>
    # 	@return {@code true} if traversing this transition in the ATN does not
    # consume an input symbol; otherwise, {@code false} if traversing this
    # transition consumes (matches) an input symbol.
    # 

    @property
    def IsEpsilon(self) -> bool:
        return False

    @property
    def Label(self) -> Optional[IntervalSet]:
        return None

    def matches(self, symbol: int, minVocabSymbol: int, maxVocabSymbol: int) -> bool:
        raise NotImplementedError()
