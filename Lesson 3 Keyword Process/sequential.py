"""
============================================================
  CrewAI — Process.sequential  |  Full Lesson File
============================================================

CONCEPT:
  Sequential Process executes tasks ONE BY ONE in the order
  they are defined. Each task's output becomes available as
  context for all subsequent tasks.

  Flow:  Task_1 → Task_2 → Task_3 → ... → Task_N

KEY RULES:
  • Every task should have agent= assigned explicitly
  • Use context=[prev_task] to pass output forward
  • Tasks run in the exact order of the `tasks` list
  • process=Process.sequential  (default if not specified)

INSTALL:
  pip install crewai crewai-tools langchain-openai

============================================================
"""

# ── Imports ─────────────────────────────────────────────────────────
import os
from crewai import Crew, Agent, Task, Process
import dotenv
dotenv.load_dotenv()  # Load .env file if it exists

# Optional: Load env vars from .env file
# from dotenv import load_dotenv
# load_dotenv()

# Set your API key (or use .env)
# os.environ["OPENAI_API_KEY"] = "sk-..."


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 1 — Basic Sequential: 3-Step Content Pipeline
# ════════════════════════════════════════════════════════════════════
#
#  Researcher  →  Writer  →  Editor
#  (research)    (draft)    (polish)
#
def example_1_basic_content_pipeline():
    print("\n" + "=" * 60)
    print("EXAMPLE 1 — Basic 3-Step Content Pipeline")
    print("=" * 60)

    # ── Step 1: Define Agents ─────────────────────────────────────
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Research the given topic thoroughly and compile key insights",
        backstory=(
            "You are an expert researcher with 10 years of experience "
            "finding and synthesizing information from diverse sources. "
            "You produce clear, well-organized research notes."
        ),
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write an engaging, well-structured article based on research",
        backstory=(
            "You are a skilled content writer specializing in technology topics. "
            "You transform raw research into compelling narratives that are "
            "accessible to a general audience."
        ),
        verbose=True,
        allow_delegation=False,
    )

    editor = Agent(
        role="Senior Editor",
        goal="Polish and finalize the article for publication",
        backstory=(
            "You are a meticulous editor with a sharp eye for clarity, "
            "grammar, and structure. You ensure every piece meets the "
            "highest publication standards."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Step 2: Define Tasks ──────────────────────────────────────
    # {topic} and {word_count} will be replaced via kickoff(inputs={})
    research_task = Task(
        description=(
            "Research the topic: '{topic}'. "
            "Find key facts, statistics, recent developments, and expert opinions. "
            "Organize your notes clearly with headings."
        ),
        expected_output=(
            "A structured research document with: "
            "1) Overview, 2) Key facts & statistics, "
            "3) Recent developments, 4) Expert perspectives."
        ),
        agent=researcher,  # explicitly assigned
    )

    write_task = Task(
        description=(
            "Using the research provided, write a {word_count}-word article "
            "about '{topic}'. Use an engaging introduction, clear body sections, "
            "and a memorable conclusion."
        ),
        expected_output=(
            "A complete {word_count}-word article in markdown format "
            "with proper headings, an introduction, body, and conclusion."
        ),
        agent=writer,
        context=[research_task],  # receives researcher's output
    )

    edit_task = Task(
        description=(
            "Edit the draft article for clarity, grammar, flow, and impact. "
            "Ensure it reads naturally and is ready for publication. "
            "Make improvements without changing the core message."
        ),
        expected_output=(
            "A polished, publication-ready article in markdown format. "
            "Include a summary of the edits made at the end."
        ),
        agent=editor,
        context=[write_task],  # receives writer's output
    )

    # ── Step 3: Assemble the Crew ─────────────────────────────────
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_task, edit_task],
        process=Process.sequential,  # ← KEY: tasks run in order
        verbose=True,
    )

    # ── Step 4: Kick Off with Dynamic Inputs ─────────────────────
    result = crew.kickoff(inputs={
        "topic": "The Rise of AI Agents in 2025",
        "word_count": "800",
    })

    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 2 — Multi-Context: SEO Content Factory
