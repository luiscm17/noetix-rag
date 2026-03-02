import asyncio
from agents.teacher_agent import teacher_agent

async def main():
    agent = await teacher_agent()
    result = await agent.run("What are the Newton's laws?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
