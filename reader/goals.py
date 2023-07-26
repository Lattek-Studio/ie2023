class Goal:
    type: str
    target = {
        "x": int,
        "y": int
    }

    def __init__(self, type, target):
        self.type = type
        self.target = target


class GoalSystem:
    goals = []

    def addGoal(self, goal):
        self.goals.append(goal)

    def getGoal(self):
        return self.goals[0]

    def removeGoal(self):
        if (len(self.goals) == 0):
            return
        self.goals.pop(0)

    def canExecuteGoal(self, goal):
        if (goal.type == "goOffset"):
            return True
        return False

    def executeGoals(self):
        for goal in self.goals:
            if (self.canExecuteGoal(goal)):
                return self.executeGoal(goal)
        return ""

    def executeGoal(self, goal):
        if (goal.type == "goOffset"):
            if (goal.target["x"] > 0):
                return "r"
            if (goal.target["x"] < 0):
                return "l"
            if (goal.target["y"] > 0):
                return "d"
            if (goal.target["y"] < 0):
                return "u"
        return ""
