import os
import operator
from typing import TypedDict, Annotated, List

# LangChain / LangGraph imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from duckduckgo_search import DDGS
from langgraph.graph import StateGraph, START, END

# --- 1. Define the State ---
# The state is a dictionary that is passed between our agents.
class ResearchState(TypedDict):
    topic: str
    research_notes: Annotated[List[str], operator.add]
    final_draft: str

# --- 2. Initialize Tools and LLM ---
# We are using Gemini because it has a generous free tier via Google AI Studio.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) 

def run_search(query: str) -> str:
    try:
        results = list(DDGS().text(query, max_results=3))
        if not results:
            return "No results found."
        return str([r['body'] for r in results])
    except Exception as e:
        return f"Search failed: {str(e)}"

# --- 3. Define the Agents (Nodes) ---
def researcher_agent(state: ResearchState):
    """
    This agent takes the topic and searches the web for relevant information.
    """
    topic = state["topic"]
    print(f"--- [Researcher Agent] Searching for: {topic} ---")
    
    # 1. Ask the LLM to generate a good search query based on the topic
    query_prompt = f"Generate a highly effective web search query to find detailed information about: {topic}. Output ONLY the query string."
    search_query = llm.invoke([HumanMessage(content=query_prompt)]).content.strip()
    
    print(f"--- [Researcher Agent] Executing Search: '{search_query}' ---")
    # 2. Use DuckDuckGo to search the internet
    search_results = run_search(search_query)
    
    # 3. Add the results to our state's "research_notes" list
    # Because we used `operator.add` in the state definition, this list will append rather than overwrite.
    return {"research_notes": [f"Search Results for '{search_query}':\n{search_results}"]}


def writer_agent(state: ResearchState):
    """
    This agent takes all the gathered research notes and writes a final article.
    """
    topic = state["topic"]
    notes = "\n\n".join(state["research_notes"])
    print(f"--- [Writer Agent] Drafting article for: {topic} ---")
    
    writer_prompt = f"""You are an expert technical writer. 
    Write a comprehensive, well-structured markdown article on the topic: '{topic}'.
    
    Research Notes:
    {notes}
    
    IMPORTANT: If the research notes are empty, say "No results found", or are insufficient, you MUST rely on your own vast internal knowledge to write a complete and detailed article anyway. Do not complain about missing notes.
    
    Ensure the article has an introduction, main body sections, and a conclusion.
    """
    
    # 2. Generate the draft
    draft = llm.invoke([HumanMessage(content=writer_prompt)]).content
    
    # 3. Save the draft to the state
    return {"final_draft": draft}

# --- 4. Orchestrate with LangGraph ---
# Initialize the graph
workflow = StateGraph(ResearchState)

# Add our nodes
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)

# Define the flow (Edges)
workflow.add_edge(START, "researcher")    # 1. Start goes to researcher
workflow.add_edge("researcher", "writer") # 2. Researcher passes notes to writer
workflow.add_edge("writer", END)          # 3. Writer finishes the process

# Compile the graph into an executable application
app = workflow.compile()

# --- 5. Execution ---
if __name__ == "__main__":
    # Ensure API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: Please set your GEMINI_API_KEY environment variable.")
        print("Run: $env:GEMINI_API_KEY='your-key-here'")
        exit(1)
        
    # LangChain's Google GenAI package looks for GOOGLE_API_KEY by default, 
    # so we'll map our GEMINI_API_KEY to it just to be safe.
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
        
    print("\nStarting Multi-Agent Research Writer...")
    
    # Initial state
    inputs = {
        "topic": "The impact of Agentic AI on software development in 2024", 
        "research_notes": [], 
        "final_draft": ""
    }
    
    # Run the graph
    result = app.invoke(inputs)
    
    print("\n================ FINAL DRAFT ================\n")
    print(result["final_draft"])
    print("\n=============================================\n")
