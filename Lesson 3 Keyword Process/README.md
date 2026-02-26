# CrewAI — `Process` Keyword: Complete Lesson

> **A production-ready guide** to understanding and applying the `Process` parameter in CrewAI multi-agent systems. Includes full code examples, patterns, decision guides, and best practices.

---

## 📁 Files in This Lesson

| File | Description |
|---|---|
| `sequential.py` | 3 full examples of `Process.sequential` with detailed comments |
| `hierarchical.py` | 3 full examples of `Process.hierarchical` with detailed comments |
| `README.md` | This file — complete reference guide |

---

## Table of Contents

1. [What is `Process`?](#1-what-is-process)
2. [Quick Start](#2-quick-start)
3. [Sequential Process — Deep Dive](#3-sequential-process--deep-dive)
4. [Hierarchical Process — Deep Dive](#4-hierarchical-process--deep-dive)
5. [Parallel Processing (Unofficial)](#5-parallel-processing-unofficial)
6. [Hybrid Pattern](#6-hybrid-pattern)
7. [Side-by-Side Comparison](#7-side-by-side-comparison)
8. [Decision Guide](#8-decision-guide)
9. [Best Practices](#9-best-practices)
10. [Common Mistakes & Fixes](#10-common-mistakes--fixes)
11. [Quick Reference Cheatsheet](#11-quick-reference-cheatsheet)
12. [Running the Examples](#12-running-the-examples)

---

## 1. What is `Process`?

`Process` is the **orchestration engine** of a CrewAI `Crew`. It defines *how* agents collaborate to complete a set of tasks:

- **In what order** tasks are executed
- **Who decides** which agent handles which task
- **How information flows** between tasks and agents

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential     # <- This is what we are learning
)
```

CrewAI provides **two official `Process` types**:

| Process | Who Coordinates | Flexibility | Token Cost |
|---|---|---|---|
| `Process.sequential` | You (via task order + context) | Low | Low |
| `Process.hierarchical` | Manager Agent (AI-powered) | High | Higher |

> Parallel processing is achievable with Python `asyncio` or `ThreadPoolExecutor` — not a built-in Process type yet.

---

## 2. Quick Start

### Installation

```bash
pip install crewai crewai-tools langchain-openai python-dotenv
```

### Minimal Sequential Example

```python
import os
from crewai import Crew, Agent, Task, Process

os.environ["OPENAI_API_KEY"] = "sk-..."

writer = Agent(role="Writer", goal="Write content", backstory="Expert writer")
editor = Agent(role="Editor", goal="Edit content", backstory="Senior editor")

write_task = Task(description="Write an article about AI",
                  expected_output="500-word article", agent=writer)
edit_task  = Task(description="Edit the article",
                  expected_output="Polished article", agent=editor,
                  context=[write_task])   # pass output forward

crew = Crew(agents=[writer, editor], tasks=[write_task, edit_task],
            process=Process.sequential)

result = crew.kickoff()
print(result)
```

---

## 3. Sequential Process — Deep Dive

### 3.1 Concept & Flow

Tasks execute in the **exact order** they are listed. Each task can access previous tasks' outputs via `context`.

```
Task_1 --> Task_2 --> Task_3 --> Task_N
  ^            ^           ^
(output)   (context)  (context)
```

**Key characteristics:**
- **Deterministic** — Same input produces same execution path
- **Transparent** — Easy to understand, trace, and debug
- **Sequential** — No task starts until the previous one finishes
- **Context-aware** — Each task can see outputs from any prior task

### 3.2 The `context` Parameter

`context` is what connects tasks. Without it, each task runs independently.

```python
# Task A: no context needed (runs first)
task_a = Task(
    description="Research {topic}",
    expected_output="Research notes",
    agent=researcher
)

# Task B: receives Task A's output
task_b = Task(
    description="Write article based on research",
    expected_output="Draft article",
    agent=writer,
    context=[task_a]    # task_b sees task_a's output
)

# Task C: receives outputs from BOTH A and B
task_c = Task(
    description="Optimize the article using keywords",
    expected_output="SEO-optimized article",
    agent=optimizer,
    context=[task_a, task_b]    # receives both outputs
)
```

### 3.3 Three Sequential Patterns

#### Pattern 1 — Linear Chain (most common)
```
A -> B -> C -> D
```
```python
task_b = Task(..., context=[task_a])
task_c = Task(..., context=[task_b])
task_d = Task(..., context=[task_c])
```
Use when: Steps build directly on each other (research -> draft -> edit -> publish)

---

#### Pattern 2 — Fork-and-Join
```
Task_A --+
          +--> Task_C -> Task_D
Task_B --+
```
```python
task_a = Task(description="Research keywords", ...)      # independent
task_b = Task(description="Analyze competitors", ...)    # independent
task_c = Task(
    description="Write SEO article using keyword research AND competitive analysis",
    context=[task_a, task_b],    # joins the two streams
    ...
)
```
Use when: Two types of research/input needed before the next step.

---

#### Pattern 3 — Broadcast
```
Task_A --> Task_B
       +-> Task_C
```
```python
task_a = Task(description="Research the company", ...)

task_b = Task(description="Write financial analysis", context=[task_a], ...)
task_c = Task(description="Write risk assessment",   context=[task_a], ...)
```
Use when: One research task feeds multiple specialist analyses.

### 3.4 Dynamic Inputs

```python
task = Task(
    description="Write a {length}-word article about {topic} for {audience}",
    expected_output="A {length}-word article targeting {audience}",
    agent=writer
)

crew.kickoff(inputs={
    "topic": "Quantum Computing",
    "length": "1000",
    "audience": "developers"
})
```

---

## 4. Hierarchical Process — Deep Dive

### 4.1 Concept & Flow

CrewAI creates a **Manager Agent** that acts as an intelligent project manager:

1. Receives all task descriptions
2. Analyzes which agent is best suited for each task
3. Delegates tasks with specific instructions
4. Evaluates output quality
5. Requests revisions if unsatisfied
6. Assembles the final result

```
              Manager Agent  (GPT-4o / Claude Opus)
             /       |        \
       [Agent A] [Agent B] [Agent C]
             \       |        /
               Final Result
```

### 4.2 Manager Setup: Two Options

#### Option A — Auto Manager via `manager_llm` (most common)

```python
from langchain_openai import ChatOpenAI

crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.1)
)
```

**Best LLMs for `manager_llm`:**
- `gpt-4o` — Recommended (best balance of intelligence and speed)
- `claude-3-5-sonnet` — Excellent for complex coordination
- `gpt-4-turbo` — Strong alternative

#### Option B — Custom Manager Agent via `manager_agent`

```python
custom_manager = Agent(
    role="Chief Research Coordinator",
    goal="Coordinate the research team to produce a comprehensive report",
    backstory="Experienced research director with 20 years in the field",
    allow_delegation=True,   # MUST be True for manager agents
    verbose=True
)

crew = Crew(
    agents=[agent1, agent2, agent3],   # does NOT include the manager
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_agent=custom_manager       # use manager_agent= for custom manager
    # Do NOT also set manager_llm= when using manager_agent=
)
```

### 4.3 Task Assignment Modes

#### Mode 1 — Fully Dynamic (no `agent=`)

The Manager independently decides which agent handles each task at runtime.

```python
task = Task(
    description="Analyze the financial statements of {company}",
    expected_output="Financial analysis report"
    # No agent= — Manager decides
)
```

Best for: Complex projects where you want maximum AI autonomy.

#### Mode 2 — Guided (with `agent=`)

Suggest an agent to the Manager. The Manager generally respects this but can override.

```python
task = Task(
    description="Analyze the financial statements of {company}",
    expected_output="Financial analysis report",
    agent=financial_analyst   # Manager is guided toward this agent
)
```

Best for: When you know which specialist fits best.

### 4.4 Full Example

```python
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

manager_llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

financial_analyst = Agent(
    role="Financial Analyst",
    goal="Analyze financial statements and metrics",
    backstory="CFA with 15 years quantitative analysis experience",
    verbose=True, allow_delegation=False
)
risk_specialist = Agent(
    role="Risk Specialist",
    goal="Identify and quantify investment risks",
    backstory="Former hedge fund risk manager",
    verbose=True, allow_delegation=False
)
report_writer = Agent(
    role="Investment Report Writer",
    goal="Write compelling investment research reports",
    backstory="Former equity research analyst at top investment bank",
    verbose=True, allow_delegation=False
)

# No agent= assignment — Manager decides who does what
financial_task = Task(
    description="Analyze Q4 2024 financials of {company}: revenue, margins, debt, cash flow",
    expected_output="Financial analysis with trend summary and valuation multiples"
)
risk_task = Task(
    description="Assess investment risks for {company}: market, business, regulatory, ESG",
    expected_output="Risk matrix with probability/impact scores and key mitigants"
)
report_task = Task(
    description="Write an investment report on {company} with Buy/Hold/Sell recommendation",
    expected_output="5-page investment report with thesis and 12-month price target"
)

crew = Crew(
    agents=[financial_analyst, risk_specialist, report_writer],
    tasks=[financial_task, risk_task, report_task],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    verbose=True
)

result = crew.kickoff(inputs={"company": "Tesla (TSLA)"})
print(result)
```

---

## 5. Parallel Processing (Unofficial)

CrewAI does not have `Process.parallel` as of mid-2025. Use Python concurrency:

### Option A — `asyncio.gather` (Recommended)

```python
import asyncio
from crewai import Crew, Agent, Task, Process

def make_crew(market: str) -> Crew:
    agent = Agent(role=f"{market} Analyst", goal="Analyze market",
                  backstory=f"Expert in {market} markets")
    task = Task(description=f"Analyze {market} market: trends, opportunities, risks",
                expected_output=f"{market} analysis report", agent=agent)
    return Crew(agents=[agent], tasks=[task], process=Process.sequential)

async def run_all():
    markets = ["US", "EU", "Asia", "LatAm"]
    crews = [make_crew(m) for m in markets]
    results = await asyncio.gather(
        *[asyncio.to_thread(crew.kickoff) for crew in crews]
    )
    return dict(zip(markets, results))

results = asyncio.run(run_all())
```

### Option B — `ThreadPoolExecutor` (Simpler)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from crewai import Crew, Agent, Task, Process

def analyze_market(market: str) -> tuple[str, str]:
    agent = Agent(role=f"{market} Analyst", goal="Analyze", backstory="Expert")
    task = Task(description=f"Analyze {market}", expected_output="Report", agent=agent)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
    return market, crew.kickoff()

results = {}
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(analyze_market, m): m for m in ["US", "EU", "Asia"]}
    for future in as_completed(futures):
        market, result = future.result()
        results[market] = result
```

---

## 6. Hybrid Pattern

Combine parallel research with sequential synthesis.

```python
import asyncio
from crewai import Crew, Agent, Task, Process

# Phase 1: Research all topics at the same time (parallel)
async def parallel_research(topics: list[str]) -> list[str]:
    async def research_one(topic: str) -> str:
        agent = Agent(role="Researcher", goal="Research thoroughly", backstory="Expert")
        task = Task(description=f"Deep research on: {topic}",
                    expected_output="Research notes", agent=agent)
        return await asyncio.to_thread(Crew(agents=[agent], tasks=[task]).kickoff)
    return await asyncio.gather(*[research_one(t) for t in topics])

# Phase 2: Synthesize then write (sequential — order matters)
def sequential_write(research_results: list) -> str:
    combined = "\n\n---\n\n".join(str(r) for r in research_results)
    synthesizer = Agent(role="Synthesizer", goal="Combine research", backstory="Analyst")
    writer = Agent(role="Writer", goal="Write report", backstory="Technical writer")
    t1 = Task(description=f"Synthesize:\n{combined}",
              expected_output="Unified insights", agent=synthesizer)
    t2 = Task(description="Write 2000-word report from synthesis",
              expected_output="Final report", agent=writer, context=[t1])
    return Crew(agents=[synthesizer, writer], tasks=[t1, t2],
                process=Process.sequential).kickoff()

async def main():
    topics = ["AI in Healthcare", "AI in Finance", "AI in Education"]
    research = await parallel_research(topics)   # fast — all at once
    report = sequential_write(research)           # ordered — synthesis before writing
    print(report)

asyncio.run(main())
```

---

## 7. Side-by-Side Comparison

| Criteria | Sequential | Hierarchical | Parallel (asyncio) |
|---|---|---|---|
| **Coordination** | You define order | Manager decides | Independent |
| **Token Cost** | Lowest | Highest (Manager overhead) | Medium |
| **Code Complexity** | Simplest | Moderate | Moderate |
| **Flexibility** | Low | Very High | High |
| **Execution Speed** | Slowest (linear) | Medium | Fastest |
| **Debuggability** | Easy | Harder | Medium |
| **`manager_llm` required** | No | Yes | No |
| **Task order guaranteed** | Yes | No (Manager decides) | No (concurrent) |
| **Best For** | Clear pipelines | Complex dynamic tasks | Independent tasks |

---

## 8. Decision Guide

```
Q1: Do tasks need to happen in a FIXED, KNOWN order,
    where each step depends on the previous?

    YES ──────────────────────────> Process.sequential
    NO  --> Continue to Q2

Q2: Is the task assignment COMPLEX or DYNAMIC?
    (Not sure which agent should do what,
     or tasks may need quality checks and retries)

    YES ──────────────────────────> Process.hierarchical
                                    (use strong manager_llm)
    NO  --> Continue to Q3

Q3: Are tasks COMPLETELY INDEPENDENT of each other,
    and SPEED is a priority?

    YES ──────────────────────────> asyncio / ThreadPool
    NO  -->  Default to Process.sequential (simplest to start)
```

**Real-world mapping:**

| Use Case | Recommended Process |
|---|---|
| Research -> Write -> Edit | `sequential` |
| News aggregation (5 sources at once) | `asyncio` parallel |
| AI product feature planning (multiple specialists) | `hierarchical` |
| Data: Collect -> Analyze -> Report | `sequential` |
| Market analysis (US + EU + Asia at once) | `asyncio` parallel |
| Investment due diligence (dynamic assignment) | `hierarchical` |
| SEO: keywords + competitors -> write -> optimize | `sequential` (fork-and-join) |

---

## 9. Best Practices

**General:**
- Set `verbose=True` during development to see what each agent is doing
- Write `expected_output` clearly and specifically — it directly drives output quality
- Use `{variable}` placeholders + `crew.kickoff(inputs={...})` for reusable pipelines
- Test with a cheap model (`gpt-4o-mini`) first, then upgrade when satisfied

**Sequential-specific:**
- Map your pipeline on paper before coding — draw the A -> B -> C flow
- Always use `context=[prev_task]` to connect tasks — without it, agents work in isolation
- Avoid more than 6-7 tasks in one crew — split into sub-crews if needed
- Name tasks clearly: `research_task`, `write_task`, not `task1`, `task2`

**Hierarchical-specific:**
- Use a powerful LLM for `manager_llm` — GPT-4o or Claude 3.5+ is strongly recommended
- Set `allow_delegation=False` on worker agents unless they truly need to sub-delegate
- Write detailed `backstory` for each agent — the Manager uses backstories to assign tasks
- If output quality is inconsistent, switch to `manager_agent=` with a custom Manager

**Parallel-specific:**
- Set `max_workers` conservatively — too many parallel calls trigger LLM rate limits
- Add retry logic for individual crew failures
- Use `asyncio` for async-native applications; `ThreadPoolExecutor` for simpler scripts

---

## 10. Common Mistakes & Fixes

| Mistake | Symptom | Fix |
|---|---|---|
| Forgetting `manager_llm` with hierarchical | `ValueError` on crew creation | Always set `manager_llm=` or `manager_agent=` |
| Using both `manager_llm` and `manager_agent` | Unexpected behavior | Use one or the other, never both |
| No `context=[]` between sequential tasks | Agent ignores prior work | Connect tasks with `context=[prev_task]` |
| Using hierarchical for a 3-step pipeline | 3x token cost for no benefit | Use sequential for simple ordered pipelines |
| Too many parallel workers | `RateLimitError` from OpenAI | Reduce `max_workers`, add delays |
| Vague `expected_output` | Inconsistent, low-quality results | Be specific: length, format, sections required |
| `allow_delegation=True` on all agents | Agents delegate uncontrollably | Only set `True` on Manager agents |
| Giant context lists (10+ tasks) | Token limit errors | Summarize intermediate results before passing |

---

## 11. Quick Reference Cheatsheet

```python
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

# Sequential
crew = Crew(agents=[a1, a2, a3], tasks=[t1, t2, t3],
            process=Process.sequential, verbose=True)

# Hierarchical (Auto Manager)
crew = Crew(agents=[a1, a2, a3], tasks=[t1, t2, t3],
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(model="gpt-4o"),
            verbose=True)

# Hierarchical (Custom Manager)
manager = Agent(role="Manager", goal="Coordinate", backstory="...",
                allow_delegation=True)
crew = Crew(agents=[a1, a2, a3], tasks=[t1, t2, t3],
            process=Process.hierarchical,
            manager_agent=manager, verbose=True)

# Parallel (asyncio)
import asyncio
results = await asyncio.gather(
    *[asyncio.to_thread(crew.kickoff) for crew in [crew1, crew2, crew3]]
)

# Parallel (ThreadPoolExecutor)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(crew.kickoff) for crew in crews]
    results = [f.result() for f in futures]

# Dynamic inputs
result = crew.kickoff(inputs={"topic": "AI Agents", "word_count": "800"})

# Task context
task_b = Task(description="...", expected_output="...", context=[task_a])
task_c = Task(description="...", expected_output="...", context=[task_a, task_b])

# Agent config
agent = Agent(
    role="...", goal="...", backstory="...",
    verbose=True,
    allow_delegation=False,   # True only for manager agents
    max_iter=5,               # max retry attempts (default: 15)
    memory=True,              # enable agent memory
)
```

---

## 12. Running the Examples

### Prerequisites

```bash
pip install crewai crewai-tools langchain-openai python-dotenv

# Set API key
export OPENAI_API_KEY="sk-..."
# OR create .env file
echo 'OPENAI_API_KEY=sk-...' > .env
```

### Run sequential.py

```bash
python sequential.py
# Choose:
#   1 -> Basic 3-Step Content Pipeline   (Researcher -> Writer -> Editor)
#   2 -> Multi-Context SEO Factory        (Fork-and-Join pattern)
#   3 -> Data Analysis Pipeline           (Collect -> Analyze -> Report)
```

### Run hierarchical.py

```bash
python hierarchical.py
# Choose:
#   1 -> Investment Research Platform     (Financial + Risk + Market + Writer)
#   2 -> Software Project Planning        (Tech + UX + Backend + Frontend + PM)
#   3 -> Custom Manager Agent             (Advanced: manager_agent=)
```

---

## Resources

- [CrewAI Official Documentation](https://docs.crewai.com)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)
- [CrewAI Concepts: Process](https://docs.crewai.com/concepts/processes)
- [CrewAI Concepts: Tasks](https://docs.crewai.com/concepts/tasks)
- [CrewAI Concepts: Agents](https://docs.crewai.com/concepts/agents)

---

*Full Lesson — CrewAI `Process` Keyword | Generated with Claude by Anthropic*