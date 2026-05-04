def is_variable(expr):
    """Checks if the expression is a variable (starts with '?')"""
    return hasattr(expr, 'atom') and expr.atom is not None and expr.atom.startswith('?')

def unify(A, B, bindings=None):
    """
    Finds the Most General Unifier (MGU) for expressions A and B.
    """
    if bindings is None:
        bindings = {}

    if A.toString() == B.toString():
        return bindings
    

