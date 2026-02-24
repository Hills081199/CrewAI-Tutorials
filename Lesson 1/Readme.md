# Lesson 1: Create Agents to Research and Write an Article

## Introduction

This project uses **CrewAI** to create a multi-agent system that automatically researches and writes articles on any given topic. The system consists of 3 AI agents working together:

1. **Planner**: Collects information and plans content
2. **Writer**: Writes articles based on the plan
3. **Editor**: Reviews and refines the final output

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

After execution, the article will be:
- Displayed on the console
- Saved to file `output_<topic_name>.md`

Example: If the topic is "Artificial Intelligence", the output file will be `output_artificial_intelligence.md`

## Project Structure

```
Lesson 1/
├── main.py                          # Main program file
├── utils.py                         # Utility functions (get API key)
├── requirements.txt                 # List of required libraries
├── README.md                        # Documentation (this file)
└── output_*.md                      # Output files after execution
```

## How It Works

### 1. Planner Agent

**Role**: Content Planner

**Tasks**:
- Prioritize latest trends and noteworthy news
- Identify target audience
- Develop detailed content outline
- Find SEO keywords and reference sources

**Output**: Comprehensive content plan document

### 2. Writer Agent

**Role**: Content Writer

**Tasks**:
- Write article based on Planner's plan
- Integrate SEO keywords naturally
- Create engaging article structure (introduction, main content, conclusion)
- Ensure grammar quality and writing style

**Output**: Complete blog post in Markdown format

### 3. Editor Agent

**Role**: Editor

**Tasks**:
- Check for grammatical errors
- Ensure article follows journalistic best practices
- Balance viewpoints
- Avoid controversial content

**Output**: Final article ready for publication

## Advanced Configuration

### Change OpenAI model

In the `main.py` file, you can change the model:

```python
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'  # Or gpt-3.5-turbo, gpt-4-turbo, etc.
```

### Use other LLMs

CrewAI supports various LLMs such as:

#### Hugging Face
```python
from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<HF_TOKEN_HERE>",
    task="text-generation",
)
```

#### Mistral
```python
OPENAI_API_KEY=your-mistral-api-key
OPENAI_API_BASE=https://api.mistral.ai/v1
OPENAI_MODEL_NAME="mistral-small"
```

#### Cohere
```python
from langchain_community.chat_models import ChatCohere

os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
llm = ChatCohere()
```

#### Ollama (Local)
See more at: [CrewAI LLM Connections](https://docs.crewai.com/how-to/LLM-Connections/)

### Customize Agents

You can adjust agent properties:

```python
agent = Agent(
    role="Your Role",
    goal="Your Goal",
    backstory="Your Backstory",
    allow_delegation=True,  # Allow delegating work to other agents
    verbose=True,  # Display detailed process
)
```

### Customize Tasks

You can add or modify tasks:

```python
custom_task = Task(
    description="Your task description",
    expected_output="Expected output description",
    agent=your_agent,
)
```

## Topic Examples

Some suggested topics you can try:

- **Technology**: "Artificial Intelligence", "Blockchain", "Quantum Computing"
- **Health**: "Mental Health", "Nutrition", "Fitness Trends"
- **Business**: "Remote Work", "Startup Ecosystem", "Digital Marketing"
- **Environment**: "Climate Change", "Renewable Energy", "Sustainable Living"
- **Education**: "Online Learning", "EdTech", "Future of Education"

## Common Errors

### API Key Error
```
Error: OpenAI API key not found
```
**Solution**: Check the `utils.py` file and ensure the API key is configured correctly.

### Library installation error
```
ERROR: Could not find a version that satisfies the requirement
```
**Solution**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Timeout or Rate Limit
```
Error: Rate limit exceeded
```
**Solution**: Wait a moment and try again, or upgrade your OpenAI API plan.

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)

## Contributing

If you want to contribute to this project:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## Contact & Support

If you have questions or encounter issues:
- Create an issue in the repository
- Refer to CrewAI documentation
- Review the installation steps

## License

This project is developed for educational and research purposes.