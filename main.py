import asyncio
from fastmcp import FastMCP
from functions import ProblemSearchFilters, get_problem_statements

mcp = FastMCP(name="crieya-chatbot")

async def run_in_thread(func, *args):
    """
    Run blocking code in a thread to avoid
    blocking the MCP event loop.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)

@mcp.tool()
async def search_problem_statements_tool(
    problem_id: str | None = None,
    title: str | None = None,
    technology_bucket: str | None = None,
    category: str | None = None,
    description: str | None = None,
    orgranization: str | None = None,
):
    """
    Search SIH problem statements.

    Examples:
    - "farming related technology bucket"
    - "problem with ID SIH1524"
    - "AI problems from ISRO"

    Notes:
    - ID is matched exactly
    - Other fields are matched partially
    """
    import sys
    print("✅ MCP TOOL CALLED", file=sys.stderr)
    filters = ProblemSearchFilters(
        problem_id=problem_id,
        title=title,
        technology_bucket=technology_bucket,
        category=category,
        description=description,
        organization=orgranization,
    )

    response = await run_in_thread(
        get_problem_statements,
        filters
    )

    return response.model_dump()

if __name__ == "__main__":
    mcp.run()