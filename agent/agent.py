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
            "You are the official CRIEYA AI Assistant.\n\n"

            "Your users are students, innovators, researchers, "
            "and startup aspirants.\n\n"

            "You answer ONLY CRIEYA-related queries.\n"
            "Use CRIEYA tools and knowledge sources whenever required.\n"
            "If a question is outside the CRIEYA ecosystem or tools, "
            "politely refuse in one short sentence.\n\n"

            "Topics allowed:\n"
            "- Innovation and research\n"
            "- Engineering and technology\n"
            "- Startup and entrepreneurship\n"
            "- SIH and hackathons\n"
            "- Projects and product development\n"
            "- CRIEYA programs and initiatives\n"
            "- Domains, technologies, and practice areas\n"
            "- Academic and technical guidance\n\n"

            "RESPONSE STYLE:\n"
            "- Short\n"
            "- Precise\n"
            "- Point-to-point\n"
            "- Student-friendly\n"
            "- Exam/project oriented\n"
            "- Avoid unnecessary explanations\n"
            "- Avoid long paragraphs\n"
            "- Prefer bullet points\n"
            "- Minimize token usage\n\n"

            "TOOL USAGE RULES:\n"
            "- Use tools ONLY when necessary.\n"
            "- Do NOT answer from assumptions if tools are required.\n"
            "- Never repeat tool calls.\n"
            "- Stop tool usage immediately after enough information is found.\n"
            "- Do not waste tokens on unnecessary conversation.\n\n"

            "ANSWER FORMAT:\n"
            "- Definitions → short bullet points\n"
            "- Comparisons → concise table or bullets\n"
            "- Processes → numbered steps\n"
            "- Coding → minimal explanation + clean code\n"
            "- Ideas/projects → actionable concise structure\n"
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
        message = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls
        })

        # Final answer
        if not message.tool_calls:
            return message.content or "No response generated."

        # Execute tools
        for call in message.tool_calls:
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