```python
"""Tool router for function calling and external actions."""

import ast
import operator
import re
from datetime import datetime


def safe_calculate(expression):
    """
    Safely evaluate basic arithmetic without using eval().

    Supported:
        +   Addition
        -   Subtraction
        *   Multiplication
        /   Division
        //  Floor division
        %   Modulo
        **  Exponentiation
        ()  Parentheses
        +x  Positive numbers
        -x  Negative numbers
    """

    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression cannot be empty")

    # Prevent excessively large expressions.
    if len(expression) > 100:
        raise ValueError("Expression is too long")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        # Numbers
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("Boolean values are not allowed")

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed")

        # Binary operations: 2 + 3, 5 * 4, etc.
        if isinstance(node, ast.BinOp):
            op = allowed_operators.get(type(node.op))

            if op is None:
                raise ValueError("Operator not allowed")

            left = evaluate(node.left)
            right = evaluate(node.right)

            # Prevent extremely large exponent calculations.
            if isinstance(node.op, ast.Pow):
                if abs(right) > 100:
                    raise ValueError("Exponent is too large")

                if abs(left) > 1000000:
                    raise ValueError("Base is too large")

            return op(left, right)

        # Unary operations: -5, +5
        if isinstance(node, ast.UnaryOp):
            op = allowed_operators.get(type(node.op))

            if op is None:
                raise ValueError("Operator not allowed")

            return op(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("Invalid mathematical expression")

    return evaluate(tree.body)


class ToolRouter:
    """Routes queries to appropriate tools and formats tool calls."""

    def __init__(self, kb=None):
        """
        Initialize tool router.

        Args:
            kb: KnowledgeBase instance for knowledge retrieval.
        """
        self.kb = kb
        self.tools = self._init_tools()

    def _init_tools(self):
```
