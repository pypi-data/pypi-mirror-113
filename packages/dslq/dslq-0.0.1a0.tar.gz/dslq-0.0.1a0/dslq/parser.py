from sly         import Parser
from .lexer      import DSLQLexer
from .exceptions import RangeError


class DSLQParser(Parser):
    def __init__(self) -> None:
        super().__init__()

    tokens = DSLQLexer.tokens

    @_('field EQ value',
       'field GT value',
       'field LT value',
       'field IN value',
       'field GTE value',
       'field LTE value',
       'field NOT value',
       'field CONTAINS value')
    def statement(self, p):
        return {
            'type': p[1],
            'field': p.field,
            'value': p.value
        }

    @_('field RANGE value')
    def statement(self, p):
        if isinstance(p.value, tuple) and len(p.value) == 2:
            return {
                'type': p[1],
                'field': p.field,
                'value': p.value
            }
        return RangeError(p.value)

    @_('statement OR statement',
       'statement AND statement',
       'statement NOT statement',
       'NOT statement')
    def statement(self, p):
        return {
            'type': p[1],
            'left': p.statement0,
            'right': p.statement1
        }

    @_('FIELD')
    def field(self, p):
        return p.FIELD

    @_('NUMBER')
    def value(self, p):
        return p.NUMBER

    @_('DECIMAL')
    def value(self, p):
        return p.DECIMAL

    @_('STRING')
    def value(self, p):
        return p.STRING

    @_('ITER')
    def value(self, p):
        return p.ITER

    @_('RANGE')
    def value(self, p):
        return p.RANGE

    @_('LPAREN statement RPAREN')
    def statement(self, p):
        return p.statement
