# CrewAI Research & Blog Writing Pipeline

A production-style example demonstrating all **6 key elements** that make AI agents perform at their best, built with [CrewAI](https://github.com/joaomdmoura/crewAI) and OpenAI GPT-4o.

---

## 📁 Project Structure

```
├── crewai_example.py     # Main pipeline script
├── research_output.md    # Auto-generated: raw research report
├── draft_blog.md         # Auto-generated: first blog draft
├── final_blog.md         # Auto-generated: polished final post
├── crew_run.log          # Auto-generated: full execution log
└── README.md             # This file
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install crewai crewai-tools langchain-openai chromadb
```

### 2. Set environment variables

```bash
export OPENAI_API_KEY="sk-..."        # Required: OpenAI API key
export SERPER_API_KEY="..."           # Required: from https://serper.dev
```

### 3. Run the pipeline

```bash
python crewai_example.py
```

---

## 🧠 The 6 Key Elements Explained

### 1. 🎭 Role Playing

Each agent is given a **role**, **goal**, and **backstory**. This is not cosmetic — it fundamentally changes how the LLM reasons and responds.

| Agent | Role | Why it matters |
|-------|------|----------------|
| `researcher` | Senior AI Research Analyst | Adopts analytical, source-critical mindset |
| `writer` | Technology Content Writer | Produces readable, audience-aware content |
| `editor` | Senior Content Editor | Applies editorial rigor and quality control |

**Example from code:**
```python
researcher = Agent(
    role="Senior AI Research Analyst",
    goal="Search and synthesize accurate information about AI trends in 2025",
    backstory="You are a veteran analyst with 10 years of experience... "
              "You never cite unverified sources..."
)
```

> **Why it works:** The backstory primes the model's context window with persona constraints. A researcher with "10 years of experience" is less likely to hallucinate than a generic assistant.

---

### 2. 🎯 Focus

Tasks are designed with **narrow, explicit scope** to prevent agents from going off-track.

Focus is enforced through:
- **What to do**: specific deliverable format required
- **What to look for**: exact fields expected per trend
- **Where to look**: preferred source domains listed
- **What NOT to do**: explicit prohibitions

**Example from code:**
```python
research_task = Task(
    description=(
        "FOCUS CONSTRAINTS:\n"
        "  - Only use sources published in 2024 or 2025\n"
        "  - Preferred sources: arxiv.org, openai.com, techcrunch.com\n"
        "  - Do NOT include trends without verifiable sources\n"
    )
)
```

> **Why it works:** Vague tasks produce vague outputs. Specific constraints reduce hallucination and off-topic tangents, acting like a lens that concentrates the agent's reasoning.

---

### 3. 🛠️ Tools

Tools extend agents beyond what the LLM knows from training data. Without tools, agents can only reason from their training cutoff.

| Tool | Agent | Purpose |
|------|-------|---------|
| `SerperDevTool` | researcher | Real-time Google search for 2025 data |

**Example from code:**
```python
from crewai.tools import SerperDevTool

search_tool = SerperDevTool(
    n_results=10,   # Fetch top 10 results per query
    country="us",
    locale="en"
)

researcher = Agent(
    tools=[search_tool],  # Only the researcher needs web access
    ...
)
```

> **Why it works:** The writer and editor don't need search tools — giving tools only to agents that need them reduces cost and prevents misuse. The researcher grounds findings in real, current data rather than hallucinated facts.

---

### 4. 🛡️ Guardrails

Guardrails prevent agents from running out of control. They operate at three levels:

**A) Iteration limits** — stop infinite loops
```python
researcher = Agent(max_iter=5)   # Max 5 reasoning steps
writer     = Agent(max_iter=3)
editor     = Agent(max_iter=3)
```

**B) Rate limits** — prevent API overuse
```python
researcher = Agent(max_rpm=10)   # Max 10 API calls/minute
crew = Crew(max_rpm=20)          # Max 20 across entire crew
```

**C) Behavioral rules in task descriptions** — enforce output constraints
```python
write_task = Task(
    description=(
        "GUARDRAIL RULES:\n"
        "  - Write entirely in Vietnamese\n"
        "  - Do NOT add facts not in the research report\n"
        "  - Target reading level: general tech audience\n"
    )
)
```

> **Why it works:** LLMs can loop, over-generate, or hallucinate without boundaries. Guardrails define acceptable behavior before the agent starts, not after problems occur.

---

### 5. 🤝 Cooperation

Agents share work through two mechanisms:

