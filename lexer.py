from enum import Enum, auto


class TT(Enum):
    SYMBOL = auto()
    LPAREN = auto()
    RPAREN = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IMPLIES = auto()
    BIMPLIES = auto()
    XOR = auto()
    SEPERATOR = auto()
    LITERAL = auto()


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return f"Token({self.token_type})"
        return f"Token({self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception(
            f"Invalid character '{self.text[self.pos]}' at position {self.pos}"
        )

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(None, None)

        current_char = text[self.pos]

        if current_char.isspace():
            self.pos += 1
            return self.get_next_token()

        if current_char in "01":
            token = Token(TT.LITERAL, current_char)
            self.pos += 1
            return token

        if current_char in "([":
            token = Token(TT.LPAREN, None)
            self.pos += 1
            return token

        if current_char in ")]":
            token = Token(TT.RPAREN, None)
            self.pos += 1
            return token

        if current_char in "~!":
            token = Token(TT.NOT, None)
            self.pos += 1
            return token

        if current_char == ";":
            token = Token(TT.SEPERATOR, None)
            self.pos += 1
            return token

        if (
            text[self.pos : self.pos + (a := 3)] == "and"
            or text[self.pos : self.pos + (a := 1)] == "&"
        ):
            token = Token(TT.AND, None)
            self.pos += a
            return token

        if (
            text[self.pos : self.pos + (a := 2)] == "or"
            or text[self.pos : self.pos + (a := 1)] == "|"
        ):
            token = Token(TT.OR, None)
            self.pos += a
            return token

        if (
            text[self.pos : self.pos + 3] == "<->"
            or text[self.pos : self.pos + 3] == "iff"
        ):
            token = Token(TT.BIMPLIES, None)
            self.pos += 3
            return token


        if (
            text[self.pos : self.pos + 2] == "->"
            or text[self.pos : self.pos + 2] == "if"
        ):
            token = Token(TT.IMPLIES, None)
            self.pos += 2
            return token

        if text[self.pos : self.pos + 3] == "xor":
            token = Token(TT.XOR, None)
            self.pos += 3
            return token

        if current_char.isalpha():
            token = Token(TT.SYMBOL, current_char)
            self.pos += 1
            return token

        self.error()

