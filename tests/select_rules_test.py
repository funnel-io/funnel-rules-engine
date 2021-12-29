from rules_engine import Rule, RulesEngine, then, when


RULE_1 = Rule(when("A"), then(1), tags=["vowel"])
RULE_2 = Rule(when("B"), then(2), tags=["even", "consonant"])
RULE_3 = Rule(when("C"), then(3), tags=["consonant"])
ENGINE = RulesEngine(RULE_1, RULE_2, RULE_3)


def test_reject_rules_with_a_certain_tag():
    assert ENGINE.reject("even").rules == (RULE_1, RULE_3)


def test_reject_rules_using_multiple_tags():
    assert ENGINE.reject("even", "vowel").rules == (RULE_3,)


def test_select_rules_with_a_certain_tag():
    assert ENGINE.select("consonant").rules == (RULE_2, RULE_3)


def test_select_rules_using_multiple_tags():
    assert ENGINE.select("even", "vowel").rules == (RULE_1, RULE_2)
