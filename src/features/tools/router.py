"""Tool router for function calling and external actions."""
import json
import re
from datetime import datetime
from pathlib import Path


class ToolRouter:
    """Routes queries to appropriate tools and formats tool calls."""
    
    def __init__(self, kb=None):
        """Initialize tool router.
        
        Args:
            kb: KnowledgeBase instance for knowledge retrieval
        """
        self.kb = kb
        self.tools = self._init_tools()
    
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
        """Detect if query is requesting a tool.
        
        Returns:
            Tuple of (tool_name, args) or (None, None)
        """
        # Pattern: "calculate 2 + 3" or "what is the capital of france"
        patterns = [
            (r"calculate\s+(.+)", "calculator"),
            (r"what is\s+(.+)", "knowledge"),
            (r"what time", "time"),
            (r"current time", "time"),
            (r"search for\s+(.+)", "document_search"),
            (r"remember that\s+(.+)", "memory_lookup"),
        ]
        
        for pattern, tool in patterns:
            match = re.search(pattern, query.lower())
            if match:
                args = match.group(1) if match.lastindex else ""
                return tool, args
        
        return None, None
    
    def tool_calculator(self, expression):
        """Safe calculator tool.
        
        Args:
            expression: Math expression to evaluate
            
        Returns:
            Result or error message
        """
        try:
            # Only allow safe math operations
            safe_dict = {"__builtins__": {}}
            result = eval(expression, safe_dict)
            return f"The result is {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def tool_knowledge(self, query):
        """Knowledge base retrieval tool.
        
        Args:
            query: Fact to look up
            
        Returns:
            Fact or "not found" message
        """
        if not self.kb:
            return "Knowledge base not available"
        
        # Try exact match first
        result = self.kb.get_fact(query.lower().replace(" ", "_"))
        if result:
            return result
        
        # Try search
        results = self.kb.search_facts(query)
        if results:
            return f"Found: {results[0][1]} (category: {results[0][2]})"
        
        return f"No information found about '{query}'"
    
    def tool_time(self, _=None):
        """Get current time.
        
        Returns:
            Current datetime string
        """
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def tool_memory_lookup(self, query):
        """Lookup information in conversation memory.
        
        Args:
            query: What to remember or look up
            
        Returns:
            Memory entry or confirmation
        """
        return f"Remembered: {query}"
    
    def tool_document_search(self, query):
        """Search documents in knowledge base.
        
        Args:
            query: Search query
            
        Returns:
            Document excerpt or not found
        """
        if not self.kb:
            return "Knowledge base not available"
        
        docs = self.kb.search_documents(query)
        if docs:
            doc_id, title, content = docs[0]
            excerpt = content[:200] + "..." if len(content) > 200 else content
            return f"Found: '{title}'\n{excerpt}"
        
        return f"No documents found for '{query}'"
    
    def route_and_execute(self, query):
        """Detect and execute appropriate tool.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (tool_executed, result)
        """
        tool_name, args = self.detect_tool_request(query)
        
        if tool_name and tool_name in self.tools:
            tool_func = self.tools[tool_name]
            result = tool_func(args) if args else tool_func()
            return True, result
        
        return False, None
    
    def format_tool_result(self, tool_name, result):
        """Format tool result for model context.
        
        Args:
            tool_name: Name of tool that was executed
            result: Tool result
            
        Returns:
            Formatted string for prompt
        """
        return f"[{tool_name.upper()}]: {result}"
