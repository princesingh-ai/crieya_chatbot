from fastmcp import FastMCP
from core.models import (ProblemSearchFilters,InnovationProcessFilters,InnovationQARequest,)
from core.services import (get_problem_statements,get_innovation_process,answer_from_innovation_process,)
from utils.threading import run_in_thread

mcp = FastMCP(name="crieya-chatbot")

@mcp.tool()
async def search_problem_statements_tool(
    problem_id: str | None = None,
    title: str | None = None,
    technology_bucket: str | None = None,
    category: str | None = None,
    description: str | None = None,
    organization: str | None = None,
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
    filters = ProblemSearchFilters(
        problem_id=problem_id,
        title=title,
        technology_bucket=technology_bucket,
        category=category,
        description=description,
        organization=organization,
    )

    response = await run_in_thread(
        get_problem_statements,
        filters
    )

    return response.model_dump()

@mcp.tool()
async def innovation_process_tool(
    process_no: int | None = None,
    level: int | None = None,
    all_processes: bool = False,
):
    """
    Retrieve CRiEYA innovation process data in a structured form.

    This tool supports three primary query modes:
    1. Fetch a specific innovation process by process number
    2. Fetch a specific innovation process by level
    3. List all innovation process titles

    Parameters:
        process_no (int, optional):
            Exact innovation process number to retrieve.
            Returns full details including input, process, and output.

        level (int, optional):
            Innovation level to retrieve.
            Functionally equivalent to process number.

        all_processes (bool, optional):
            When True, returns a compact list of all innovation processes
            containing only process number and title.
            Defaults to False.

    Returns:
        dict:
            A standardized response containing:
            - count: Number of matching innovation processes
            - results: List of innovation process records

    Examples:
        - "innovation process number 1"
        - "process at level 6"
        - "give me all innovation processes"
    """

    filters = InnovationProcessFilters(
        process_no=process_no,
        level=level,
        all_processes=all_processes,
    )

    response = await run_in_thread(
        get_innovation_process,
        filters
    )

    return response.model_dump()

@mcp.tool()
async def innovation_process_qa_tool(level: int,question: str):
    """
    Answer questions strictly using the specified innovation
    process level as context.
    """

    request = InnovationQARequest(level=level,question=question)
    response = await run_in_thread(answer_from_innovation_process,request)

    return response.model_dump()


if __name__ == "__main__":
    mcp.run()