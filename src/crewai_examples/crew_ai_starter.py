import os

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

# Choose LLM provider based on environment variable
# Set USE_OLLAMA=true to use local Ollama, otherwise uses OpenAI
if os.getenv("USE_OLLAMA", "false").lower() == "true":
    # Use host.docker.internal to access Ollama running on host machine
    llm = LLM(
        model="ollama/mistral:7b",
        base_url="http://host.docker.internal:11434",
    )
else:
    # Use OpenAI - requires OPENAI_API_KEY in .env
    # gpt-4o-mini is cheap (~$0.15/1M input tokens)
    llm = LLM(
        model="gpt-4o-mini",
    )


def create_linkedin_content_agent(topic: str) -> Crew:
    # Define the AI agent focused on generating LinkedIn content for AI pros
    content_agent = Agent(
        role="Content Creator for LinkedIn",
        goal=f"""Generate engaging LinkedIn posts tailored for
                 AI professionals on the topic: {topic}""",
        verbose=False,
        llm=llm,
        backstory=(
            """You are a professional content writer specialized
               in crafting insightful and concise LinkedIn posts
               that resonate with AI professionals. Your style is clear,
               informative, and engaging."""
        ),
    )

    # Define the task with dynamic topic interpolation
    task = Task(
        description=f"""Write a LinkedIn post about: {topic}
        Focus on relevance to AI professionals, keep it concise
        (around 150-200 words), and include a call to action.""",
        expected_output="A LinkedIn post text ready to be published.",
        agent=content_agent,
    )

    # Create the crew with the agent and task, sequential execution
    crew = Crew(
        agents=[content_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


if __name__ == "__main__":
    topic = "The future of Large Language Models in AI"
    crew = create_linkedin_content_agent(topic)
    result = crew.kickoff()
    print("Generated LinkedIn Post:\n", result)
