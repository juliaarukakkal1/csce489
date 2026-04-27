import collections

class Action:
    def __init__(self, name, preconds, effects):
        self.name = name
        self.preconds = set(preconds)
        self.effects = set(effects)

    def __repr__(self):
        return f"[{self.name}]"
    
class POP:
    def __init__(self, actions, initial_state, goal_state):
        self.start = Action("Start", [], initial_state)
        self.finish = Action("Finish", goal_state, [])


init = ["At_Home"]
goal = ["HasShoe_L", "HasShoe_R"]