from search import *
from reporting import *


class MCState:
    def __init__(self, leftMissionaries=3, leftCannibales=3, isBoatLeftShore=True):
        self.leftMissionaries = leftMissionaries
        self.leftCannibales = leftCannibales

        self.rightMissionaries = 3 - leftMissionaries
        self.rightCannibales = 3 - leftCannibales

        self.isBoatLeftShore = isBoatLeftShore

    def next(self, action, previous=None):
        if previous.isBoatLeftShore:
            return MCState(
                previous.leftMissionaries - action[0],
                previous.leftCannibales - action[1],
                False,
            )
        else:
            return MCState(
                previous.leftMissionaries + action[0],
                previous.leftCannibales + action[1],
                True,
            )

    def __lt__(self, other):
        return (
            13 - self.leftMissionaries * 2 - self.leftCannibales * 2 - 1
            if self.isBoatLeftShore
            else 0
        ) < (
            13 - other.leftMissionaries * 2 - other.leftCannibales * 2 - 1
            if other.isBoatLeftShore
            else 0
        )

    def __str__(self):
        str = ""
        for i in range(0, self.leftMissionaries):
            str += "🔵"
        for i in range(0, self.leftCannibales):
            str += "🔴"
        for i in range(self.leftMissionaries + self.leftCannibales, 6):
            str += "  "

        if self.isBoatLeftShore:
            str += " LEFT  "
        else:
            str += " RIGHT "

        for i in range(0, self.rightMissionaries):
            str += "🔵"
        for i in range(0, self.rightCannibales):
            str += "🔴"
        for i in range(self.rightMissionaries + self.rightCannibales, 6):
            str += "  "

        return str


class MCProblem(Problem):
    def __init__(self, initial=MCState(), goal=MCState(0, 0, False)):
        self.initial = initial
        self.goal = goal

    def actions(self, state: MCState):

        actions = self.generateActions(state)
        validActions = actions.copy()

        r = range(0, 4)

        for action in actions:
            newState = state.next(action, state)

            # UNFEASIBLE NUMBER OF PEOPLE
            if not (
                newState.leftMissionaries in r
                and newState.leftCannibales in r
                and newState.rightMissionaries in r
                and newState.rightCannibales in r
            ):
                validActions.remove(action)

            # CANNIBALES MORE THAN MISSIONARY UNFEASIBLE STATES
            elif (
                newState.leftCannibales > newState.leftMissionaries
                and newState.leftMissionaries > 0
                or newState.rightCannibales > newState.rightMissionaries
                and newState.rightMissionaries > 0
            ):
                validActions.remove(action)

        return validActions

    def generateActions(self, state):
        results = []

        results.append([1, 0])
        results.append([0, 1])
        results.append([1, 1])
        results.append([2, 0])
        results.append([0, 2])

        return results

    def result(self, state: MCState, action):
        newState = state.next(action, state)
        return newState

    def goal_test(self, state: MCState):
        return (
            state.leftCannibales == 0
            and state.leftMissionaries == 0
            and state.isBoatLeftShore == False
        )

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node: Node):
        return (
            13 - node.state.leftMissionaries * 2 - node.state.leftCannibales * 2 - 1
            if node.state.isBoatLeftShore
            else 0
        )


def main():
    problem = MCProblem()
    soln = breadth_first_tree_search(problem)
    path = path_actions(soln)
    print(path)
    print("Cost: ", soln.path_cost)
    path = path_states(soln)
    print(path)

    report(
        [
            breadth_first_tree_search,
            breadth_first_graph_search,
            astar_search,
        ],
        [problem],
    )


if __name__ == "__main__":
    main()
