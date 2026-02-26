"""
============================================================
  CrewAI — Process.hierarchical  |  Full Lesson File
============================================================

CONCEPT:
  Hierarchical Process automatically creates a Manager Agent
  that orchestrates all other agents. The Manager decides:
    - Which agent handles which task
    - The optimal execution order
    - Whether to retry or reassign a task

  Structure:
              Manager Agent  (LLM-powered)
             /      |        \
       [Agent A] [Agent B] [Agent C]
             \      |        /
                  Result

KEY DIFFERENCES from Sequential:
  • You do NOT need to assign agent= to each task
    (Manager decides at runtime)
  • manager_llm= is REQUIRED
  • More flexible but higher token cost
  • Use a powerful model for manager_llm (GPT-4o, Claude)

KEY RULES:
  • Always provide manager_llm= in the Crew
  • Tasks can have agent= (guided) or not (fully dynamic)
  • Manager can delegate sub-tasks between agents
  • Enable allow_delegation=True for agents that may sub-delegate

INSTALL:
  pip install crewai crewai-tools langchain-openai

============================================================
"""

# ── Imports ─────────────────────────────────────────────────────────
import os
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

# Optional: Load env vars from .env file
# from dotenv import load_dotenv
# load_dotenv()

# os.environ["OPENAI_API_KEY"] = "sk-..."

