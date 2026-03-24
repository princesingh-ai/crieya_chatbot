import json
import asyncio
from llm.sarvam_client import chat

async def run_agent(query: str, mcp_client, mcp_tools):
    # Get tools from MCP

    tools = []
    for tool in mcp_tools:
        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })

    messages = [
        {"role": "system", "content":  "You are the CRIEYA AI Agent. "
        "Always call tools using correct JSON format based on their parameters. "
        "Arguments MUST be valid JSON objects matching the tool schema. "
        "Do not pass raw strings as arguments."},
        {"role": "user", "content": query}
    ]

    MAX_STEPS = 5

    for step in range(MAX_STEPS):
        response = await asyncio.to_thread(chat, messages, tools)
        message = response.choices[0].message

        # add assistant message
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls
        })

        # if no tool call -> return answer
        if not message.tool_calls:
            return message.content

        # execute tools
        for tool_call in message.tool_calls:
            print(f"Tool called: {tool_call.function.name}")
            print(f"Arguments: {tool_call.function.arguments}")

            result = await mcp_client.call_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )

            texts = [c.text for c in result.content if getattr(c, "type", None) == "text"]

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": "\n".join(texts)
            })