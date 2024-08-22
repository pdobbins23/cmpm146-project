class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state):
        raise NotImplementedError

class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ": " + self.name if self.name else ""

    def tree_to_string(self, indent=0):
        string = "| " * indent + str(self) + "\n"

        for child in self.child_nodes:
            if hasattr(child, "tree_to_string"):
                string += child.tree_to_string(indent + 1)
            else:
                string += "| " * (indent + 1) + str(child) + "\n"

        return string

class Selector(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            if child_node.execute(state):
                return True

        return False

class Sequence(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            if not child_node.execute(state):
                return False

        return True

class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    def execute(self, state):
        return self.check_function(state)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.check_function.__name__

class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    def execute(self, state):
        return self.action_function(state)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.action_function.__name__
