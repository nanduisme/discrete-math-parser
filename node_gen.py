from lexer import TT, Lexer


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"


class UnOpNode:
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"UnOpNode({self.op}, {self.right})"


class Parser:
    def __init__(self, text) -> None:
        self.symbols = set()
        self.lexer = Lexer(text)

    def parse(self, left=None):
        if left is None:
            left = self.parse_atom()
        while True:
            token = self.lexer.get_next_token()
            if token.token_type in [TT.AND, TT.OR, TT.IMPLIES, TT.BIMPLIES, TT.XOR]:
                left = BinOpNode(left, token, self.parse_atom())
            else:
                self.lexer.pos -= 1
                break
        
        return left

    def parse_atom(self):
        token = self.lexer.get_next_token()
        if token.token_type == TT.SYMBOL:
            self.symbols.add(token.value)
            return token
        if token.token_type == TT.LITERAL:
            return token
        if token.token_type == TT.LPAREN:
            node = self.parse()
            if self.lexer.get_next_token().token_type != TT.RPAREN:
                raise Exception("Invalid syntax: expected ')'")
            return node
        if token.token_type == TT.NOT:
            return UnOpNode(token, self.parse_atom())

        raise Exception("Invalid syntax: expected symbol or '('")

