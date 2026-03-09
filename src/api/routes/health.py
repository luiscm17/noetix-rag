from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello_world(query: str):
    # Import agent for demonstration purposes
    from src.agents.teacher_agent import teacher_agent

    # Create instance of the agent
    agent = await teacher_agent()

    # Use the agent to respond to the user's query
    result = await agent.run(query)

    return {
        "message": "Agent response socratic method",
        "query": query,
        "agent_response": result,
        "status": "running",
    }


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pdf-reader-api"}
