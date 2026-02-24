# Lesson 1: Create AI Agents to Research and Write Articles

## Introduction

This project uses **CrewAI** to create a multi-agent system that automatically researches and writes articles on any given topic. The system consists of 3 AI agents working collaboratively:

1. **Planner**: Collects information and plans content strategy
2. **Writer**: Writes articles based on the planner's strategy
3. **Editor**: Reviews and refines the final article

## Features

- Automatic topic research and analysis
- Detailed content outline generation
- Complete blog post writing in Markdown format
- SEO optimization with relevant keywords
- Professional editing and proofreading
- Export results to Markdown files

## System Requirements

- Python 3.8 or higher
- OpenAI API key

## Installation

### 1. Navigate to the lesson folder

```bash
cd "Lesson 1"
```

### 2. Install required libraries

```bash
pip install -r requirements.txt
```

Main libraries:
- `crewai==0.28.8` - Multi-agent framework
- `crewai_tools==0.1.6` - Tools for CrewAI
- `langchain_community==0.0.29` - LangChain support library

### 3. Configure API Key

Create a `.env` file or configure the OpenAI API key in the `utils.py` file:

```python
# In utils.py or .env file
OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Run the program

```bash
python main.py
```

### Customize topic

Open the `main.py` file and change the `topic` variable in the `main()` function:

```python
def main():
    # Change topic as desired
    topic = "Blockchain Technology"  # Or any topic
    
    # ... rest of the code
