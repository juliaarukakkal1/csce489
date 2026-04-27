import collections

class Action:
    def __init__(self, name, preconds, effects):
        self.name = name
        self.preconds = set(preconds)
        self.effects = set(effects)

    def __repr__(self):
        return f"[{self.name}]"
