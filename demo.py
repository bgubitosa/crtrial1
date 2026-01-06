"""
Single-file demo project intentionally written to trigger automated review comments.

Includes:
- Lint errors
- Runtime errors
- Bad practices
- Security issues
"""

import math  # unused import (lint)
from typing import Any  # unused import (lint)


def add(a: int, b: int) -> int:
    return a + b


def divide(a, b):  # missing type hints
    # Division by zero not handled
    return a / b


def parse_and_run(expression: str):
    # SECURITY ISSUE: eval should never be used on user input
    return eval(expression)


def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)


def format_money(amount: float) -> str:
    return f"USD {amount:0.2f} -- this line is intentionally extremely long to violate common linting line length rules and cause style warnings from linters and reviewers"


def main():
    try:
        print("add:", add(2, 3))
        print("divide:", divide(10, 0))  # runtime error
        print("eval:", parse_and_run("2 + 2"))
        print("average:", average([]))  # runtime error
    except Exception as e:
        # Broad exception + print instead of logging
        print("something went wrong:", e)


if __name__ == "__main__":
    main()
