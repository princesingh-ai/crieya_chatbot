import asyncio
from fastmcp import Client
from agent.agent import run_agent

async def main():
    print("Connecting to MCP server...")

    async with Client("http://127.0.0.1:8000/mcp") as client:
        print("Welcome to the CRIEYA Assistant! Type 'exit' or 'quit' to stop.")

        mcp_tools = await client.list_tools()

        while True:
            query = input("\nUser: ").strip()

            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if not query:
                continue

            response = await run_agent(query, client, mcp_tools)
            print(f"\nAssistant: {response}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")