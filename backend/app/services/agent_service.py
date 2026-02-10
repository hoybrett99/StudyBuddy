from typing import List, Dict, Any, Optional
from anthropic import Anthropic
import json

class StudyBuddyAgent:
    """
    AI Agent that intelligently handles user queries.
    
    Capabilities:
    - Intent detection (question type)
    - Multi-step reasoning
    - Tool usage (search, summarize, generate)
    - Conversation management
    """
    def __init__(self, claude_api_key: str, rag_service):
        self.client = Anthropic(api_key=claude_api_key)
        self.rag_service = rag_service

        # Define agent tools
        self.tools = [
            {
                "name": "search_documents",
                "description": "Search through uploaded study materials for relevant information. Use this for factual questions, definitions, and explanations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query (be specific and focused)"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of relevant chunks to retrieve (default 4, use 6-8 for complex questions)"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "multi_search",
                "description": "Perform multiple searches for multi-part questions or comparisons. Use when the question asks about several different topics.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "queries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of focused search queries"
                        }
                    },
                    "required": ["queries"]
                }
            },
            {
                "name": "generate_practice_questions",
                "description": "Generate practice questions based on document content. Use when user asks for test questions, practice, or self-assessment.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to generate questions about"
                        },
                        "num_questions": {
                            "type": "integer",
                            "description": "Number of questions to generate"
                        }
                    },
                    "required": ["topic"]
                }
            }
        ]

    async def process_query(
            self,
            user_query: str,
            conversation_history: List[Dict] = None
    ):
        """
        Process user query with agentic reasoning.
        
        Args:
            user_query: The user's question
            conversation_history: Previous messages for context
            
        Returns:
            Dict with answer, sources, and metadata
        """

        # Build conversation context
        messages = conversation_history or []
        messages.append({
            "role": "user",
            "content": user_query
        })

        # Initial agent prompt
        system_prompt = """You are Study Buddy, an intelligent AI tutor assistant. Your job is to help students learn from their uploaded study materials.

    Your capabilities:
    1. **search_documents**: Find specific information in study materials
    2. **multi_search**: Search multiple topics for comparison questions
    3. **generate_practice_questions**: Create test questions from content

    Guidelines:
    - For simple questions: use search_documents with a clear query
    - For "what's the difference between X and Y": use multi_search with separate queries for X and Y
    - For broad questions: break into focused sub-queries
    - For practice/test questions: use generate_practice_questions
    - Always explain your reasoning before calling tools
    - Be encouraging and educational

    Analyze the user's question and decide which tool(s) to use."""

        print(f"\nAgent processing: '{user_query}'")

        # Agent reasoning loop
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=self.tools,
            messages=messages
        )

        # Process agent's decision
        return await self._execute_tools(response, user_query)
    
    async def _execute_tools(self, response, original_query: str) -> Dict[str, Any]:
        """Execute tools based on agent's decision."""

        final_answer = ""
        sources = []
        tool_results = []

        # Check what the agents want to do
        for block in response.content:
            if block.type == "text":
                final_answer += block.text

            elif block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input

                print(f"Using tool: {tool_name}")
                print(f"Input: {tool_input}")

                # Execute the tools
                if tool_name == "search_documents":
                    result = await self._search_documents(
                        query=tool_input["query"],
                        num_results=tool_input.get("num_results", 4)
                    )
                    tool_results.append(result)
                    sources.extend(result[sources])

                elif tool_name == "multi_search":
                    result = await self._multi_search(tool_input["queries"])
                    tool_results.append(result)
                    sources.extend(result["sources"])
                
                elif tool_name == "generate_practice_questions":
                    result = await self._generate_practice_questions(
                        topic=tool_input["topic"],
                        num_questions=tool_input.get("num_questions", 5)
                    )
                    tool_results.append(result)

        # If agent used tools, get final synthesis
        if tool_results:
            final_answer = await self._synthesize_answer(
                original_query=original_query,
                tool_results=tool_results
            )

        return {
            "answer": final_answer,
            "sources": sources,
            "tool_calls": len(tool_results)
        }
    
    



