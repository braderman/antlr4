# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root. 

from typing import List, Optional
from collections import OrderedDict
from copy import copy
from ATNState import ATNState

class ATN:
    states: List[Optional[ATNState]]
    
    # Each subrule/rule is a decision point and we must track them so we
    # can go back later and build DFA predictors for them.  This includes
    # all the rules, subrules, optional blocks, ()+, ()* etc...
    decisionToState: List[DecisionState]
    ruleToStartState: List[RuleStartState] # Maps from rule index to starting state number.
    ruleToStopState: List[RuleStopState] # Maps from rule index to stop state number.
    modeNameToStartState: OrderedDict[str, TokenStartState]
    grammarType: ATNType # The type of the ATN.
    maxTokenType: int
    
    # For lexer ATNs, this maps the rule index to the resulting token type.
    # For parser ATNs, this maps the rule index to the generated bypass token
    # type if the
    # {@link ATNDeserializationOptions#isGenerateRuleBypassTransitions}
    # deserialization option was specified; otherwise, this is {@code null}.
    # 
    ruleToTokenType: List[int]

    # For lexer ATNs, this is an array of {@link LexerAction} objects which may
    # be referenced by action transitions in the ATN. 
    lexerActions: List[LexerAction]

    modeToStartState: List[TokenStartState]

    INVALID_ALT_NUMBER = 0

    # Used for runtime deserialization of ATNs from strings
    def __init__(self, grammarType_: ATNType, maxTokenType_: int):
        self.grammarType = grammarType_
        self.maxTokenType = maxTokenType_
        self.states = []
        self.decisionToState = []
        self.ruleToStartState = []
        self.ruleToStopState = []
        self.modeNameToStartState = {}
        self.ruleTokenType = []
        self.lexerActions = []
        self.modeToStartState = []

    # Compute the set of valid tokens that can occur starting in state {@code s}.
    # If {@code ctx} is null, the set of tokens will not include what can follow
    # the rule surrounding {@code s}. In other words, the set will be
    # restricted to tokens reachable staying within {@code s}'s rule.
    def nextTokensWithRuleCtx(self, s: ATNState, ctx: RuleContext) -> IntervalSet:
        analyzer = LL1Analyzer(self)
        next = analyzer.LOOK(s, ctx)
        return next

    # Compute the set of valid tokens that can occur starting in {@code s} and
    # staying in same rule. {@link Token#EPSILON} is in set if we reach end of
    # rule.
    def nextTokens(self, s: ATNState) -> IntervalSet:
        if s.nextTokenWithinRule is not None:
            return s.nextTokenWithinRule
        
        s.nextTokenWithinRule = self.nextTokens(s, None)
        s.nextTokenWithinRule.setReadonly(True)
        return s.nextTokenWithinRule

    def addState(self, state: Optional[ATNState]):
        if state is not None:
            state.atn = self
            state.stateNumber = len(self.states)
        
        self.states.append(state)

    def removeState(self, state: ATNState):
        self.states[state.stateNumber] = None #just free mem, don't shift states in list
    
    def defineDecisionState(self, s: DecisionState) -> int:
        self.decisionToState.append(s)
        s.decision = len(self.decisionToState)-1
        return s.decision

    def getDecisionState(self, decision: int) -> Optional[DecisionState]:
        if len(self.decisionToState) != 0:
            return self.decisionToState[decision]
        
        return None
    
    @property
    def NumberOfDecisions(self) -> int:
        return len(self.decisionToState)
    
    # Computes the set of input symbols which could follow ATN state number
    # {@code stateNumber} in the specified full {@code context}. This method
    # considers the complete parser context, but does not evaluate semantic
    # predicates (i.e. all predicates encountered during the calculation are
    # assumed true). If a path in the ATN exists from the starting state to the
    # {@link RuleStopState} of the outermost context without matching any
    # symbols, {@link Token#EOF} is added to the returned set.
    # 
    # <p>If {@code context} is {@code null}, it is treated as {@link ParserRuleContext#EMPTY}.</p>
    # 
    # Note that this does NOT give you the set of all tokens that could
    # appear at a given token position in the input phrase.  In other words,
    # it does not answer:
    # 
    #   "Given a specific partial input phrase, return the set of all tokens
    #    that can follow the last token in the input phrase."
    # 
    # The big difference is that with just the input, the parser could
    # land right in the middle of a lookahead decision. Getting
    # all *possible* tokens given a partial input stream is a separate
    # computation. See https://github.com/antlr/antlr4/issues/1428
    # 
    # For this function, we are specifying an ATN state and call stack to compute
    # what token(s) can come next and specifically: outside of a lookahead decision.
    # That is what you want for error reporting and recovery upon parse error.
    # 
    # @param stateNumber the ATN state number
    # @param context the full parse context
    # @return The set of potentially valid input symbols which could follow the
    # specified state in the specified context.
    # @throws IllegalArgumentException if the ATN does not contain a state with
    # number {@code stateNumber}
    def getExpectedTokens(self, stateNumber: int, context: RuleContext) -> IntervalSet:
        if stateNumber < 0 or stateNumber >= len(self.states):
            raise RuntimeError("Invalid state number.")

        ctx = context
        s = self.states[stateNumber]
        following = self.nextTokens(s)
        if Token.EPSILON not in following: 
            return following

        expected = IntervalSet()
        expected.addAll(following)
        expected.remove(Token.EPSILON)

        while ctx is not None and ctx.invokingState >= 0 and Token.EPSILON in following:
            invokingState = self.states[ctx.invokingState]
            rt = invokingState.transition(0)
            following = self.nextTokens(rt.followState)
            expected.addAll(following)
            expected.remove(Token.EPSILON)
            ctx = ctx.parent

        if Token.EPSILON in following:
            expected.add(Token.EOF)

        return expected
