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
        self.library = library
        self.start = Action("Start", [], initial_state)
        self.finish = Action("Finish", goal_state, [])

        self.initial_plan = {
            'actions':{self.start, self.finish},
            'constraints':{(self.start, self.finish)},
            'links':{},
            'agenda':{(pre, self.finish) for pre in self.finish.preconds},
        } 



library = [
    Action("Sock_L", [], ["HasSock_L"]),
    Action("Sock_R", [], ["HasSock_R"]),
    Action("Shoe_L", ["HasSock_L"], ["HasShoe_L"]),
    Action("Shoe_R", ["HasSock_R"], ["HasShoe_R"])
]

init = ["At_Home"]
goal = ["HasShoe_L", "HasShoe_R"]

planner = POP(library, init, goal)