# ════════════════════════════════════════════════════════════════════
#
#  Keyword Researcher ──┐
#                        ├──→ Writer → SEO Optimizer → Publisher
#  Competitor Analyst ──┘
#
#  Two independent tasks feed INTO the Writer simultaneously.
#
def example_2_multi_context_seo_pipeline():
    print("\n" + "=" * 60)
    print("EXAMPLE 2 — Multi-Context SEO Content Factory")
    print("=" * 60)

    # ── Agents ───────────────────────────────────────────────────
    keyword_researcher = Agent(
        role="SEO Keyword Researcher",
        goal="Find high-value keywords and search intent for the target topic",
        backstory=(
            "You specialize in SEO keyword research using data-driven methods. "
            "You identify primary keywords, long-tail variations, and understand "
            "what users are searching for."
        ),
        verbose=True,
        allow_delegation=False,
    )

    competitor_analyst = Agent(
        role="Competitor Content Analyst",
        goal="Analyze top-ranking competitor content and find content gaps",
        backstory=(
            "You analyze competitor websites to understand what content performs "
            "well in search rankings and identify opportunities to outperform them."
        ),
        verbose=True,
        allow_delegation=False,
    )

    content_writer = Agent(
        role="SEO Content Writer",
        goal="Write SEO-optimized, engaging content that ranks and converts",
        backstory=(
            "You create content that balances search engine optimization with "
            "genuine reader value. You naturally integrate keywords without stuffing."
        ),
        verbose=True,
        allow_delegation=False,
    )

    seo_optimizer = Agent(
        role="On-Page SEO Specialist",
        goal="Optimize the article's technical SEO elements",
        backstory=(
            "You handle meta tags, heading structure, internal linking strategy, "
            "and ensure content meets all on-page SEO best practices."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks ─────────────────────────────────────────────────────
    # These two tasks have NO context dependency — they run independently
    keyword_task = Task(
        description=(
            "Research SEO keywords for the topic: '{topic}'. "
            "Find the primary keyword, 5 secondary keywords, and 3 long-tail keywords. "
            "Estimate search volume and difficulty for each."
        ),
        expected_output=(
            "A keyword research report with: primary keyword, secondary keywords, "
            "long-tail keywords, and search intent analysis."
        ),
        agent=keyword_researcher,
    )

    competitor_task = Task(
        description=(
            "Analyze the top 5 competitor articles about '{topic}'. "
            "Identify: their main angles, content gaps, word counts, "
            "and what makes them rank."
        ),
        expected_output=(
            "A competitor analysis report with: summary of top articles, "
            "identified gaps, recommended content angle, and target word count."
        ),
        agent=competitor_analyst,
    )

    # This task uses BOTH previous tasks as context simultaneously
    write_task = Task(
        description=(
            "Using the keyword research AND competitor analysis, "
            "write a comprehensive article about '{topic}'. "
            "Naturally integrate the target keywords and cover gaps the competitors missed."
        ),
        expected_output=(
            "A complete SEO article with all target keywords naturally integrated, "
            "covering unique angles competitors missed."
        ),
        agent=content_writer,
        context=[keyword_task, competitor_task],  # ← receives BOTH outputs
    )

    optimize_task = Task(
        description=(
            "Optimize the article for on-page SEO. "
            "Write: title tag (60 chars), meta description (155 chars), "
            "H1 and H2 structure, and 3 internal link suggestions."
        ),
        expected_output=(
            "SEO optimization report + optimized article with: "
            "title tag, meta description, heading structure, and internal link plan."
        ),
        agent=seo_optimizer,
        context=[write_task, keyword_task],  # needs the article AND keywords
    )

    # ── Crew ──────────────────────────────────────────────────────
    crew = Crew(
        agents=[keyword_researcher, competitor_analyst, content_writer, seo_optimizer],
        tasks=[keyword_task, competitor_task, write_task, optimize_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "Machine Learning for Beginners"})
    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 3 — Data Analysis Pipeline
# ════════════════════════════════════════════════════════════════════
#
#  Data Collector → Analyst → Visualizer → Report Writer
#
def example_3_data_analysis_pipeline():
    print("\n" + "=" * 60)
    print("EXAMPLE 3 — Data Analysis Pipeline")
    print("=" * 60)

    data_collector = Agent(
        role="Data Collection Specialist",
        goal="Gather and clean raw data about the specified topic",
        backstory=(
            "You specialize in finding, collecting, and cleaning datasets. "
            "You ensure data quality and document any issues found."
        ),
        verbose=True,
        allow_delegation=False,
    )

    analyst = Agent(
        role="Senior Data Analyst",
        goal="Perform statistical analysis and extract meaningful insights",
        backstory=(
            "You have deep expertise in statistical analysis, trend identification, "
            "and turning raw numbers into actionable insights."
        ),
        verbose=True,
        allow_delegation=False,
    )

    report_writer = Agent(
        role="Business Intelligence Writer",
        goal="Transform data insights into clear executive reports",
        backstory=(
            "You bridge the gap between data science and business decision-making "
            "by crafting reports that are both accurate and accessible."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks ─────────────────────────────────────────────────────
    collect_task = Task(
        description=(
            "Collect and describe the dataset for: '{analysis_subject}'. "
            "Document: data sources, variables, sample size, time period, "
            "and any data quality issues."
        ),
        expected_output=(
            "A data inventory document with: source description, "
            "variable definitions, sample stats, and quality notes."
        ),
        agent=data_collector,
    )

    analyze_task = Task(
        description=(
            "Analyze the collected data about '{analysis_subject}'. "
            "Perform: descriptive statistics, trend analysis, correlation analysis, "
            "and identify the top 5 most significant insights."
        ),
        expected_output=(
            "A detailed analysis report with: summary statistics, "
            "identified trends, key correlations, and top 5 insights."
        ),
        agent=analyst,
        context=[collect_task],
    )

    report_task = Task(
        description=(
            "Write an executive summary report on '{analysis_subject}'. "
            "The report must be clear, concise, and include "
            "actionable recommendations based on the analysis."
        ),
        expected_output=(
            "A 1-2 page executive report with: executive summary, "
            "key findings, visualisation descriptions, and 3-5 recommendations."
        ),
        agent=report_writer,
        context=[collect_task, analyze_task],
    )

    crew = Crew(
        agents=[data_collector, analyst, report_writer],
        tasks=[collect_task, analyze_task, report_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"analysis_subject": "Global EV Adoption 2020-2024"})
    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# SEQUENTIAL PROCESS — KEY CONCEPTS SUMMARY
# ════════════════════════════════════════════════════════════════════
"""
PATTERN REFERENCE:

  ┌─────────────────────────────────────────────────────────┐
  │              SEQUENTIAL PROCESS PATTERNS                │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  1. LINEAR CHAIN (most common)                          │
  │     A → B → C                                           │
  │     task_b = Task(..., context=[task_a])                │
  │     task_c = Task(..., context=[task_b])                │
  │                                                         │
  │  2. FORK-AND-JOIN                                       │
  │     A ──┐                                               │
  │          ├──→ C → D                                     │
  │     B ──┘                                               │
  │     task_c = Task(..., context=[task_a, task_b])        │
  │                                                         │
  │  3. BROADCAST (one feeds many)                          │
  │     A → B                                               │
  │     A → C                                               │
  │     task_b = Task(..., context=[task_a])                │
  │     task_c = Task(..., context=[task_a])                │
  │                                                         │
  └─────────────────────────────────────────────────────────┘

WHEN TO USE Sequential:
  ✅ Clear step-by-step pipelines
  ✅ Each step builds on the previous one
  ✅ Predictable, auditable execution
  ✅ Low token cost
  ✅ Easy to debug

WHEN NOT TO USE Sequential:
  ❌ Tasks are completely independent (use Parallel instead)
  ❌ Need dynamic task assignment (use Hierarchical)
  ❌ Task order depends on runtime conditions
"""

# ── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║         CrewAI  —  Process.sequential  Full Lesson           ║
╠══════════════════════════════════════════════════════════════╣
║  Choose which example to run:                                ║
║    1 → Basic Content Pipeline    (Researcher→Writer→Editor)  ║
║    2 → Multi-Context SEO Factory (Fork-and-Join pattern)     ║
║    3 → Data Analysis Pipeline    (Collect→Analyze→Report)    ║
╚══════════════════════════════════════════════════════════════╝
    """)

    choice = input("Enter example number (1/2/3): ").strip()

    if choice == "1":
        example_1_basic_content_pipeline()
    elif choice == "2":
        example_2_multi_context_seo_pipeline()
    elif choice == "3":
        example_3_data_analysis_pipeline()
    else:
        print("Invalid choice. Running Example 1 by default...")
        example_1_basic_content_pipeline()