```

### Output

After execution, the article will:
- Be displayed on the console
- Be saved to file `output_<topic_name>.md`

Example: If the topic is "Artificial Intelligence", the output file will be `output_artificial_intelligence.md`

## Project Structure

```
Lesson 1/
├── main.py                          # Main program file
├── main-old.py                      # Full version with comments
├── utils.py                         # Utility functions (get API key)
├── requirements.txt                 # List of required libraries
├── README.md                        # Documentation (this file)
└── output_*.md                      # Output files after execution
```

---

## 📚 In-Depth Component Explanations

### 1. Agent (AI Entity)

An Agent is an AI with a specific role and goal. Each agent in CrewAI is created using the `Agent()` class with the following attributes:

#### **role** (Role) - REQUIRED
- **Definition**: The role or title of the agent within the crew
- **Purpose**: Defines "who this agent is" and their scope of responsibility
- **Examples**: 
  ```python
  role="Content Planner"  # Content planning specialist
  role="Content Writer"   # Content writer
  role="Editor"           # Editor
  ```
- **Best practices**: 
  - Keep it concise and clear (2-4 words)
  - Should accurately reflect the main function
  - Avoid vague or overly generic titles

#### **goal** (Goal) - REQUIRED
- **Definition**: The specific objective the agent needs to achieve
- **Purpose**: Guides the agent on "what needs to be done" in each task
- **Examples**:
  ```python
  goal="Plan engaging and factually accurate content on {topic}"
  # Plan engaging and accurate content about {topic}
  
  goal="Write insightful and factually accurate opinion piece about {topic}"
  # Write insightful and accurate article about {topic}
  ```
- **Best practices**:
  - Be specific and measurable
  - Use variables like `{topic}` for dynamic content
  - Focus on the end result

#### **backstory** (Background Story) - REQUIRED
- **Definition**: Background story that helps the agent understand the work context
- **Purpose**: Provides context about "why" the agent does this work and "how" to do it
- **Examples**:
  ```python
  backstory="""You're working on planning a blog article about {topic}.
  You collect information that helps the audience learn something 
  and make informed decisions. Your work is the basis for 
  the Content Writer to write an article on this topic."""
  ```
- **Best practices**:
  - Describe the role within the workflow
  - Explain relationships with other agents
  - Provide guidance on work style
  - Can be 3-5 sentences to provide sufficient context

#### **allow_delegation** (Allow Delegation)
- **Definition**: Determines whether the agent can delegate work to other agents
- **Value**: `True` or `False` (default is `True`)
- **When to use True**:
  - Managing/coordinating agents (manager, supervisor)
  - When workflow is complex and needs task division
  - Agent has ability to decide which tasks to assign to whom
- **When to use False**:
  - Specialized agents doing one specific job
  - Linear, clear workflow
  - Want tight control over workflow
- **Example**:
  ```python
  allow_delegation=False  # Don't allow delegation
  # In this example, each agent only does assigned tasks
  ```

#### **verbose** (Display Details)
- **Definition**: Shows the agent's thought process and execution
- **Value**: `True` or `False` (default is `False`)
- **When to use True**:
  - During development/debugging
  - Want to understand what the agent is doing
  - Learning and research
- **When to use False**:
  - Production environment
  - Only care about final results
  - Reduce log output
- **Example**:
  ```python
  verbose=True  # Show detailed process
  # You'll see: thought process, actions, observations
  ```

#### **Other attributes** (Advanced)
- **llm**: Specific language model for this agent
- **tools**: List of tools the agent can use
- **max_iter**: Maximum number of iterations to complete task
- **memory**: Allows agent to remember previous interactions

---

### 2. Task (Task/Assignment)

A Task is specific work assigned to an agent. Each task is created using the `Task()` class:

#### **description** (Task Description) - REQUIRED
- **Definition**: Detailed description of what the agent needs to do
- **Purpose**: Provides specific step-by-step guidance for the agent
- **Example**:
  ```python
  description=(
      "1. Prioritize the latest trends, key players, "
      "   and noteworthy news on {topic}.\n"
      "2. Identify the target audience, considering "
      "   their interests and pain points.\n"
      "3. Develop a detailed content outline including "
      "   an introduction, key points, and a call to action.\n"
      "4. Include SEO keywords and relevant data or sources."
  )
  ```
- **Best practices**:
  - Break down into specific steps
  - Use numbered lists for clarity
  - Provide detailed requirements about format and content
  - Use variables like `{topic}` for dynamic content

#### **expected_output** (Expected Output) - REQUIRED
- **Definition**: Clear description of the output the agent needs to create
- **Purpose**: Helps the agent know "what success looks like"
- **Example**:
  ```python
  expected_output="A comprehensive content plan document "
                  "with an outline, audience analysis, "
                  "SEO keywords, and resources."
  ```
- **Best practices**:
  - Be specific about format (markdown, JSON, plain text...)
  - Clearly state required elements
  - Provide quality assessment criteria

#### **agent** (Executing Agent) - REQUIRED
- **Definition**: Which agent will execute this task
- **Example**:
  ```python
  agent=planner  # Task assigned to planner agent
  ```

#### **Other attributes** (Advanced)
- **context**: List of other tasks that provide context
- **tools**: Specific tools for this task
- **async_execution**: Whether to run asynchronously
- **output_file**: Save results to file

---

### 3. Crew (Team)

A Crew is a group of agents working together to achieve a common goal.

#### **agents** (List of Agents) - REQUIRED
- **Definition**: List of agents participating in the crew
- **Example**:
  ```python
  agents=[planner, writer, editor]
  ```
- **Order**: Not important here, execution order is determined by tasks

#### **tasks** (List of Tasks) - REQUIRED
- **Definition**: List of tasks to complete
- **Example**:
  ```python
  tasks=[plan, write, edit]
  ```
- **Order**: VERY IMPORTANT - tasks will be executed sequentially in this order

#### **verbose** (Detail Level)
- **Value**: `0`, `1`, `2` (or `True`/`False`)
  - `0` or `False`: Only show final results
  - `1` or `True`: Show basic information
  - `2`: Show all details (recommended for learning)
- **Example**:
  ```python
  verbose=True  # Show detailed logs (use True instead of 2)
  ```
- **Important Note**: Newer versions of CrewAI require `verbose` to be a boolean (`True`/`False`), not an integer

#### **process** (Execution Process)
- **Values**: 
  - `sequential` (default): Execute sequentially
  - `hierarchical`: With a manager agent coordinating
- **Example**:
  ```python
  from crewai import Process
  
  crew = Crew(
      agents=[...],
      tasks=[...],
      process=Process.sequential  # Or Process.hierarchical
  )
  ```

---

### 4. Workflow (Work Process)

In this example, the workflow operates as follows:

```
Topic Input → Planner Agent → Writer Agent → Editor Agent → Final Output
              (Task: plan)    (Task: write)   (Task: edit)
```

#### **Step 1: Planning**
- **Agent**: Planner
- **Input**: Topic from user
- **Process**: 
  - Research latest trends
  - Identify target audience
  - Create detailed outline
  - Find SEO keywords
- **Output**: Content plan document

#### **Step 2: Writing**
- **Agent**: Writer
- **Input**: Content plan from Planner
- **Process**:
  - Write article based on outline
  - Integrate SEO keywords
  - Structure article (intro, body, conclusion)
  - Check grammar
- **Output**: Blog post in Markdown format

#### **Step 3: Editing**
- **Agent**: Editor
- **Input**: Blog post from Writer
- **Process**:
  - Check for grammatical errors
  - Ensure journalistic best practices
  - Balance viewpoints
  - Avoid controversial content
- **Output**: Final article ready for publication

---

## 💡 Complete Code Example

Below is a complete example with explanations:

```python
from crewai import Agent, Task, Crew

