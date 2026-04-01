import json
import asyncio
from llm.sarvam_client import chat


async def run_agent(query: str, mcp_client, mcp_tools):
    # Convert tools to LLM schema
    tools = [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        }
        for tool in mcp_tools
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are the CRIEYA AI Agent.\n"
                "Use tools ONLY when necessary to retrieve factual data.\n"
                "After you have enough information, you MUST stop calling tools and provide a final answer.\n"
                "Do NOT call tools repeatedly for the same information.\n"
                "Always synthesize tool results into a clear final answer.\n"
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]

    max_steps = 6

    for step in range(max_steps):
        response = await asyncio.to_thread(chat, messages, tools)
        msg = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": msg.tool_calls
        })

        # Final answer
        if not msg.tool_calls:
            return msg.content or "No response generated."

        # Execute tools
        for call in msg.tool_calls:
            tool_name = call.function.name
            raw_args = call.function.arguments

            try:
                args = json.loads(raw_args) if raw_args else {}
            except:
                args = {}

            try:
                result = await mcp_client.call_tool(tool_name, args)
                output = "\n".join(
                    content.text for content in result.content
                    if getattr(content, "type", None) == "text"
                )
            except Exception as e:
                output = f"Error: {str(e)}"

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": tool_name,
                "content": output
            })

    final = await asyncio.to_thread(chat, messages)
    return final.choices[0].message.content or "Agent stopped without final answer."