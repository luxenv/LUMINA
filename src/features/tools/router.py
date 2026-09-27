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
    """

    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression cannot be empty")

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
                raise ValueError(
                    "Boolean values are not allowed"
                )

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError(
                "Only numbers are allowed"
            )

        # Binary operations
        if isinstance(node, ast.BinOp):
            op = allowed_operators.get(
                type(node.op)
            )

            if op is None:
                raise ValueError(
                    "Operator not allowed"
                )

            left = evaluate(node.left)
            right = evaluate(node.right)

            # Prevent extremely large exponent calculations.
            if isinstance(node.op, ast.Pow):

                if abs(right) > 100:
                    raise ValueError(
                        "Exponent is too large"
                    )

                if abs(left) > 1000000:
                    raise ValueError(
                        "Base is too large"
                    )

            return op(left, right)

        # Unary operations such as -5 and +5
        if isinstance(node, ast.UnaryOp):
            op = allowed_operators.get(
                type(node.op)
            )

            if op is None:
                raise ValueError(
                    "Operator not allowed"
                )

            return op(
                evaluate(node.operand)
            )

        raise ValueError(
            "Invalid mathematical expression"
        )

    try:
        tree = ast.parse(
            expression,
            mode="eval"
        )
    except SyntaxError:
        raise ValueError(
            "Invalid mathematical expression"
        )

    return evaluate(tree.body)


class ToolRouter:
    """Routes queries to appropriate tools."""

    def __init__(self, kb=None, memory=None):
        """
        Initialize the tool router.

        Args:
            kb: KnowledgeBase instance.
            memory: ConversationMemory instance.
        """

        self.kb = kb
        self.memory = memory
        self.tools = self._init_tools()

    def set_memory(self, memory):
        """Set the active conversation memory."""

        self.memory = memory

    def _init_tools(self):
        """Initialize available tools."""

        return {
            "calculator": self.tool_calculator,
            "knowledge": self.tool_knowledge,
            "time": self.tool_time,
            "memory_lookup": self.tool_memory_lookup,
            "document_search": self.tool_document_search,
        }

    def detect_tool_request(self, query):
        """
        Detect whether the user is requesting a tool.

        Returns:
            Tuple of (tool_name, args).
        """

        patterns = [
            (
                r"calculate\s+(.+)",
                "calculator"
            ),
            (
                r"what is\s+(.+)",
                "knowledge"
            ),
            (
                r"what time",
                "time"
            ),
            (
                r"current time",
                "time"
            ),
            (
                r"search for\s+(.+)",
                "document_search"
            ),
            (
                r"remember that\s+(.+)",
                "memory_lookup"
            ),
            (
                r"what do you remember about\s+(.+)",
                "memory_lookup"
            ),
            (
                r"do you remember\s+(.+)",
                "memory_lookup"
            ),
            (
                r"remember\s+(.+)",
                "memory_lookup"
            ),
        ]

        query_lower = query.lower()

        for pattern, tool in patterns:

            match = re.search(
                pattern,
                query_lower
            )

            if match:
                args = (
                    match.group(1)
                    if match.lastindex
                    else ""
                )

                return tool, args

        return None, None

    def tool_calculator(self, expression):
        """Safely calculate a mathematical expression."""

        try:
            result = safe_calculate(
                expression
            )

            return f"The result is {result}"

        except Exception as exc:
            return f"Calculation error: {exc}"

    def tool_knowledge(self, query):
        """Retrieve information from the knowledge base."""

        if not self.kb:
            return "Knowledge base not available"

        # Try exact match first.
        result = self.kb.get_fact(
            query.lower().replace(
                " ",
                "_"
            )
        )

        if result:
            return result

        # Try broader search.
        results = self.kb.search_facts(
            query
        )

        if results:
            return (
                f"Found: {results[0][1]} "
                f"(category: {results[0][2]})"
            )

        return (
            f"No information found about "
            f"'{query}'"
        )

    def tool_time(self, _=None):
        """Return the current local time."""

        return (
            "Current time: "
            + datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    def tool_memory_lookup(self, query):
        """Search the active conversation session."""

        if not self.memory:
            return (
                "Conversation memory "
                "is not available"
            )

        if not query:
            return "No memory query provided"

        results = self.memory.search_memory(
            query,
            max_results=5
        )

        if not results:
            return (
                "I couldn't find anything "
                f"in this conversation about "
                f"'{query}'."
            )

        parts = []

        for turn in results:

            prompt = turn.get(
                "prompt",
                ""
            )

            response = turn.get(
                "response",
                ""
            )

            parts.append(
                f"User: {prompt}\n"
                f"Assistant: {response}"
            )

        return (
            "Relevant memories:\n"
            + "\n\n".join(parts)
        )

    def tool_document_search(self, query):
        """Search documents in the knowledge base."""

        if not self.kb:
            return "Knowledge base not available"

        docs = self.kb.search_documents(
            query
        )

        if docs:

            doc_id, title, content = docs[0]

            excerpt = (
                content[:200] + "..."
                if len(content) > 200
                else content
            )

            return (
                f"Found: '{title}'\n"
                f"{excerpt}"
            )

        return (
            f"No documents found for "
            f"'{query}'"
        )

    def route_and_execute(self, query):
        """Detect and execute an appropriate tool."""

        tool_name, args = (
            self.detect_tool_request(query)
        )

        if (
            tool_name
            and tool_name in self.tools
        ):

            tool_func = self.tools[
                tool_name
            ]

            result = (
                tool_func(args)
                if args
                else tool_func()
            )

            return True, result

        return False, None

    def format_tool_result(
        self,
        tool_name,
        result
    ):
        """Format a tool result for model context."""

        return (
            f"[{tool_name.upper()}]: "
            f"{result}"
        )

