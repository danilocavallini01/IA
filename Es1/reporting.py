from collections import Counter

from search import *

failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.


def path_actions(node):
    """The sequence of actions to get to this node."""
    if node is None:
        return []
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    """The sequence of states to get to this node."""
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""

    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)

def myLen(node):
    return 0 if node.parent is None else (1 + myLen(node.parent))

def report(searchers, problems, verbose=True):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    for searcher in searchers:
        print(searcher.__name__ + ':')
        total_counts = Counter()
        for p in problems:
            prob = CountCalls(p)
            soln = searcher(prob)
            counts = prob._counts;
            counts.update(actions=myLen(soln), cost=soln.path_cost)
            total_counts += counts
            if verbose: report_counts(counts, str(p.__class__.__name__)[:40])
        report_counts(total_counts, 'TOTAL\n')


def report_counts(counts, name):
    """Print one line of the counts report."""
    print('{:9,d} inserted nodes |{:9,d} tested goals |{:5.0f} cost |{:8,d} expanded_nodes | {}'.format(
        counts['result'], counts['goal_test'], counts['cost'], counts['actions'], name))
