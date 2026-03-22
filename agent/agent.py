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
        {"role": "system", "content": "You are CRiEYA AI Agent, only answer queries relevant to the tools, Use tools to answer."},
        {"role": "user", "content": query}
    ]

    while True:
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