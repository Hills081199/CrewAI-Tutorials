"""
CrewAI Example: AI Research & Blog Writing Pipeline
=====================================================
Demonstrates all 6 key elements of high-performance agents:
  1. Role Playing  - Agents with defined roles, goals, and backstory
  2. Focus         - Tasks with clear scope and constraints
  3. Tools         - SerperDevTool for real-time web search
  4. Cooperation   - Agents share output via task context
  5. Guardrails    - max_iter, output constraints, behavioral rules
  6. Memory        - Short-term, Long-term, and Entity memory enabled
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()  # Load environment variables from .env file

openai_api_key = os.getenv("OPENAI_API_KEY")
# LLM config
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=openai_api_key)

# Tools (element 3)
# SerperDevTool provides real-time Google Search capability.
# Only the researcher agent gets this tool — the writer does not
# need to search the web; it only uses the researcher's output.
# Requires SERPER_API_KEY environment variable.
search_tool = SerperDevTool(
    n_results = 10, # retrun top 10 search results per query
    country="us", # target English language results
    locale="en"
)

# ==============================================================
# ELEMENT 1: ROLE PLAYING — Agent: Researcher
# A well-defined role, goal, and backstory guide the LLM to
# adopt a specific persona, which dramatically improves output
# quality and consistency.
#
# ELEMENT 4: GUARDRAILS (max_iter)
# max_iter=5 prevents the agent from looping indefinitely.
# If it hasn't finished in 5 iterations, it returns best effort.
#
# ELEMENT 6: MEMORY (agent-level)
# memory=True allows the agent to recall information from
# earlier steps within the same crew run (short-term) and
# from previous runs (long-term via SQLite).
# ==============================================================
researcher = Agent(
    # -- Role Playing --
    role = "Senior AI Research Analyst",
    goal = (
        "Search, analyze, and synthesize the most accurate and up-to-date "
        "information about the top AI trends in 2025 from credible sources."
    ),
    backstory = (
        "You are a veteran research analyst with 10 years of experience tracking "
        "technology trends for Fortune 500 companies. You are known for your "
        "ability to cut through the noise and identify only the most impactful, "
        "well-supported insights. You never cite unverified sources, and you "
        "always cross-reference findings across multiple publications."
    ),
    # -- Tools --
    tools = [search_tool],  # Only the researcher has access to the search tool
    llm = llm,  # Use the configured LLM
    verbose = True,  # Print agent thoughts and actions

    # -- Guardrails --
    max_iter = 5,  # Limit to 5 iterations to prevent infinite loops
    max_rpm = 10,    # Max 10 API requests per minute to avoid rate limits

    # -- Memory --
    memory = True,  # Enable both short-term and long-term memory
    allow_delegation = False  # Researcher handles its own tasks; no sub-delegation
)

# ==============================================================
# ELEMENT 1: ROLE PLAYING — Agent: Editor
# New agent added to review and improve the draft before
# publishing. Demonstrates a 3-agent pipeline.
# ==============================================================
editor = Agent(
    role = "Senior Content Editor",
    goal = (
        "Review the draft blog post for clarity, structure, and accuracy. "
        "Ensure it matches the target audience's reading level and fix any "
        "grammar or flow issues."
    ),
    backstory=(
        "You are a meticulous editor who has worked at top tech media outlets "
        "for 8 years. You have a sharp eye for vague claims, awkward sentences, "
        "and structural inconsistencies. You improve readability without changing "
        "the core message or adding new facts."
    ),
    llm = llm,
    verbose = True,
    # -- Guardrails --
    max_iter = 3,  # Limit to 3 iterations for editing
    # -- Memory --
    memoryview = True,  # Editor can recall the draft and previous edits
    allow_delegation = False  # Editor handles its own tasks; no sub-delegation
)

# ==============================================================
# ELEMENT 1: ROLE PLAYING — Agent: Writer
# ==============================================================
writer = Agent(
    role="Technology Content Writer",
    goal=(
        "Write an engaging, well-structured Vietnamese blog post based strictly "
        "on the research report provided. The article must be accessible to "
        "a general tech-savvy audience."
    ),
    backstory=(
        "You are a professional technology writer who has published over 500 "
        "articles on AI, software, and digital transformation. You excel at "
        "turning dense research into compelling narratives. You NEVER fabricate "
        "data or add information not present in your source material. "
        "You write exclusively in Vietnamese when producing final content."
    ),
    llm=llm,
    verbose=True,
    # --- Guardrails ---
    max_iter=3,
    # --- Memory ---
    memory=True,
    allow_delegation=False
)

# ==============================================================
# ELEMENT 2: FOCUS — Task: Research
# A well-focused task description tells the agent exactly:
#   - WHAT to do (research top 5 AI trends)
#   - WHERE to look (credible sources only)
#   - WHAT to produce (structured report with 3 specific fields)
#   - WHAT NOT to do (avoid speculative or unverified sources)
#
# Narrow scope = higher quality output.
# ==============================================================
research_task = Task(
    description=(
        "Research the Top 5 most impactful AI trends in 2025. \n\n"
        "For EACH trend, you MUST provide:\n"
        "  1. Trend Name — a clear, concise title\n"
        "  2. Summary — what it is and why it matters (80–120 words)\n"
        "  3. Real-world Applications — at least 2 concrete use cases\n"
        "  4. Leading Organizations — companies or institutions driving this trend\n"
        "  5. Source URLs — at least 1 credible reference per trend\n\n"
        "FOCUS CONSTRAINTS:\n"
        "  - Only use sources published in 2024 or 2025\n"
        "  - Preferred sources: arxiv.org, openai.com, deepmind.google, "
        "techcrunch.com, wired.com, nature.com\n"
        "  - Do NOT include trends without verifiable sources\n"
        "  - Do NOT speculate beyond what sources state\n"
    ),
    expected_output=(
        "A structured markdown report with exactly 5 sections. "
        "Each section covers one trend with all 5 required fields clearly labeled. "
        "Total length: 600–800 words. Language: English."
    ),
    agent=researcher,
    output_file="research_output.md"
)

# ==============================================================
# ELEMENT 2: FOCUS — Task: Write Draft
# ELEMENT 5: COOPERATION
# context=[research_task] passes the researcher's output directly
# into this task's prompt, enabling agent-to-agent data sharing
# without manual intervention.
# ==============================================================
write_task = Task(
    description=(
        "Using ONLY the research report provided in context, write a complete "
        "Vietnamese blog post with the following structure:\n\n"
        "  1. Title — catchy, SEO-friendly, in Vietnamese\n"
        "  2. Introduction — 150 words, hooks the reader, explains why AI trends matter\n"
        "  3. Main Body — one section per trend (use H2 headings), each section:\n"
        "       - Opens with a compelling hook sentence\n"
        "       - Explains the trend in plain language (100–120 words)\n"
        "       - Includes a real-world example\n"
        "       - Ends with a forward-looking insight\n"
        "  4. Conclusion — 100 words, summarizes key takeaways, ends with a CTA\n\n"
        "GUARDRAIL RULES:\n"
        "  - Write entirely in Vietnamese\n"
        "  - Do NOT add facts, statistics, or claims not in the research report\n"
        "  - Do NOT include source URLs in the blog post\n"
        "  - Use H1 for title, H2 for each trend section\n"
        "  - Target reading level: general Vietnamese tech audience\n"
    ),
    expected_output=(
        "A complete, publish-ready Vietnamese blog post in markdown format. "
        "Length: 800–1000 words. Must include all 5 trend sections with H2 headings."
    ),
    agent=writer,
    # --- Cooperation: receive researcher's output as context ---
    context=[research_task],
    output_file="draft_blog.md"
)

# ==============================================================
# ELEMENT 2: FOCUS — Task: Edit & Finalize
# ELEMENT 5: COOPERATION
# Editor receives both the research and the draft as context,
# allowing it to verify accuracy while improving the writing.
# ==============================================================
edit_task = Task(
    description=(
        "Review the Vietnamese blog post draft and improve it. Your job is to:\n\n"
        "  1. Fix grammar, punctuation, and awkward phrasing\n"
        "  2. Improve sentence flow and readability\n"
        "  3. Ensure each section follows the required structure\n"
        "  4. Verify no claims appear that are NOT in the research report\n"
        "  5. Strengthen the introduction hook and conclusion CTA\n"
        "  6. Add a meta description (150 chars max) at the very top\n\n"
        "GUARDRAIL RULES:\n"
        "  - Do NOT change the meaning of any paragraph\n"
        "  - Do NOT add new facts or data\n"
        "  - Preserve Vietnamese language throughout\n"
        "  - Keep the final length between 800–1000 words\n"
    ),
    expected_output=(
        "The final, polished Vietnamese blog post in markdown format, "
        "starting with a meta description line. "
        "All 5 trend sections present. Ready to publish."
    ),
    agent=editor,
    # --- Cooperation: editor uses both research + draft as context ---
    context=[research_task, write_task],
    output_file="final_blog.md"
)

# ==============================================================
# ELEMENT 5: COOPERATION — Crew Assembly
# Process.sequential ensures tasks run in order:
#   researcher → writer → editor
# Each agent's output is automatically available to the next.
#
# ELEMENT 6: MEMORY (crew-level)
# memory=True at crew level enables:
#   - Short-term memory: shared context within this run (ChromaDB)
#   - Long-term memory: persisted learnings across runs (SQLite)
#   - Entity memory: tracks people, orgs, concepts (ChromaDB)
#
# embedder config uses text-embedding-3-small for vector storage.
# ==============================================================
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],

    # --- Cooperation ---
    process=Process.sequential,   # Tasks run in order; outputs chain automatically

    # --- Memory (crew-level) ---
    memory=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"  # Cost-efficient embedding model
        }
    },

    # --- Guardrails (crew-level) ---
    max_rpm=20,       # Limit total API calls across all agents to 20/min

    verbose=True,     # Print detailed execution logs to console
    output_log_file="crew_run.log"  # Save full execution log to file
)

# ==============================================================
# KICKOFF
# crew.kickoff() starts the pipeline. The final result is the
# output of the last task (edit_task = polished blog post).
# ==============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Starting CrewAI Research & Writing Pipeline")
    print("  Agents: Researcher → Writer → Editor")
    print("="*60 + "\n")

    result = crew.kickoff()

    print("\n" + "="*60)
    print("  FINAL OUTPUT")
    print("="*60)
    print(result)

    print("\n✅ Output files saved:")
    print("   - research_output.md  (raw research)")
    print("   - draft_blog.md       (first draft)")
    print("   - final_blog.md       (polished final)")
    print("   - crew_run.log        (execution log)")