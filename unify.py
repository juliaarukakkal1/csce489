import sys
from convCNF import *

def is_variable(expr):
    """Checks if the expression is a variable (typically starts with '?')."""
    return hasattr(expr, 'atom') and expr.atom is not None and expr.atom.startswith('?')

def unify(A, B, bindings=None):
    """
    Finds the Most General Unifier (MGU) for expressions A and B.
    """
    if bindings is None:
        bindings = {}

    # 1. Identity check
    if A.toString() == B.toString():
        return bindings

    # 2. Variable cases
    if is_variable(A):
        return unify_var(A.atom, B, bindings)
    if is_variable(B):
        return unify_var(B.atom, A, bindings)

    # 3. Structural recursion (List/Function cases)
    if A.list is not None and B.list is not None:
        if len(A.list) != len(B.list):
            return None
        
        # Unify head and then unify the rest using the updated bindings
        for a_sub, b_sub in zip(A.list, B.list):
            bindings = unify(a_sub, b_sub, bindings)
            if bindings is None:
                return None
        return bindings

    # 4. Constants that aren't identical fail
    return None

def unify_var(var, expr, bindings):
    """Handles binding a variable to an expression or another variable."""
    if var in bindings:
        return unify(bindings[var], expr, bindings)
    
    # If the expression is also a bound variable, look it up
    if is_variable(expr) and expr.atom in bindings:
        return unify(var, bindings[expr.atom], bindings)

    # CRITICAL: Occurs Check
    # Ensures ?x cannot be unified with (f ?x)
    if occurs_check(var, expr, bindings):
        return None

    # Add the new substitution
    new_bindings = bindings.copy()
    new_bindings[var] = expr
    return new_bindings

def occurs_check(var, expr, bindings):
    """Returns True if variable 'var' appears inside 'expr'."""
    if is_variable(expr):
        if var == expr.atom:
            return True
        if expr.atom in bindings:
            return occurs_check(var, bindings[expr.atom], bindings)
    elif expr.list is not None:
        return any(occurs_check(var, sub, bindings) for sub in expr.list)
    return False

def subst(bindings, expr):
    """Recursively applies substitutions to an expression."""
    if is_variable(expr):
        if expr.atom in bindings:
            # Recurse in case the value is another variable
            return subst(bindings, bindings[expr.atom])
        return expr
    
    if expr.list is not None:
        new_expr = expr.copy()
        new_expr.list = [subst(bindings, x) for x in expr.list]
        return new_expr
    
    return expr

if __name__ == "__main__":
    # Check if we got the right number of arguments from the terminal
    if len(sys.argv) < 3:
        print("Usage: python unify.py \"(expr1)\" \"(expr2)\"")
    else:
        # 1. Parse the strings into Sexpr objects
        try:
            A = Sexpr(tokenize(sys.argv[1]), 0)
            B = Sexpr(tokenize(sys.argv[2]), 0)

            # 2. Run the unification
            unifier = unify(A, B, {})

            # 3. Print the results
            if unifier is None:
                print("Result: Not Unifiable")
            else:
                print("--- Unification Successful ---")
                print("Bindings found:")
                for var, expr in unifier.items():
                    print(f"  {var} -> {expr.toString()}")
                
                # Show the final "filled-in" version
                final_A = subst(unifier, A)
                print(f"\nFinal Unified Expression: {final_A.toString()}")
        except Exception as e:
            print(f"Error: Could not parse input. {e}")