# Rules Engine

A simple, generic rules engine. Inspired by [Martin Fowler's 2009 blog post](https://www.martinfowler.com/bliki/RulesEngine.html).

## Installation

Install the package `funnel_rules_engine` version `1.1+` from PyPi.
The recommended `requirements.txt` line is `funnel_rules_engine~=1.1`.

## Current Functionality

### `Rule`

A combination of a condition and an action, both of which are callables such as functions or lambdas.

#### `Otherwise`

Special case of Rule where the action always fires. Suitable as a catch-all last rule.

#### `NoAction`

Special case of Rule where `None` is returned if the condition is met. Useful for halting the execution of `.run()`

### `RulesEngine`

A generic rules engine that accepts a list of `Rule`s and some input to apply the rules to. The rules engine can either apply the first rule that matches (`run`) or all the rules that matches (`run_all`). In addition, rules can be evaluated and executed in parallel (`run_all_in_parallel`).

For more on rules engines, see [Martin Fowler's blog post](https://martinfowler.com/bliki/RulesEngine.html).

#### `run`

Only apply the first rule that matches and return its result. This is comparable to the behaviour of a [structured switch statement](https://en.wikipedia.org/wiki/Switch_statement#Semantics) or an arbitrary [conditional statement](https://en.wikipedia.org/wiki/Conditional_(computer_programming)).

#### `run_all`

Apply all rules that match. The result is returned as a list. 

#### `run_all_in_parallel`

Evaluate and apply all rules in parallel. The result is returned as a list.
