from rules_engine import Rule, RulesEngine, then, when


RULE_1 = Rule(when("A"), then(1), tags=["vowel"])
RULE_2 = Rule(when("B"), then(2), tags=["even", "consonant"])
RULE_3 = Rule(when("C"), then(3), tags=["consonant"])


def test_reject_rules_with_a_certain_tag():
    engine = RulesEngine(RULE_1, RULE_2, RULE_3).reject("even")
    assert engine.rules == (RULE_1, RULE_3)


def test_reject_rules_using_multiple_tags():
    engine = RulesEngine(RULE_1, RULE_2, RULE_3).reject("even", "vowel")
    assert engine.rules == (RULE_3,)


def test_select_rules_with_a_certain_tag():
    engine = RulesEngine(RULE_1, RULE_2, RULE_3).select("consonant")
    assert engine.rules == (RULE_2, RULE_3)


def test_select_rules_using_multiple_tags():
    engine = RulesEngine(RULE_1, RULE_2, RULE_3).select("even", "vowel")
    assert engine.rules == (RULE_1, RULE_2)
