from rules_engine import Rule, RulesEngine, then, when


RULE_1 = Rule(when("A"), then(1))
RULE_2 = Rule(when("B"), then(2), tags=["even", "consonant"])
RULE_3 = Rule(when("C"), then(3), tags=["consonant"])


def test_reject_rules_with_a_certain_tag():
    engine = a_rules_engine_with_tagged_rules().reject("even")
    assert engine.rules == (RULE_1, RULE_3)


def test_select_rules_with_a_certain_tag():
    engine = a_rules_engine_with_tagged_rules().select("consonant")
    assert engine.rules == (RULE_2, RULE_3)


def a_rules_engine_with_tagged_rules():
    return RulesEngine(RULE_1, RULE_2, RULE_3)