# CREATE AGENT 1: PLANNER
planner = Agent(
    role="Content Planner",                    # Role
    goal="Plan engaging content on {topic}",   # Goal
    backstory="You're an expert content strategist...",  # Background
    allow_delegation=False,                    # No delegation
    verbose=True                               # Show details
)

# CREATE TASK FOR PLANNER
plan_task = Task(
    description="Research and create outline for {topic}",  # Description
    expected_output="A detailed content outline",           # Expected output
    agent=planner                                           # Executing agent
)

# CREATE CREW
crew = Crew(
    agents=[planner],      # List of agents
    tasks=[plan_task],     # List of tasks
    verbose=True           # Show logs (use True not 2)
)

# RUN CREW
result = crew.kickoff(inputs={"topic": "AI in Healthcare"})
print(str(result))  # Convert CrewOutput to string
```

---

## 🎯 Best Practices

### 1. Designing Agents
- ✅ Each agent should have ONE main responsibility
- ✅ Role should be concise, Goal specific, Backstory with full context
- ✅ Use `allow_delegation=False` for simple workflows
- ❌ Avoid creating an agent that "does everything"

### 2. Designing Tasks
- ✅ Description broken into clear steps
- ✅ Expected output describes specific format and content
- ✅ Task order reflects workflow logic
- ❌ Avoid vague descriptions like "do this task well"

### 3. Designing Crew
- ✅ Just enough agents (3-5 agents is optimal)
- ✅ Clear workflow with beginning and end
- ✅ Use `verbose=True` when learning/debugging (not 2)
- ❌ Avoid creating too many unnecessary agents

---

## 🔧 Advanced Configuration

### Changing OpenAI Model

In the `main.py` file, you can change the model:

```python
import os

# GPT-3.5 Turbo (fast, cheap, suitable for most tasks)
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# GPT-4 (more powerful, more accurate, more expensive)
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'

# GPT-4 Turbo (balance between speed and quality)
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
```

**Choosing the right model**:
- `gpt-3.5-turbo`: Demo, learning, simple tasks
- `gpt-4-turbo`: Production, complex tasks
- `gpt-4`: Need highest accuracy

### Using Other LLMs

CrewAI supports various LLMs:

#### 1. Hugging Face (Free)
```python
from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<HF_TOKEN_HERE>",
    task="text-generation",
)

# Apply to specific agent
planner = Agent(
    role="Content Planner",
    goal="...",
    backstory="...",
    llm=llm  # Add this line
)
```

#### 2. Mistral AI
```python
# Configure in .env or code
os.environ["OPENAI_API_KEY"] = "your-mistral-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.mistral.ai/v1"
os.environ["OPENAI_MODEL_NAME"] = "mistral-small"
```

#### 3. Cohere
```python
from langchain_community.chat_models import ChatCohere

os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
llm = ChatCohere()
```

#### 4. Ollama (Local, FREE)
```python
from langchain_community.llms import Ollama

llm = Ollama(model="llama2")

planner = Agent(
    role="Content Planner",
    # ... other params
    llm=llm
)
```

Learn more: [CrewAI LLM Connections](https://docs.crewai.com/how-to/LLM-Connections/)

### Customizing Agents with Tools

You can provide tools to agents:

```python
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Create tools
search_tool = SerperDevTool()
web_tool = WebsiteSearchTool()

# Apply to agent
planner = Agent(
    role="Content Planner",
    goal="Plan engaging content on {topic}",
    backstory="...",
    tools=[search_tool, web_tool],  # Agent can search Google and web
    allow_delegation=False,
    verbose=True
)
```

**Popular tools**:
- `SerperDevTool`: Google search
- `WebsiteSearchTool`: Search within website
- `FileReadTool`: Read files
- `DirectoryReadTool`: Read directories
- `CodeInterpreterTool`: Run Python code

### Customizing Tasks with Context

Tasks can use output from other tasks as context:

```python
# Task 1
research_task = Task(
    description="Research about {topic}",
    expected_output="Research summary",
    agent=researcher
)

