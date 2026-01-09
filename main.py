from fastmcp import FastMCP
from core.models import (ProblemSearchFilters,InnovationProcessFilters, CrieyaPreincubationHubQARequest)
from core.services import (get_problem_statements,get_innovation_process, get_crieya_preincubation_hub_qa)
from utils.threading import run_in_thread

mcp = FastMCP(name="crieya-chatbot")

@mcp.tool()
async def search_problem_statements_tool(filters: ProblemSearchFilters):
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

    response = await run_in_thread(
        get_problem_statements,
        filters
    )
    return response.model_dump()

@mcp.tool()
async def innovation_process_tool(filters: InnovationProcessFilters):
    """
    Retrieve CRiEYA innovation process data.

    Supports:
    - Specific process by number or level
    - Listing all process titles
    """
    
    response = await run_in_thread(
        get_innovation_process,
        filters
    )
    return response.model_dump()

@mcp.tool()
async def crieya_preincubation_hub_qa_tool(request:CrieyaPreincubationHubQARequest):
    """
    Answer questions about CRiEYA as an institution:
    identity, affiliation, funding, impact, programs, patents, startups.
    """
    response = await run_in_thread(
        get_crieya_preincubation_hub_qa,
        request
    )
    return response.model_dump()

if __name__ == "__main__":
    mcp.run()