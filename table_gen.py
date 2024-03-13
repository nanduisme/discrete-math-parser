from itertools import product
from lexer import TT, Token
from node_gen import BinOpNode, Parser, UnOpNode

from rich.table import Table
from rich import print

_state = {
    "bool_mode": False,
}

class Expr:
    def __init__(self, text, node, syms) -> None:
        self.text = text
        self.node = node
        self.syms = syms

class ExprSet:
    def __init__(self) -> None:
        self.exprs = []
        self.syms = set()
    
    def add_expr(self, expr: Expr):
        self.exprs.append(expr)
        self.syms |= expr.syms

def evaluate(node, values):
    if isinstance(node, Token):
        if node.token_type == TT.LITERAL:
            return bool(int(node.value))
        return values[node.value]
    if isinstance(node, UnOpNode):
        return not evaluate(node.right, values)
    if isinstance(node, BinOpNode):
        if node.op.token_type == TT.AND:
            return evaluate(node.left, values) and evaluate(node.right, values)
        if node.op.token_type == TT.OR:
            return evaluate(node.left, values) or evaluate(node.right, values)
        if node.op.token_type == TT.IMPLIES:
            return not evaluate(node.left, values) or evaluate(node.right, values)
        if node.op.token_type == TT.BIMPLIES:
            return evaluate(node.left, values) == evaluate(node.right, values)
        if node.op.token_type == TT.XOR:
            return evaluate(node.left, values) != evaluate(node.right, values)


def bool_to_binstr(value):
    if _state["bool_mode"]:
        return "[green]True[/]" if value else "[red]False[/]"
    return "[green]1[/]" if value else "[red]0[/]"


def gen_data(nodes, symbols):
    data = []
    for syms in product([False, True], repeat=len(symbols)):
        values = dict(zip(symbols, syms))
        row = list(values.values())
        for node in nodes:
            row.append(evaluate(node, values))
        data.append(row)
    return data


def gen_table(data, symbols, exprs):
    table = Table(title="Truth Table")
    for s in symbols:
        table.add_column(s)
    for i, expr in enumerate(exprs):
        expr = expr.replace("[", "\[")
        result_column = [row[0 - len(exprs) + i] for row in data]
        if all(result_column):
            text = f"[green]{expr}[/]"
        elif not any(result_column):
            text = f"[red]{expr}[/]"
        else:
            text = expr
        table.add_column(text, justify="center")
    for row in data:
        table.add_row(*map(bool_to_binstr, row))
    table.rows[-1].style = "b i"
    return table


def process_input(text: str):
    exprs = list(
        map(lambda x: x.strip(), text.split(";"))
    )  # Split the input into expressions

    # Split the expressions into subexpressions
    for expr_text in enumerate(exprs[:]):
        opens = []
        subexprs = []
        for i, ch in enumerate(expr_text):
            if ch == "[":
                opens.append(i)
            if ch == "]":
                if len(opens) == 0:
                    raise Exception("Invalid syntax: unmatched ']'")
                subexprs.append(expr_text[opens.pop() + 1 : i])
        if len(opens) > 0:
            raise Exception("Invalid syntax: unmatched '['")
        exprs = subexprs + exprs

    expr_sets = []
    # Split the expressions into sets of expressions that share symbols
    for expr_text in exprs:
        parser = Parser(expr_text)
        node = parser.parse()

        for expr_set in expr_sets:
            # If the expression shares symbols with an existing set, add it to that set
            if (expr_set.syms & parser.symbols) != set():
                expr_set.add_expr(Expr(expr_text, node, parser.symbols.copy()))
                break
        else:
            # If the expression doesn't share symbols with any existing set, create a new set
            new_expr_set = ExprSet()
            new_expr_set.add_expr(Expr(expr_text, node, parser.symbols.copy()))
            expr_sets.append(new_expr_set)

    tables = []
    for expr_set in expr_sets:
        data = gen_data([expr.node for expr in expr_set.exprs], expr_set.syms)
        table = gen_table(data, expr_set.syms, [expr.text for expr in expr_set.exprs])
        tables.append(table)

    return tables
