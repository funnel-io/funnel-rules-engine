# Rules Engine

![PyPI](https://img.shields.io/pypi/v/funnel-rules-engine)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/funnel-rules-engine)
![PyPI - Status](https://img.shields.io/pypi/status/funnel-rules-engine)
![PyPI - License](https://img.shields.io/pypi/l/funnel-rules-engine)
[![Python package](https://github.com/funnel-io/funnel-rules-engine/actions/workflows/python-package.yml/badge.svg)](https://github.com/funnel-io/funnel-rules-engine/actions/workflows/python-package.yml)

A simple, generic rules engine. Inspired by [Martin Fowler's 2009 blog post](https://www.martinfowler.com/bliki/RulesEngine.html).

This package was extracted from [Funnel](https://funnel.io)'s production code and made open source.

For the story behind its inception, raison d'être, and overall concept, you can watch the talk [Rules Rule](https://youtu.be/Lsi1ZhmbNDc) held by [Lennart Fridén](https://github.com/DevL) at [PyCon Sweden](https://www.pycon.se) 2021.


## Installation

Install the package `funnel_rules_engine` version `1.3+` from PyPi.
The recommended `requirements.txt` line is `funnel_rules_engine~=1.3`.

## Current Functionality

### `Rule`

A combination of a condition and an action, both of which are callables such as functions or lambdas. The callables must have an arity of one. If the conditional returns true given a single object, the action will be called with the same object as its argument.

#### `Otherwise`

Special case of Rule where the action always fires. Suitable as a catch-all last rule.

#### `NoAction`

Special case of Rule where `None` is returned if the condition is met. Useful for halting the execution of `.run()`

### `RulesEngine`

A generic rules engine that accepts a list of `Rule`s and some input to apply the rules to. The rules engine can either apply the first rule that matches (`run`) or all the rules that matches (`run_all`). In addition, rules can be evaluated and executed in parallel (`run_all_in_parallel`). The latter two cases can optionally be lazily executed by returning a generator rather than a list as the result.

For more on rules engines, see [Martin Fowler's blog post](https://martinfowler.com/bliki/RulesEngine.html).

#### `run`

Only apply the first rule that matches and return its result. This is comparable to the behaviour of a [structured switch statement](https://en.wikipedia.org/wiki/Switch_statement#Semantics) or an arbitrary [conditional statement](https://en.wikipedia.org/wiki/Conditional_(computer_programming)).

#### `run_all`

Apply all rules that match. The result is returned as a list, or as a generator if the optional parameter `lazy` is passed as `True`.

#### `run_all_in_parallel`

Evaluate and apply all rules in parallel. The result is returned as a list, or as a generator if the optional parameter `lazy` is passed as `True`.

### `when` and `then`

These are convenience functions for creating simple conditions and actions. They both accept a single value that in the case of `when` will be used to check equality with the passed state and in the case of `then` will be returned, ignoring the passed state.
