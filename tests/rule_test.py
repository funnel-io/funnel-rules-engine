from rules_engine import NoAction, Otherwise, Rule, then, when


def test_repr():
    rule = Rule(when("A"), then(1))
    assert repr(rule) == f"<Rule id={id(rule)} tags=[]>"


def test_repr_for_no_action():
    rule = NoAction(when("B"), tags=["idle", "noop"])
    assert repr(rule) == f"<NoAction id={id(rule)} tags=['idle', 'noop']>"


def test_repr_for_otherwise():
    rule = Otherwise(then(3), tags=["else"])
    assert repr(rule) == f"<Otherwise id={id(rule)} tags=['else']>"


def test_matches():
    rule = NoAction(when("B"), tags=["idle", "noop"])
    assert rule.matches("noop")
    assert rule.matches("whatever", "idle")
    assert not rule.matches("no", "matching", "tag")