# ── Manager LLM Setup ────────────────────────────────────────────────
# CRITICAL: Use a capable model — the Manager drives the entire crew.
# GPT-4o, Claude 3.5 Sonnet, or better recommended.
manager_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,   # low temperature = more consistent decisions
)


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 1 — Investment Research Platform
# ════════════════════════════════════════════════════════════════════
#
#  Manager dynamically coordinates:
#    Financial Analyst, Risk Specialist, Market Researcher, Writer
#
def example_1_investment_research():
    print("\n" + "=" * 60)
    print("EXAMPLE 1 — Investment Research Platform")
    print("=" * 60)

    # ── Agents ───────────────────────────────────────────────────
    financial_analyst = Agent(
        role="Financial Data Analyst",
        goal=(
            "Analyze financial statements, earnings, revenue trends, "
            "and key financial metrics for the target company"
        ),
        backstory=(
            "You are a CFA charterholder with 15 years of experience in "
            "quantitative financial analysis. You specialize in reading balance "
            "sheets, income statements, and deriving meaningful metrics."
        ),
        verbose=True,
        allow_delegation=False,
    )

    risk_specialist = Agent(
        role="Risk Management Specialist",
        goal=(
            "Identify, quantify, and categorize all material investment risks "
            "including market, operational, regulatory, and ESG risks"
        ),
        backstory=(
            "Former hedge fund risk manager with expertise in building risk "
            "matrices. You think in probabilities and impact scenarios, "
            "producing actionable risk assessments."
        ),
        verbose=True,
        allow_delegation=False,
    )

    market_researcher = Agent(
        role="Market & Competitive Intelligence Analyst",
        goal=(
            "Research the company's market position, industry dynamics, "
            "competitive landscape, and growth opportunities"
        ),
        backstory=(
            "You are a senior industry analyst who tracks market trends, "
            "competitive movements, and macroeconomic factors. You have "
            "deep expertise in market sizing and competitive benchmarking."
        ),
        verbose=True,
        allow_delegation=False,
    )

    report_writer = Agent(
        role="Investment Report Author",
        goal=(
            "Synthesize all research into a compelling, accurate "
            "investment research report with a clear recommendation"
        ),
        backstory=(
            "Former equity research analyst at a top-tier investment bank. "
            "You write reports that are both rigorous and accessible, "
            "with a clear buy/hold/sell thesis backed by evidence."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks (NO agent= needed — Manager will assign) ────────────
    financial_task = Task(
        description=(
            "Conduct a thorough financial analysis of {company}. "
            "Cover: revenue growth, profit margins, debt levels, cash flow, "
            "P/E ratio vs peers, and a 3-year financial trend summary."
        ),
        expected_output=(
            "Financial analysis report covering: revenue trends, margin analysis, "
            "balance sheet health, cash flow status, and valuation multiples."
        ),
        # No agent= — Manager decides who does this
    )

    risk_task = Task(
        description=(
            "Assess all material investment risks for {company}. "
            "Include: market risks, business risks, regulatory risks, "
            "ESG risks, and rate each on probability (H/M/L) and impact (H/M/L)."
        ),
        expected_output=(
            "A risk matrix document categorizing risks by type, probability, "
            "and impact, with 3-5 key risk mitigants identified."
        ),
    )

    market_task = Task(
        description=(
            "Research {company}'s market position. Analyze: total addressable market, "
            "market share trends, top 3 competitors, competitive advantages (moat), "
            "and key growth catalysts for the next 2-3 years."
        ),
        expected_output=(
            "Market intelligence report with: TAM analysis, market share data, "
            "competitive benchmarking, moat assessment, and growth catalysts."
        ),
    )

    final_report_task = Task(
        description=(
            "Write a comprehensive equity research report on {company}. "
            "Synthesize all financial, risk, and market research. "
            "Include a clear investment thesis and Buy / Hold / Sell recommendation "
            "with a 12-month price target rationale."
        ),
        expected_output=(
            "A 5-7 page investment research report with: executive summary, "
            "investment thesis, financial highlights, risk factors, market analysis, "
            "and a final Buy/Hold/Sell recommendation with price target."
        ),
    )

    # ── Crew with Hierarchical Process ───────────────────────────
    crew = Crew(
        agents=[financial_analyst, risk_specialist, market_researcher, report_writer],
        tasks=[financial_task, risk_task, market_task, final_report_task],
        process=Process.hierarchical,   # ← KEY
        manager_llm=manager_llm,         # ← REQUIRED
        verbose=True,
    )

    result = crew.kickoff(inputs={"company": "Tesla (TSLA)"})
    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 2 — Software Project Planning System
# ════════════════════════════════════════════════════════════════════
#
#  Manager coordinates: Tech Lead, UX Designer, Backend Dev,
#  Frontend Dev, QA Engineer → Project Plan
#
def example_2_software_project_planning():
    print("\n" + "=" * 60)
    print("EXAMPLE 2 — Software Project Planning System")
    print("=" * 60)

    tech_lead = Agent(
        role="Technical Lead Architect",
        goal=(
            "Define the technical architecture, tech stack decisions, "
            "and high-level system design for the project"
        ),
        backstory=(
            "10+ years as a software architect. You make pragmatic technology "
            "choices, define system boundaries, and identify technical risks early. "
            "You think in terms of scalability, maintainability, and team capability."
        ),
        verbose=True,
        allow_delegation=True,   # Can delegate sub-tasks to others
    )

    ux_designer = Agent(
        role="Senior UX Designer",
        goal=(
            "Define the user experience, information architecture, "
            "key user flows, and UI component requirements"
        ),
        backstory=(
            "Specialist in user-centered design with experience shipping "
            "products used by millions. You define wireframes in words, "
            "user personas, and design systems."
        ),
        verbose=True,
        allow_delegation=False,
    )

    backend_dev = Agent(
        role="Senior Backend Developer",
        goal=(
            "Define the API design, database schema, "
            "backend services, and integration requirements"
        ),
        backstory=(
            "Expert in building scalable APIs and data systems. "
            "You think through data models, service boundaries, "
            "authentication patterns, and third-party integrations."
        ),
        verbose=True,
        allow_delegation=False,
    )

    frontend_dev = Agent(
        role="Senior Frontend Developer",
        goal=(
            "Define frontend architecture, component structure, "
            "state management strategy, and performance requirements"
        ),
        backstory=(
            "Expert in modern frontend frameworks (React/Vue/Next.js). "
            "You define component hierarchies, routing logic, and "
            "performance optimization strategies."
        ),
        verbose=True,
        allow_delegation=False,
    )

    project_manager = Agent(
        role="Technical Project Manager",
        goal=(
            "Compile all technical inputs into a complete project plan "
            "with milestones, timeline estimates, and team structure"
        ),
        backstory=(
            "Experienced PM who has delivered 50+ software projects. "
            "You translate technical requirements into actionable sprint plans, "
            "resource allocations, and realistic timelines."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks ─────────────────────────────────────────────────────
    architecture_task = Task(
        description=(
            "Define the technical architecture for building: '{project_description}'. "
            "Cover: recommended tech stack, system components, scalability approach, "
            "and top 3 technical risks."
        ),
        expected_output=(
            "Architecture document with: tech stack recommendation, "
            "system diagram description, scalability notes, and risk log."
        ),
    )

    ux_task = Task(
        description=(
            "Define the UX/UI requirements for: '{project_description}'. "
            "Include: primary user personas (2-3), key user flows (3-5), "
            "core screens needed, and design system requirements."
        ),
        expected_output=(
            "UX specification with: user personas, user flow descriptions, "
            "screen inventory, and design system notes."
        ),
    )

    backend_task = Task(
        description=(
            "Design the backend specification for: '{project_description}'. "
            "Define: core API endpoints (RESTful or GraphQL), "
            "database schema overview, authentication strategy, "
            "and third-party integrations needed."
        ),
        expected_output=(
            "Backend spec with: API endpoint list, database schema overview, "
            "auth approach, and integration requirements."
        ),
    )

    frontend_task = Task(
        description=(
            "Define the frontend specification for: '{project_description}'. "
            "Include: framework recommendation, core component list, "
            "state management strategy, routing structure, and performance targets."
        ),
        expected_output=(
            "Frontend spec with: framework choice + rationale, component tree, "
            "state management plan, routing map, and performance KPIs."
        ),
    )

    project_plan_task = Task(
        description=(
            "Compile all technical specifications into a complete project plan "
            "for: '{project_description}'. "
            "Create: work breakdown structure, milestone timeline (in weeks), "
            "team size recommendation, and MVP scope definition."
        ),
        expected_output=(
            "Complete project plan with: WBS, milestone timeline, team composition, "
            "MVP scope, and delivery estimate."
        ),
    )

    crew = Crew(
        agents=[tech_lead, ux_designer, backend_dev, frontend_dev, project_manager],
        tasks=[architecture_task, ux_task, backend_task, frontend_task, project_plan_task],
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
    )

    result = crew.kickoff(inputs={
        "project_description": (
            "A SaaS platform for freelancers to manage invoices, "
            "clients, and payments with AI-powered financial insights"
        )
    })
    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# EXAMPLE 3 — Custom Manager Agent (Advanced)
# ════════════════════════════════════════════════════════════════════
#
#  You can also provide a CUSTOM Manager Agent with specific
#  role, goal, and backstory — for fine-grained control.
#
def example_3_custom_manager():
    print("\n" + "=" * 60)
    print("EXAMPLE 3 — Custom Manager Agent")
    print("=" * 60)

    # ── Define a custom Manager Agent ─────────────────────────────
    custom_manager = Agent(
        role="Chief Research Coordinator",
        goal=(
            "Coordinate the research team to produce a comprehensive, "
            "accurate, and actionable market research report. "
            "Ensure each specialist contributes their expertise fully."
        ),
        backstory=(
            "You are an experienced research director who has coordinated "
            "hundreds of market research projects. You know exactly which "
            "specialist to assign each task to, and you hold high standards "
            "for the quality and completeness of deliverables."
        ),
        verbose=True,
        allow_delegation=True,   # Manager MUST allow delegation
    )

    # ── Specialist Agents ─────────────────────────────────────────
    trend_analyst = Agent(
        role="Market Trend Analyst",
        goal="Identify and analyze emerging trends in the target market",
        backstory="Expert in identifying market signals before they become mainstream.",
        verbose=True,
        allow_delegation=False,
    )

    consumer_researcher = Agent(
        role="Consumer Behavior Researcher",
        goal="Understand consumer needs, pain points, and purchase drivers",
        backstory="Specialist in qualitative and quantitative consumer research methods.",
        verbose=True,
        allow_delegation=False,
    )

    competitive_analyst = Agent(
        role="Competitive Intelligence Analyst",
        goal="Map the competitive landscape and identify strategic opportunities",
        backstory="Former strategy consultant with deep expertise in competitive benchmarking.",
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks ─────────────────────────────────────────────────────
    trend_task = Task(
        description="Identify top 5 emerging trends in the '{market}' market for 2025-2026.",
        expected_output="Trend report with: trend name, description, evidence, and business impact.",
    )

    consumer_task = Task(
        description=(
            "Research consumer behavior in the '{market}' market. "
            "Identify: top 3 pain points, key purchase drivers, and demographic insights."
        ),
        expected_output="Consumer research summary with pain points, drivers, and persona sketches.",
    )

    competitive_task = Task(
        description=(
            "Map the competitive landscape for the '{market}' market. "
            "Identify top 5 players, their strengths/weaknesses, and 2 white-space opportunities."
        ),
        expected_output="Competitive map with player profiles, SWOT summary, and opportunity gaps.",
    )

    synthesis_task = Task(
        description=(
            "Synthesize trend, consumer, and competitive research for the '{market}' market "
            "into an executive market research report with strategic recommendations."
        ),
        expected_output=(
            "Executive market research report (3-4 pages) with: market overview, "
            "trend highlights, consumer insights, competitive analysis, and 3 strategic recommendations."
        ),
    )

    # ── Crew with Custom Manager ───────────────────────────────────
    crew = Crew(
        agents=[trend_analyst, consumer_researcher, competitive_analyst],
        tasks=[trend_task, consumer_task, competitive_task, synthesis_task],
        process=Process.hierarchical,
        manager_agent=custom_manager,   # ← Use manager_agent= for custom manager
        # NOTE: When using manager_agent=, do NOT also set manager_llm=
        verbose=True,
    )

    result = crew.kickoff(inputs={"market": "AI-powered productivity tools"})
    print("\n[RESULT]\n", result)
    return result


# ════════════════════════════════════════════════════════════════════
# HIERARCHICAL PROCESS — KEY CONCEPTS SUMMARY
# ════════════════════════════════════════════════════════════════════
"""
TWO WAYS TO SET THE MANAGER:

  Option A — Auto Manager (manager_llm):
    crew = Crew(
        agents=[...], tasks=[...],
        process=Process.hierarchical,
        manager_llm=ChatOpenAI(model="gpt-4o")  ← LLM powers auto manager
    )

  Option B — Custom Manager Agent (manager_agent):
    crew = Crew(
        agents=[...], tasks=[...],
        process=Process.hierarchical,
        manager_agent=my_custom_manager_agent   ← Full Agent object
    )
    NOTE: Do NOT use both manager_llm and manager_agent together.

TASK ASSIGNMENT MODES:

  Mode 1 — Fully Dynamic (no agent=):
    task = Task(description="...", expected_output="...")
    → Manager picks the best agent at runtime

  Mode 2 — Guided (with agent=):
    task = Task(description="...", expected_output="...", agent=specific_agent)
    → Manager is guided toward a specific agent, but can override

ALLOW DELEGATION:
  • Manager agent: MUST have allow_delegation=True (default)
  • Worker agents: allow_delegation=False (default, recommended)
    → Set True if you want agents to sub-delegate to each other

WHEN TO USE Hierarchical:
  ✅ Tasks need dynamic assignment based on content
  ✅ Complex projects with many specialists
  ✅ Quality matters more than token cost
  ✅ Tasks may need revision or retry
  ✅ You want autonomous coordination

WHEN NOT TO USE Hierarchical:
  ❌ Simple, fixed-order pipelines (use Sequential)
  ❌ Tight token budget (Manager adds overhead)
  ❌ Tasks are completely independent (use Parallel)
"""

# ── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║       CrewAI  —  Process.hierarchical  Full Lesson           ║
╠══════════════════════════════════════════════════════════════╣
║  Choose which example to run:                                ║
║    1 → Investment Research     (Financial+Risk+Market+Write) ║
║    2 → Software Project Plan   (Tech+UX+Backend+Frontend+PM) ║
║    3 → Custom Manager Agent    (Advanced: manager_agent=)    ║
╚══════════════════════════════════════════════════════════════╝
    """)

    choice = input("Enter example number (1/2/3): ").strip()

    if choice == "1":
        example_1_investment_research()
    elif choice == "2":
        example_2_software_project_planning()
    elif choice == "3":
        example_3_custom_manager()
    else:
        print("Invalid choice. Running Example 1 by default...")
        example_1_investment_research()