# Task 2 uses output from Task 1
write_task = Task(
    description="Write article based on research",
    expected_output="Complete article",
    agent=writer,
    context=[research_task]  # Automatically receives output from research_task
)
```

### Customizing Crew Process

#### Sequential Process
```python
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    process=Process.sequential,  # Default
    verbose=True
)
# Order: plan → write → edit
```

#### Hierarchical Process (With Manager)
```python
from crewai import Process

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    process=Process.hierarchical,  # Automatic manager
    manager_llm="gpt-4",            # Model for manager
    verbose=True
)
# Manager will divide and assign tasks to agents
```

---

## 📋 Topic Examples

Some suggested topics you can try:

### Technology
- "Artificial Intelligence in Healthcare"
- "Blockchain Technology and Its Applications"
- "Quantum Computing Explained"
- "The Future of 5G Networks"
- "Cybersecurity Best Practices 2026"

### Health
- "Mental Health in the Digital Age"
- "Plant-Based Nutrition Benefits"
- "Fitness Trends in 2026"
- "Sleep Science and Productivity"

### Business
- "Remote Work Best Practices"
- "Startup Ecosystem in Vietnam"
- "Digital Marketing Strategies"
- "Sustainable Business Models"

### Environment
- "Climate Change Solutions"
- "Renewable Energy Technologies"
- "Sustainable Living Guide"
- "Ocean Conservation Efforts"

### Education
- "Online Learning Revolution"
- "EdTech Tools for Teachers"
- "Future of Higher Education"
- "AI in Personalized Learning"

---

## ❗ Common Error Troubleshooting

### 1. API Key Error

**Symptoms**:
```
Error: OpenAI API key not found
AuthenticationError: No API key provided
ImportError: Error importing native provider: OPENAI_API_KEY is required
```

**Causes**: 
- API key not configured
- Incorrect API key
- API key not loaded properly

**Solutions**:
```python
# In utils.py
import os

def get_openai_api_key():
    api_key = "sk-xxxxxxxxxxxxx"  # Replace with real key
    os.environ["OPENAI_API_KEY"] = api_key
    return api_key
```

Or use `.env` file:
```bash
# .env
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

```python
# utils.py
from dotenv import load_dotenv
import os

load_dotenv()

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")
```

### 2. Library Installation Error

**Symptoms**:
```
ERROR: Could not find a version that satisfies the requirement
ModuleNotFoundError: No module named 'crewai'
```

**Solutions**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall
pip install -r requirements.txt

# Or install individually
pip install crewai==0.28.8
pip install crewai_tools==0.1.6
pip install langchain_community==0.0.29
```

### 3. Verbose Type Error

**Symptoms**:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Crew
verbose
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value=2, input_type=int]
```

**Cause**:
- Newer versions of CrewAI require `verbose` to be a boolean (`True`/`False`), not an integer

**Solution**:
```python
# Change from:
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=2  # ❌ Wrong
)

# To:
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=True  # ✅ Correct
)
```

### 4. CrewOutput Write Error

**Symptoms**:
```
TypeError: write() argument must be str, not CrewOutput
```

**Cause**:
- `crew.kickoff()` returns a `CrewOutput` object, not a string
- File write requires string

**Solution**:
```python
# Change from:
result = crew.kickoff(inputs={"topic": topic})
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result)  # ❌ Wrong

# To:
result = crew.kickoff(inputs={"topic": topic})
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(str(result))  # ✅ Correct - convert to string
```

### 5. Rate Limit Error

**Symptoms**:
```
Error: Rate limit exceeded
RateLimitError: You exceeded your current quota
```

**Causes**:
- Too many API calls in short time
- Exceeded OpenAI account quota

**Solutions**:
- Wait a few minutes and try again
- Check quota at: https://platform.openai.com/usage
- Upgrade OpenAI plan if needed
- Reduce `verbose` to decrease API calls

### 6. Timeout Error

**Symptoms**:
```
TimeoutError: Request timed out
```

**Solution**:
```python
# Add timeout for agent
planner = Agent(
    role="Content Planner",
    goal="...",
    backstory="...",
    max_iter=15,  # Reduce iterations (default is 25)
    verbose=True
)
```

### 7. Memory/Performance Issues

**Symptoms**:
- Program runs very slowly
- Uses too much RAM

**Solutions**:
```python
# Reduce verbose level
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=False  # Instead of True
)

# Use lighter model
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'  # Instead of gpt-4
```

---

## 🧪 Testing and Debugging

### 1. Test Individual Agents

```python
# Test planner agent
test_crew = Crew(
    agents=[planner],
    tasks=[plan],
    verbose=True
)

result = test_crew.kickoff(inputs={"topic": "Test Topic"})
print(str(result))
```

