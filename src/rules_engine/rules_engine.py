from concurrent.futures import ThreadPoolExecutor


class RulesEngine:
    def __init__(self, *rules):
        self.rules = rules

    def run(self, state):
        """Short-circuits on the first applicable rule."""
        for rule in self.rules:
            if rule.condition(state):
                return rule.action(state)

    def run_all(self, state):
        """Runs all applicable rules."""
        return [rule.action(state) for rule in self.rules if rule.condition(state)]

    def run_all_in_parallel(self, state):
        """Runs all applicable rules in parallel threads."""

        def run_rule(rule):
            return rule.action(state) if rule.condition(state) else NoMatch

        def only_executed(results):
            return list(filter(lambda result: result != NoMatch, results))

        with ThreadPoolExecutor() as parallel:
            return only_executed(parallel.map(run_rule, self.rules))


class Rule:
    """
    Contains a condition callable and an action callable.

    The condition takes a state and returns True or False.
    The action takes a state and is executed if the condition returned True.
    """

    def __init__(self, condition, action):
        self.condition = condition
        self.action = action


class NoAction(Rule):
    """This rule returns None if its condition matches."""

    def __init__(self, condition):
        super().__init__(condition, lambda state: None)


class Otherwise(Rule):
    """This rule always executes its action."""

    def __init__(self, action):
        super().__init__(lambda state: True, action)


class NoMatch:
    """Represents a rule not matching and hence its action not being executed."""
