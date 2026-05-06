import collections

class Action:
    def __init__(self, name, preconditions, effects, deletes=None):
        self.name = name
        self.preconditions = set(preconditions)
        self.effects = set(effects)
        self.deletes = set(deletes) if deletes else set()

    def __repr__(self):
        return f"[{self.name}]"

class PartialOrderPlanner:
    def __init__(self, action_library, initial_state, goal_state):
        self.library = action_library
        
        # Start and Finish are the boundaries of our logic
        self.start_node = Action("START", [], initial_state)
        self.finish_node = Action("FINISH", goal_state, [])

        self.actions_in_plan = {self.start_node, self.finish_node}
        self.causal_links = set()         # (helper, condition, waiting_action)
        self.time_constraints = {(self.start_node, self.finish_node)}
        
        # The to_do_list contains "Flaws" (Unsatisfied needs)
        self.to_do_list = set() 
        for condition in self.finish_node.preconditions:
            self.to_do_list.add((condition, self.finish_node))

    def solve(self):
        print(f"Planning... Goals to reach: {[c for c, a in self.to_do_list]}")
        
        while self.to_do_list:
            # Pick a condition we need and the action that is waiting for it
            needed_condition, waiting_action = self.to_do_list.pop()
            
            # Find an action that can help
            helper_action = self.find_helper(needed_condition, waiting_action)
            
            if not helper_action:
                print(f"STOP: Impossible to satisfy {needed_condition}")
                return None

            # Link them: The helper provides the condition for the waiting action
            self.causal_links.add((helper_action, needed_condition, waiting_action))
            self.time_constraints.add((helper_action, waiting_action))

            # Fix any "Threats" where an action might ruin our helper's work
            self.fix_conflicts(helper_action)

        print("\n--- Logic Complete! ---")
        self.show_timeline()

    def find_helper(self, needed_condition, waiting_action):
        # 1. Can an action we already decided on help us?
        for action in self.actions_in_plan:
            if needed_condition in action.effects:
                if self.can_come_before(action, waiting_action):
                    print(f"  Existing action {action} helps with '{needed_condition}'")
                    return action

        # 2. If not, pick a new action from our library
        for template in self.library:
            if needed_condition in template.effects:
                new_action = Action(template.name, template.preconditions, template.effects)
                self.actions_in_plan.add(new_action)
                
                # New actions always happen after START and before FINISH
                self.time_constraints.add((self.start_node, new_action))
                self.time_constraints.add((new_action, self.finish_node))
                
                # Since this is a new action, we now need to satisfy ITS preconditions
                for pre in new_action.preconditions:
                    self.to_do_list.add((pre, new_action))
                
                print(f"  Added new action {new_action} to provide '{needed_condition}'")
                return new_action
        return None

    def fix_conflicts(self, new_action):
        """
        Promotion/Demotion: If an action ruins a condition we are relying on,
        we force it to happen earlier or later.
        """
        for action_t in self.actions_in_plan:
            for (action_h, condition, action_w) in self.causal_links:
                if condition in action_t.deletes:
                    # Move the "threat" before the helper (Promotion)
                    if self.can_come_before(action_t, action_h):
                        self.time_constraints.add((action_t, action_h))
                    # Move the "threat" after the waiting action is done (Demotion)
                    elif self.can_come_before(action_w, action_t):
                        self.time_constraints.add((action_w, action_t))

    def can_come_before(self, early_action, late_action):
        """Checks if early_action can happen before late_action without a time loop."""
        if early_action == late_action: return False
        
        visited = set()
        queue = collections.deque([late_action])
        while queue:
            current = queue.popleft()
            if current == early_action: return False
            for (before, after) in self.time_constraints:
                if before == current and after not in visited:
                    visited.add(after)
                    queue.append(after)
        return True

    def show_timeline(self):
        print("Sequence Requirements:")
        for (before, after) in sorted(list(self.time_constraints), key=lambda x: x[0].name):
            print(f"  {before.name.ljust(8)} -> then -> {after.name}")

# --- Run ---
library = [
    Action("Sock_L", [], ["HasSock_L"]),
    Action("Sock_R", [], ["HasSock_R"]),
    Action("Shoe_L", ["HasSock_L"], ["HasShoe_L"]),
    Action("Shoe_R", ["HasSock_R"], ["HasShoe_R"])
]

planner = PartialOrderPlanner(library, ["At_Home"], ["HasShoe_L", "HasShoe_R"])
planner.solve()