### 2. Debug with Print Statements

```python
# During execution
print("=" * 50)
print("STARTING TASK:", task.description)
print("AGENT:", agent.role)
print("=" * 50)
```

### 3. Check Output of Each Task

```python
# Save output of each task
plan_result = crew.tasks[0].output
write_result = crew.tasks[1].output
edit_result = crew.tasks[2].output

print("Plan:", plan_result)
print("Write:", write_result)
print("Edit:", edit_result)
```

### 4. Monitor API Usage

```python
import openai

# Enable debug mode
openai.debug = True

# Or track costs
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = crew.kickoff(inputs={"topic": "AI"})
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Total Cost: ${cb.total_cost}")
```

---

## 📚 Reference Documentation

### CrewAI Documentation
- [Official Docs](https://docs.crewai.com/)
- [Agent Configuration](https://docs.crewai.com/core-concepts/Agents/)
- [Task Configuration](https://docs.crewai.com/core-concepts/Tasks/)
- [Crew Configuration](https://docs.crewai.com/core-concepts/Crews/)
- [Tools](https://docs.crewai.com/core-concepts/Tools/)

### OpenAI
- [API Documentation](https://platform.openai.com/docs)
- [Model Pricing](https://openai.com/pricing)
- [Best Practices](https://platform.openai.com/docs/guides/best-practices)

### LangChain
- [Documentation](https://python.langchain.com/)
- [Community Tools](https://python.langchain.com/docs/integrations/tools/)

### Tutorials & Examples
- [CrewAI Examples](https://github.com/joaomdmoura/crewAI-examples)
- [YouTube Tutorials](https://www.youtube.com/results?search_query=crewai+tutorial)

---

## 🚀 Advanced Topics

### 1. Adding Memory to Agents

```python
planner = Agent(
    role="Content Planner",
    goal="...",
    backstory="...",
    memory=True,  # Agent remembers previous interactions
    verbose=True
)
```

### 2. Using Custom Tools

```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "Custom Search"
    description: str = "Custom search tool"
    
    def _run(self, query: str) -> str:
        # Tool logic
        return f"Results for: {query}"

# Apply
planner = Agent(
    role="Content Planner",
    tools=[MyCustomTool()],
    # ... other params
)
```

### 3. Callbacks and Monitoring

```python
from crewai.callbacks import CrewCallback

class MyCallback(CrewCallback):
    def on_task_start(self, task):
        print(f"Task started: {task.description}")
    
    def on_task_end(self, task, output):
        print(f"Task completed: {output}")

crew = Crew(
    agents=[...],
    tasks=[...],
    callbacks=[MyCallback()]
)
```

### 4. Parallel Execution

```python
# Some tasks can run in parallel
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.parallel,  # Experimental
    max_concurrent_tasks=3
)
```

---

## 💬 Support & Community

### Having issues?
1. ✅ Check the "Common Error Troubleshooting" section
2. ✅ Review CrewAI documentation
3. ✅ Search on Google/Stack Overflow
4. ✅ Create an issue on GitHub repository
5. ✅ Join CrewAI Discord community

### Contributing
If you want to contribute to this project:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

---

## 📝 License

This project is developed for educational and research purposes.

---

## 🎓 Key Concepts Summary

| Concept | Description | Importance |
|---------|-------------|------------|
| **Agent** | AI entity with role, goal, backstory | ⭐⭐⭐⭐⭐ |
| **role** | Agent's role (who?) | ⭐⭐⭐⭐⭐ |
| **goal** | Agent's objective (what to do?) | ⭐⭐⭐⭐⭐ |
| **backstory** | Context for agent (why? how?) | ⭐⭐⭐⭐⭐ |
| **allow_delegation** | Allow delegation of work | ⭐⭐⭐ |
| **verbose** | Show detailed process | ⭐⭐⭐⭐ |
| **Task** | Specific task for agent | ⭐⭐⭐⭐⭐ |
| **description** | Detailed task description | ⭐⭐⭐⭐⭐ |
| **expected_output** | Expected output | ⭐⭐⭐⭐⭐ |
| **Crew** | Group of agents working together | ⭐⭐⭐⭐⭐ |
| **process** | Sequential/Hierarchical | ⭐⭐⭐ |
| **tools** | Tools for agents | ⭐⭐⭐⭐ |

---

**Happy Coding! 🚀**

If you find this guide helpful, please star ⭐ the repository!