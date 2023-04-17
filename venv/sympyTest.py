import sympy

expr = sympy.parsing.sympy_parser.parse_expr('2+2*3+2+(5+8)')
atoms = expr.atoms()

print(sympy.simplify("6%5"))