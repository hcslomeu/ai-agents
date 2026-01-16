#!/usr/bin/env python3
"""
Simple AI Agents Workflow
=========================

Three specialized agents working in sequence:
- 🏷️  Agent Classifier: Expert in categorizing texts
- 🔍 Agent Keywords: Expert in identifying keywords
- 📝 Agent Summarizer: Expert in summarizing texts

Each agent has its own "personality" and specific focus.
"""

import os
from typing import List, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

load_dotenv()


# ============================================================================
# LLM Configuration
# ============================================================================

# Choose LLM provider based on environment variable
# Set USE_OLLAMA=true to use local Ollama, otherwise uses OpenAI
if os.getenv("USE_OLLAMA", "false").lower() == "true":
    from langchain_ollama import ChatOllama

    # Use host.docker.internal to access Ollama running on host machine
    llm = ChatOllama(
        model="mistral:7b",
        base_url="http://host.docker.internal:11434",
        temperature=0.5,
    )
    print("🤖 Using Ollama + Mistral (local)")
else:
    from langchain_openai import ChatOpenAI

    # Use OpenAI - requires OPENAI_API_KEY in .env
    # gpt-4o-mini is cheap (~$0.15/1M input tokens)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5,
    )
    print("🤖 Using OpenAI + gpt-4o-mini")


# ============================================================================
# Graph Visualization
# ============================================================================

# Output directory for generated files
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")


def save_graph_visualization(team, filename="agents_workflow.png"):
    """Saves the workflow graph as PNG to the outputs/ directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)

    print("\n📊 Generating workflow visualization...")
    try:
        graph_png = team.get_graph().draw_mermaid_png()
        with open(filepath, "wb") as f:
            f.write(graph_png)
        print(f"✅ Graph saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"⚠️  Error generating visualization: {e}")
        return None


# ============================================================================
# Shared State - Team Memory
# ============================================================================


class TeamState(TypedDict):
    """Shared memory between agents"""

    original_text: str  # Original text for analysis
    category: str  # Category identified by Classifier
    important_terms: List[str]  # Keywords found by Keywords agent
    summary: str  # Summary created by Summarizer
    current_agent: str  # Which agent is currently working


# ============================================================================
# Agent 1: Classifier - Categorization Expert
# ============================================================================


def agent_classifier(state: TeamState):
    """
    🏷️ Agent Classifier
    Expert in identifying the type/category of texts
    """
    print("\n🏷️  Agent Classifier is analyzing...")
    print("   Specialty: Text categorization")

    # Specialized prompt for classification
    prompt = f"""
    You are a text classification expert.
    Your only task is to identify the category of the text.

    Classify this text into ONE of these categories:
    - News
    - Personal Blog
    - Technical Article
    - Marketing
    - Educational
    - Other

    Text to analyze:
    {state["original_text"]}

    Reply only with the category:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    category = response.content.strip()

    print(f"   📂 Category identified: {category}")

    return {"category": category, "current_agent": "Classifier"}


# ============================================================================
# Agent 2: Keywords - Keywords Expert
# ============================================================================


def agent_keywords(state: TeamState):
    """
    🔍 Agent Keywords
    Expert in extracting important keywords
    """
    print("\n🔍 Agent Keywords is analyzing...")
    print("   Specialty: Keyword identification")

    # Specialized prompt for keywords
    prompt = f"""
    You are a keyword analysis expert.
    Your task is to find the 5 most important keywords from the text.

    Category already identified: {state["category"]}

    Text to analyze:
    {state["original_text"]}

    Extract exactly 5 important keywords, separated by commas.
    Focus on: main concepts, important names, technologies, places.

    Keywords:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    keywords_text = response.content.strip()
    keywords = [kw.strip() for kw in keywords_text.split(",")]

    print(f"   🔑 Keywords: {keywords}")

    return {"important_terms": keywords, "current_agent": "Keywords"}


# ============================================================================
# Agent 3: Summarizer - Summary Expert
# ============================================================================


def agent_summarizer(state: TeamState):
    """
    📝 Agent Summarizer
    Expert in creating concise and informative summaries
    """
    print("\n📝 Agent Summarizer is analyzing...")
    print("   Specialty: Summary creation")

    # Specialized prompt for summary
    prompt = f"""
    You are an expert in creating concise summaries.
    Your task is to summarize the text in maximum 15 words.

    Information from other agents:
    - Category: {state["category"]}
    - Keywords: {", ".join(state["important_terms"])}

    Text to summarize:
    {state["original_text"]}

    Create a summary of maximum 15 words that captures the essence:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    summary = response.content.strip()

    print(f"   📋 Summary: {summary}")

    return {"summary": summary, "current_agent": "Summarizer"}


