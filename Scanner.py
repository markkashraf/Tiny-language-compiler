from Util import *


class Scanner:
    STATES = {
        'START': False,
        'IN_COMMENT': False,
        'IN_IDENTIFIER': False,
        'IN_NUM': False,
        'IN_ASSIGN': False,
        'DONE': False,
        'OTHER': False
    }
    KEYWORDS = ['else', 'end', 'if', 'repeat', 'then', 'until', 'read', 'write']
    OPERATORS = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        ':': 'COLON',
        '=': 'EQUALS',
        ':=': 'ASSIGNMENT',
        '>': 'GREATER',
        '<': 'LESS',
        ';': 'SEMICOLON',
        '(': 'OPEN_PARENTHESIS',
        ')': 'CLOSE_PARENTHESIS'
    }

    # initialize states and set the current state to start.
    def __init__(self):
        self.set_state('START')
        self.tokens = []
        self.state_other = False

    # set the current state to true and other states to false (transition from the current state to another).
    def set_state(self, state):
        for key in self.STATES:
            self.STATES[key] = False
        self.STATES[state] = True

    # check if this is the current state.
    def get_state(self, state):
        return self.STATES[state]

