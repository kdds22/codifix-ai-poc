# Fix.Ai Code

Welcome to the Fix.Ai Code project, powered by [crewAI](https://crewai.com). 

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. 

First, create a new environment:

```bash
python3 -m venv .venv
```
and activate it...
```bash
source .venv/bin/activate
```

So... This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

Then, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

#### Into the `.env`.

**Add your `OPENAI_API_KEY`**
**Add your `OPENAI_MODEL_NAME`**
**Add your `GOOGLE_APPLICATION_CREDENTIALS` with your bigquery json file.**

**Add your `GIT_AZURE_TOKEN` [`--optional`]**

**Add your `GIT_AZURE_REPO`**
**Add your `GIT_AZURE_USERNAME`**
**Add your `GIT_AZURE_PASSWORD` [Your own user token].**
**Add your `GIT_AZURE_SQUAD`**

- Modify `src/codifix_ai/config/agents.yaml` to define your agents
- Modify `src/codifix_ai/config/tasks.yaml` to define your tasks
- Modify `src/codifix_ai/main.py` to add your own logic, tools, specific args, custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run codifix_ai
```

## Understanding Your Crew

The codifix_ai Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

