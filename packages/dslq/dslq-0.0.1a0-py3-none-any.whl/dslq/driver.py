from .lexer  import DSLQLexer
from .parser import DSLQParser

class DSLQDriver:
    def __init__(self, query) -> None:
        self.query = query
        self.parser = DSLQParser()

    def tokenize(self):
        _lexer = DSLQLexer()
        _token = _lexer.tokenize(self.query)
        return [_t for _t in _token]

    def parse(self):
        _lexer = DSLQLexer()
        _token = _lexer.tokenize(self.query)

        _parser = DSLQParser()
        return _parser.parse(_token)