**A) Task context** — pass one task's output to another
```python
write_task = Task(
    context=[research_task],  # Writer receives researcher's full output
    agent=writer
)

edit_task = Task(
    context=[research_task, write_task],  # Editor sees both research AND draft
    agent=editor
)
```

**B) Sequential process** — enforces a defined execution order
```python
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential   # Runs in order: research -> write -> edit
)
```

**Data flow:**
```
research_task output
        |
        v
write_task (context = research)
        |
        v
edit_task (context = research + draft)
        |
        v
   final_blog.md
```

> **Why it works:** Each agent builds on verified, structured input from the previous agent. The editor can cross-check the draft against the original research to catch invented facts.

---

### 6. 🧠 Memory

Memory allows agents to retain and reuse information. When `memory=True` is set at the crew level, **three memory types** are activated simultaneously:

| Memory Type | Storage | Scope | Purpose |
|-------------|---------|-------|---------|
| **Short-term** | ChromaDB (RAG) | Current run only | Agents share context within a single run |
| **Long-term** | SQLite (`~/.crewai/`) | Across runs | Crew learns from past executions |
| **Entity** | ChromaDB (RAG) | Current run only | Tracks people, orgs, concepts mentioned |

**Example from code:**
```python
crew = Crew(
    memory=True,              # Activates all 3 memory types
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"  # Used by ChromaDB for RAG
        }
    }
)
```

**How memory improves results:**
- The writer remembers what the researcher found — no need to repeat context
- On the second run about a similar topic, the crew recalls prior strategies
- Entity memory ensures "OpenAI" is consistently treated as an organization

> **Why it works:** Without memory, each agent starts from scratch on every step. Memory creates continuity, reduces redundant processing, and enables learning across sessions.

---

## 🔄 Full Pipeline Flow

```
+----------------------------------------------------------+
|                    CREW KICKOFF                           |
+------------------------+---------------------------------+
                         |
             +-----------v-----------+
             |   RESEARCHER AGENT    |
             |  Role: Research Analyst|
             |  Tools: SerperDevTool  |
             |  Guardrail: max_iter=5 |
             |  Memory: YES           |
             +-----------+-----------+
                         | research_output.md
             +-----------v-----------+
             |    WRITER AGENT       |
             |  Role: Content Writer  |
             |  Tools: None           |
             |  Guardrail: max_iter=3 |
             |  Context: research     |
             |  Memory: YES           |
             +-----------+-----------+
                         | draft_blog.md
             +-----------v-----------+
             |    EDITOR AGENT       |
             |  Role: Content Editor  |
             |  Tools: None           |
             |  Guardrail: max_iter=3 |
             |  Context: both         |
             |  Memory: YES           |
             +-----------+-----------+
                         |
                   final_blog.md
```

---

## ⚙️ Configuration Reference

```python
# Agent parameters
Agent(
    role="...",           # Persona title
    goal="...",           # What the agent is optimizing for
    backstory="...",      # Context that shapes reasoning style
    tools=[...],          # List of tools the agent can use
    llm=llm,              # Language model to use
    memory=True,          # Enable agent-level memory
    max_iter=5,           # Max reasoning iterations (guardrail)
    max_rpm=10,           # Max API calls per minute (guardrail)
    verbose=True,         # Print step-by-step reasoning
    allow_delegation=False # Prevent passing tasks to other agents
)

# Task parameters
Task(
    description="...",      # Detailed instructions (focus + guardrails)
    expected_output="...",  # What the output should look like
    agent=agent,            # Which agent handles this task
    context=[other_task],   # Inputs from previous tasks (cooperation)
    output_file="out.md"    # Save output to file automatically
)

# Crew parameters
Crew(
    agents=[...],                   # All agents in the pipeline
    tasks=[...],                    # All tasks in order
    process=Process.sequential,     # Execution mode
    memory=True,                    # Enable all 3 memory types
    embedder={...},                 # Embedding model for RAG memory
    max_rpm=20,                     # Crew-wide rate limit (guardrail)
    verbose=True,
    output_log_file="run.log"       # Save full execution log
)
```

---

## 💡 Key Takeaways

| Element | Without It | With It |
|---------|-----------|---------|
| Role Playing | Generic, inconsistent outputs | Consistent, persona-appropriate responses |
| Focus | Off-topic, overly broad results | Precise, structured deliverables |
| Tools | Limited to training data | Access to real-time information |
| Guardrails | Infinite loops, hallucination risk | Predictable, bounded behavior |
| Cooperation | Isolated, disconnected agents | Compounding quality through the pipeline |
| Memory | Repeats work, no learning | Context-aware, improving over time |

---

## 📄 License

MIT License — free to use and modify for educational and commercial purposes.