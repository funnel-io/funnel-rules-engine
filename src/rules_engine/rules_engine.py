from concurrent.futures import ThreadPoolExecutor


class RulesEngine:
    def __init__(self, *rules):
        self.rules = rules

    def reject(self, *tags):
        """Returns a new instance without the rules matching any of the given tags."""
        return self.__class__(*filter(lambda rule: not rule.matches(*tags), self.rules))

    def run(self, state):
        """Short-circuits on the first applicable rule."""
        return next(self.run_all(state, lazy=True), None)

    def run_all(self, state, lazy=False):
        """
        Runs all applicable rules and returns the result as a list.

        Accepts the optional boolean argument 'lazy' to return a generator of the results.
        """
        return result((rule.action(state) for rule in self.rules if rule.condition(state)), lazy)

    def run_all_in_parallel(self, state, lazy=False):
        """
        Runs all applicable rules in parallel threads and returns the result as a list.

        Accepts the optional boolean argument 'lazy' to return a generator of the results.
        """

        def run_rule(rule):
            return rule.action(state) if rule.condition(state) else NoMatch

        with ThreadPoolExecutor() as parallel:
            return result(only_executed(parallel.map(run_rule, self.rules)), lazy)

    def select(self, *tags):
        """Returns a new instance with the rules matching any of the given tags."""
        return self.__class__(*filter(lambda rule: rule.matches(*tags), self.rules))


class Rule:
    """
    Contains a condition callable and an action callable.

    The condition takes a state and returns True or False.
    The action takes a state and is executed if the condition returned True.
    """

    def __init__(self, condition, action, tags=None):
        self.condition = condition
        self.action = action
        self.tags = tags or []

    def matches(self, *tags):
        """Returns whether the rule is tagged with any of the given tags."""
        return any((tag in self.tags for tag in tags))

    def __repr__(self):
        return f"<{self.__class__.__name__} id={id(self)} tags={self.tags}>"


class NoAction(Rule):
    """This rule returns None if its condition matches."""

    def __init__(self, condition, tags=None):
        super().__init__(condition, then(None), tags=tags)


class Otherwise(Rule):
    """This rule always executes its action."""

    def __init__(self, action, tags=None):
        super().__init__(then(True), action, tags=tags)


class NoMatch:
    """Represents a rule not matching and hence its action not being executed."""


def only_executed(results):
    return (result for result in results if result != NoMatch)


def result(generator, lazy):
    return generator if lazy else list(generator)


def then(value):
    """
    Creates an action that ignores the passed state and returns the value.

    >>> then(1)("whatever")
    1

    >>> then(1)("anything")
    1
    """
    return lambda _state: value


def when(value):
    """
    Creates a predicate function comparing the state to the value.

    >>> when(1)(1)
    True

    >>> when(1)(2)
    False
    """
    return lambda state: state == value
