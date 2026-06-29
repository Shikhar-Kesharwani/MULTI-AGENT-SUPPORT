import os
import autogen
from duckduckgo_search import DDGS

def main():
    # Ensure API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: Please set your GEMINI_API_KEY environment variable.")
        print("Run: $env:GEMINI_API_KEY='your-key-here'")
        exit(1)

    # 1. Configure the LLM for AutoGen using the Gemini OpenAI-compatible endpoint
    llm_config = {
        "config_list": [{
            "model": "gemini-3.5-flash",
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
        }],
        "temperature": 0.5,
    }

    # 2. Configure the Agents
    # The UserProxy acts as the "human in the loop" and executes functions (tools).
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        system_message="A human admin.",
        code_execution_config={"use_docker": False}, # Disable docker for this local script
        human_input_mode="NEVER", # Set to NEVER so it runs fully autonomously
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    )

    # The Researcher is instructed to use tools to find info
    researcher = autogen.AssistantAgent(
        name="Researcher",
        system_message="""You are an expert Researcher. 
        Use the 'search_web' tool to find detailed facts about the user's topic.
        Once you have enough facts, summarize them for the Writer.
        DO NOT write the final article yourself.""",
        llm_config=llm_config,
    )

    # The Writer takes the researcher's summary and drafts the article
    writer = autogen.AssistantAgent(
        name="Writer",
        system_message="""You are an expert technical Writer.
        Take the facts gathered by the Researcher and write a comprehensive, well-structured markdown article.
        When you are completely finished writing the article, output 'TERMINATE' on a new line at the very end.""",
        llm_config=llm_config,
    )

    # 3. Register the Search Tool
    def search_web(query: str) -> str:
        """Search the web for information using DuckDuckGo."""
        print(f"\n[Tool Execution] Searching for: {query}\n")
        results = list(DDGS().text(query, max_results=3))
        if not results:
            return "No results found."
        return str([r['body'] for r in results])

    # Let the Researcher call the tool, and the UserProxy execute it.
    autogen.agentchat.register_function(
        search_web,
        caller=researcher,
        executor=user_proxy,
        name="search_web",
        description="Search the web for information."
    )

    # 4. Orchestrate the Group Chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, researcher, writer], 
        messages=[], 
        max_round=10
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # 5. Execution
    topic = "The impact of Agentic AI on software development in 2024"
    print(f"\n--- Starting AutoGen run for topic: {topic} ---\n")
    
    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message=f"Please research and write an article about: {topic}"
    )

if __name__ == "__main__":
    main()
