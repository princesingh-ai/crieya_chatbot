from fastmcp import FastMCP
from core.models import (ProblemSearchFilters,InnovationProcessFilters, CrieyaPreincubationHubQARequest, CrieyaFocusQARequest, TrlLevelRequest)
from core.services import (get_problem_statements,get_innovation_process, get_crieya_preincubation_hub_qa, get_crieya_focus_qa, get_trl_levels)
from asyncio import to_thread

mcp = FastMCP(name="crieya-chatbot")

@mcp.tool()
async def search_problem_statements(filters: ProblemSearchFilters):
    """
    Search SIH problem statements.

    Examples:
    - "farming related technology bucket"
    - "problem with ID SIH1524"
    - "AI problems from ISRO"
    - "problem id 1524"

    Supports:
    - Exact ID matching
    - Partial matching across other fields

    ID Handling:
    - If the query contains a 4-digit number referring to a problem ID
    (e.g., "id 1524", "problem 1524", "problem statement 1524"),
    automatically prepend "SIH" to the number
    → Example: 1524 → SIH1524

    - If "SIH" is already present, use the ID as-is

    Notes:
    - ID matching is exact after normalization
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
    Retrieve CRiEYA innovation process data and annexures.

    This tool contains and retrieves structured information about the complete
    CRiEYA innovation lifecycle, including all process stages and supporting annexures.

    Innovation Process Flow:
    1. Call for Application by CRiEYA Co-ordinators (the first stage of the innovation process where potential innovators are formally invited to submit their ideas or project proposals.)
    2. Innovation Projects Screening at Institute/Department internal level (Level 1)
    3. Innovation Projects Screening by External Steering Committee/Industry Experts (Level 2)
    4. Funding Evaluation by CRiEYA Seed Management Committee (CSMC) (Level 3)
    5. Innovation Projects On-boarding by Team CRiEYA
    6. Project Execution and Operations by Institute/Department Co-ordinator,
       Principal Investigator, and Students
    7. Role of Project Mentoring and Monitoring Committee
    8. Innovation Projects Closure as per work status
    9. Project Closure

    Capabilities:
    - Fetch a specific innovation process by process number
    - Retrieve the complete innovation process (all stages)
    - List all innovation process titles
    - Retrieve annexures (Annexure A to Annexure J)
    - Handle combined queries (e.g., "Process 2 with Annexure B")

    Args:
        filters (InnovationProcessFilters):
            Input filters used to query the innovation process data. May include:
            - process_number (int): Specific process stage number
            - annexure (str): Annexure identifier (e.g., "A", "B", ..., "J")
            - query_type (str): Type of request (e.g., "full", "titles", "specific", "annexure")
            - additional flags depending on schema

    Parameters Context:
        - If process_number is provided → returns that specific stage
        - If annexure is provided → returns annexure details
        - If both are provided → returns combined results
        - If no filters → returns full innovation process

    Returns:
        dict:
            A structured JSON response containing:
            - process details (title, description, stage info)
            - annexure details (if requested)
            - full workflow data (if requested)
            - or filtered results based on input

    Notes:
        - This tool is the source of truth for CRiEYA innovation workflow data
    """  
    response = await to_thread(
        get_innovation_process,
        filters
    )
    return response.model_dump()

@mcp.tool()
async def crieya_preincubation_hub_qa_tool(request:CrieyaPreincubationHubQARequest):
    """
    Retrieve structured information about the CRiEYA Pre-incubation Hub.

    Args:
        request (CrieyaPreincubationHubQARequest):
            An object containing the query parameters for retrieval.
            Expected fields:
            - query (str): The user’s question or topic to search for

    Returns:
        dict:
            A structured JSON object containing retrieved information.
            Typical structure:
            {
                "results": [
                    {
                        "title": str,
                        "content": str,
                        "source": str (optional),
                    }
                ]
            }

    Notes:
        - This tool ONLY retrieves factual data from CRiEYA documentation.
        - It does NOT generate final answers.
        - The calling agent must interpret and synthesize the response.
    """
    response = await to_thread(
        get_crieya_preincubation_hub_qa,
        request
    )
    return response.model_dump()

@mcp.tool()
async def crieya_focus_tool(request: CrieyaFocusQARequest):
    """
    Retrieve structured information about CRiEYA focus areas.

    This includes:
    - domains
    - technologies
    - practice areas
    - objectives

    Args:
        request (CrieyaFocusQARequest):
            Query parameters for retrieving focus-related data.
            Expected fields:
            - query (str): Topic or question about focus areas

    Returns:
        dict:
            Structured data containing relevant focus area information.
            Example:
            {
                "results": [
                    {
                        "title": str,
                        "content": str,
                    }
                ]
            }

    Notes:
        - This tool retrieves factual data only.
        - It does NOT generate final answers.
        - The calling agent must interpret and synthesize the response.
    """
    response = await to_thread(
        get_crieya_focus_qa,
        request
    )
    return response.model_dump()

@mcp.tool()
async def trl_levels_tool(request: TrlLevelRequest):
    """
    Retrieve structured information about Technology Readiness Levels (TRL).

    This includes:
    - definitions of each TRL level
    - evaluation criteria
    - characteristics of maturity stages

    Args:
        request (TrlLevelRequest):
            Query parameters for TRL-related retrieval.
            Expected fields:
            - query (str): Specific TRL question or level (e.g., "TRL 5 meaning")
            - level (optional, int): Specific TRL level (1–9)

    Returns:
        dict:
            Structured TRL information.
            Example:
            {
                "results": [
                    {
                        "level": int,
                        "title": str,
                        "description": str,
                    }
                ]
            }

    Notes:
        - This tool only retrieves TRL data.
        - It does NOT generate final answers.
        - The calling agent must synthesize the final response.
    """
    response = await to_thread(
        get_trl_levels,
        request
    )
    return response.model_dump()

if __name__ == "__main__":
    # HTTP transport
    mcp.run(transport="http", host="127.0.0.1", port=8000)