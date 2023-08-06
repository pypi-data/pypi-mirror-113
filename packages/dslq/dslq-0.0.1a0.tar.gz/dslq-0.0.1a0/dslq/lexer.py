from sly import Lexer

class DSLQLexer(Lexer):
    tokens   = { EQ, GT, LT, GTE, LTE, AND, OR, IN, RANGE, CONTAINS,
                 ITER, NOT, FIELD, STRING, NUMBER, DECIMAL, LPAREN, RPAREN }

    ignore   = '\t '
    literals = { '(', ')', '{', '}', '>', '<' }

    @_(r'\d+\.\d+')
    def DECIMAL(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\(([^\)]+)\)')
    def ITER(self, t):
        t.value = eval(t.value)
        return t

    @_(r'\".*?\"|\'.*?\'')
    def STRING(self, t):
        t.value = t.value.strip('"').strip("'")
        return t

    EQ       = r'='
    LTE      = r'<='
    GTE      = r'>='
    LT       = r'<'
    GT       = r'>'
    IN       = r'IN|in'
    OR       = r'\||OR|or'
    AND      = r'&|AND|and'
    NOT      = r'!=|~|NOT|not'
    RANGE    = r'RANGE|range'
    CONTAINS = r'CONTAINS|contains'
    FIELD    = r'[a-zA-Z_][a-zA-Z0-9_]*'
    LPAREN   = r'\{'
    RPAREN   = r'\}'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