# ============================================================================
# Creating the Agents Team
# ============================================================================


def create_agents_team():
    """Creates the specialized agents team"""
    print("\n🔧 Assembling agents team...")

    # Create the workflow
    workflow = StateGraph(TeamState)

    # Add each specialized agent
    workflow.add_node("classifier", agent_classifier)
    workflow.add_node("keyword_agent", agent_keywords)
    workflow.add_node("summarizer", agent_summarizer)

    # Define the team's workflow
    workflow.set_entry_point("classifier")  # Starts with classification
    workflow.add_edge("classifier", "keyword_agent")  # Then identifies keywords
    workflow.add_edge("keyword_agent", "summarizer")  # Finally, creates summary
    workflow.add_edge("summarizer", END)  # Work completed

    # Compile the team
    team = workflow.compile()
    print("✅ Agents team ready to work!")

    return team


# ============================================================================
# Testing Our Team
# ============================================================================


def test_agents_team():
    """Tests our agents team with sample text"""
    print("\n" + "=" * 70)
    print("🚀 AGENTS TEAM IN ACTION")
    print("=" * 70)

    # Create the team
    team = create_agents_team()

    # Try to save visualization
    save_graph_visualization(team)

    # Sample text
    sample_text = """
    OpenAI launched ChatGPT-4, a new version of its language model
    that promises to revolutionize how we interact with artificial intelligence.
    The model presents significant improvements in reasoning, creativity and
    multimodal capabilities, being able to process both text and images.
    The company expects this technology to positively impact various sectors,
    from education to software development.
    """

    print("\n📖 Text for analysis:")
    print(f"   {sample_text.strip()}")
    print("\n" + "-" * 70)
    print("🔄 Starting collaborative analysis...")

    # Execute the team analysis
    result = team.invoke({"original_text": sample_text, "current_agent": "Starting"})

    # Show final results
    print("\n" + "=" * 70)
    print("📊 TEAM FINAL REPORT")
    print("=" * 70)
    print(f"🏷️  Category: {result['category']}")
    print(f"🔑 Keywords: {', '.join(result['important_terms'])}")
    print(f"📋 Summary: {result['summary']}")
    print(f"👥 Last agent: {result['current_agent']}")
    print("\n✨ Collaborative analysis completed!")

    return result


def test_different_texts():
    """Tests with different types of text"""
    team = create_agents_team()

    texts = {
        "Personal Blog": "Today I woke up early and went running in the park. The day was beautiful and I managed to do 5km. I feel great after the exercise and ready for another productive day of work.",
        "News": "The Brazilian government announced new economic measures today to combat inflation. The Central Bank is expected to raise the Selic rate at the next Copom meeting.",
        "Technical Article": "Machine Learning is a subfield of artificial intelligence that allows systems to learn automatically without being explicitly programmed. Algorithms like Random Forest and Neural Networks are widely used.",
    }

    print("\n" + "=" * 70)
    print("🔬 TESTING DIFFERENT TEXT TYPES")
    print("=" * 70)

    for text_type, text in texts.items():
        print(f"\n📄 Testing: {text_type}")
        print(f"Text: {text[:60]}...")
        print("-" * 50)

        result = team.invoke({"original_text": text})

        print(f"🏷️  {result['category']}")
        print(f"🔑 {', '.join(result['important_terms'][:3])}...")  # First 3 keywords
        print(f"📋 {result['summary']}")


# ============================================================================
# Main Execution
# ============================================================================


def main():
    """Main function - runs the team tests"""
    print("🌟 SPECIALIZED AGENTS SYSTEM")
    print("Each agent has its specialty and works as a team!")
    print("=" * 70)

    try:
        # Main test
        # test_agents_team()

        # Tests with varied texts
        test_different_texts()

        print("\n" + "=" * 70)
        print("💡 TIPS:")
        print("- Check the 'outputs/agents_workflow.png' file to see the graph!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Ollama is running:")
        print("ollama run mistral:latest")


if __name__ == "__main__":
    main()
