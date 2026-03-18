from fastmcp import FastMCP
from core.models import (ProblemSearchFilters,InnovationProcessFilters, CrieyaPreincubationHubQARequest, CrieyaFocusQARequest, TrlLevelRequest)
from core.services import (get_problem_statements,get_innovation_process, get_crieya_preincubation_hub_qa, get_crieya_focus_qa, get_trl_levels)
from asyncio import to_thread

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

    response = await to_thread(
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
    
    response = await to_thread(
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
    response = await to_thread(
        get_crieya_preincubation_hub_qa,
        request
    )
    return response.model_dump()

@mcp.tool()
async def crieya_focus_tool(request: CrieyaFocusQARequest):
    """
    Answer questions about CRiEYA focus areas:
    domains, technologies, practice areas, objectives.
    """
    response = await to_thread(
        get_crieya_focus_qa,
        request
    )
    return response.model_dump()

@mcp.tool()
async def trl_levels_tool(request: TrlLevelRequest):
    """
    Provide information on Technology Readiness Levels (TRL):
    definitions, criteria, etc.
    """
    response = await to_thread(
        get_trl_levels,
        request
    )
    return response.model_dump()

if __name__ == "__main__":
    mcp.run()