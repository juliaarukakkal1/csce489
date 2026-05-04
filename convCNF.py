import re

class Sexpr:
    def __init__(self, tokens, pos=0):
        self.atom = None
        self.list = None
        
        if isinstance(tokens, str): # Handle direct atom creation
            self.atom = tokens
            return

        token = tokens[pos]
        if token == '(':
            self.list = []
            pos += 1
            while tokens[pos] != ')':
                child = Sexpr(tokens, pos)
                self.list.append(child)
                pos = child.end_pos
            self.end_pos = pos + 1
        else:
            self.atom = token
            self.end_pos = pos + 1

    def toString(self):
        if self.atom is not None:
            return self.atom
        return "(" + " ".join([child.toString() for child in self.list]) + ")"

    def copy(self):
        # Creates a shallow copy of the object
        new_obj = Sexpr("temp") 
        new_obj.atom = self.atom
        new_obj.list = self.list[:] if self.list is not None else None
        return new_obj

def tokenize(s):
    # Adds spaces around parentheses so we can split easily
    s = s.replace("(", " ( ").replace(")", " ) ")
    return s.split()

def isVar(expr):
    return expr.atom is not None and expr.atom.startswith('?')

def isConst(expr):
    return expr.atom is not None and not expr.atom.startswith('?')