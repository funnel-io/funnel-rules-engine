from inspect import isgenerator
import pytest
from time import sleep, time
from rules_engine import NoAction, Otherwise, Rule, RulesEngine, then

NOT_FOUND_MESSAGE = "not found"
NOT_IMPLEMENTED_MESSAGE = "not implemented"
OTHER_MESSAGE = "other"


@pytest.mark.parametrize(
    "status, result",
    [
        (404, NOT_FOUND_MESSAGE),
        (501, NOT_IMPLEMENTED_MESSAGE),
        (418, OTHER_MESSAGE),
    ],
    ids=[
        "test_first_condition_matches",
        "test_second_condition_matches",
        "test_default_rule",
    ],
)
def test_run(status, result):
    assert a_rules_engine().run(State(status=status)) == result


def test_run_without_any_matching_rules():
    assert RulesEngine().run(State()) is None


def test_run_all():
    assert a_rules_engine().run_all(State(status=404)) == [NOT_FOUND_MESSAGE, OTHER_MESSAGE]


def test_run_all_lazily():
    lazy_results = a_rules_engine().run_all(State(status=404), lazy=True)
    assert isgenerator(lazy_results)
    assert list(lazy_results) == [NOT_FOUND_MESSAGE, OTHER_MESSAGE]


def test_run_all_in_parallel():
    engine = RulesEngine(
        Rule(always_matches, then(1)),
        Rule(never_matches, never_executed),
        Rule(always_matches, then(2)),
        Rule(always_matches, then(3)),
        NoAction(always_matches),
        Otherwise(then(OTHER_MESSAGE)),
    )
    assert engine.run_all_in_parallel(State()) == [1, 2, 3, None, OTHER_MESSAGE]


def test_run_all_in_parallel_with_delay():
    engine = RulesEngine(
        Rule(always_matches, return_after_delay(1)),
        Rule(always_matches, return_after_delay(2)),
        Rule(always_matches, return_after_delay(3)),
        Rule(always_matches, return_after_delay(4)),
        Rule(always_matches, return_after_delay(5)),
    )
    elapsed_time, result = measure(lambda: engine.run_all_in_parallel(State()))
    assert result == [1, 2, 3, 4, 5]
    assert elapsed_time < 0.5


def test_run_all_in_parallel_lazily():
    engine = RulesEngine(
        Rule(always_matches, then(1)),
        Rule(never_matches, never_executed),
        Rule(always_matches, then(2)),
        Rule(always_matches, then(3)),
        NoAction(always_matches),
        Otherwise(then(OTHER_MESSAGE)),
    )
    lazy_results = engine.run_all_in_parallel(State(), lazy=True)
    assert isgenerator(lazy_results)
    assert list(lazy_results) == [1, 2, 3, None, OTHER_MESSAGE]


def test_no_action():
    engine = RulesEngine(
        Rule(never_matches, never_executed),
        NoAction(always_matches),
        Otherwise(then(OTHER_MESSAGE)),
    )
    assert engine.run(State()) is None


def test_otherwise():
    engine = RulesEngine(
        Rule(never_matches, never_executed),
        Otherwise(then(OTHER_MESSAGE)),
    )
    assert engine.run(State()) == OTHER_MESSAGE


def a_rules_engine():
    return RulesEngine(
        Rule(when_is_not_found, then(NOT_FOUND_MESSAGE)),
        Rule(when_is_service_not_implemented, then(NOT_IMPLEMENTED_MESSAGE)),
        Otherwise(then(OTHER_MESSAGE)),
    )


def always_matches(state):
    return True


def measure(function):
    start = time()
    result = function()
    elapsed_time = time() - start
    return elapsed_time, result


def never_executed(state):
    raise AssertionError("This action should never be executed.")


def never_matches(state):
    return False


def return_after_delay(value, seconds=0.1):
    def wait_and_return(state):
        sleep(seconds)
        return value

    return wait_and_return


def when_is_not_found(state):
    return state.status == 404


def when_is_service_not_implemented(state):
    return state.status == 501


class State:
    def __init__(self, status=200):
        self.status = status
