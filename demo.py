"""
demo.py

A small, clean single-file demo that should pass typical review/lint expectations.
"""

from __future__ import annotations

import ast
import pandas
import logging
from typing import Iterable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def add(a: int, b: int) -> int:
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b must not be 0")
    return a / b


def parse_and_run(expression: str) -> int | float:
    """
    Safely evaluate a very small subset of arithmetic expressions.
    Supports: numbers, +, -, *, /, parentheses.

    This avoids `eval` on user input.
    """
    node = ast.parse(expression, mode="eval")

    def _eval(n: ast.AST) -> int | float:
        if isinstance(n, ast.Expression):
            return _eval(n.body)

        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value

        if isinstance(n, ast.BinOp) and isinstance(
            n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)
        ):
            left = _eval(n.left)
            right = _eval(n.right)

            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("division by zero in expression")
                return left / right

        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            value = _eval(n.operand)
            return value if isinstance(n.op, ast.UAdd) else -value

        raise ValueError("Unsupported expression")

    return _eval(node)


def average(nums: Iterable[float]) -> float:
    values = list(nums)
    if not values:
        raise ValueError("nums must not be empty")
    return sum(values) / len(values)


def format_money(amount: float) -> str:
    return f"USD {amount:0.2f}"


def main() -> None:
    logger.info("add(2, 3) = %s", add(2, 3))

    try:
        logger.info("divide(10, 2) = %s", divide(10, 2))
    except ZeroDivisionError:
        logger.exception("divide() failed (inputs: a=%s, b=%s)", 10, 2)

    try:
        expr = "2 + 2 * (3 - 1)"
        logger.info("parse_and_run(%r) = %s", expr, parse_and_run(expr))
    except (ValueError, SyntaxError, ZeroDivisionError) as exc:
        logger.exception("parse_and_run() failed for expression=%r: %s", expr, exc)

    try:
        numbers = [1.0, 2.0, 3.0]
        logger.info("average(%s) = %s", numbers, average(numbers))
    except ValueError as exc:
        logger.exception("average() failed for nums=%s: %s", numbers, exc)

    logger.info("format_money(12.5) = %s", format_money(12.5))


if __name__ == "__main__":
    main()
