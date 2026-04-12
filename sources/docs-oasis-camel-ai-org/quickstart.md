---
title: "Quickstart"
source: "https://docs.oasis.camel-ai.org/quickstart"
author: "CAMEL-AI OASIS Docs"
published: "2025-11-13"
---

# Quickstart

Start using OASIS for social simulations in under 5 minutes

Setup your environment

Learn how to set up OASIS and run your first social simulation. 

Installation

You can install OASIS in two ways: 

Option 1: Install via pip

```
pip install camel-oasis

```

Option 2: Clone the repository

```
git clone https://github.com/camel-ai/oasis.git
cd oasis

pip install --upgrade pip setuptools
pip install -e . # This will install dependencies as specified in pyproject.toml

```

Running simulations

OASIS supports different types of LLM backends for running simulations. Choose the option that works best for your needs. 

Using OpenAI API

Set up your API key

Add your OpenAI API key to your environment variables:**For Bash (Linux, macOS, Git Bash on Windows):**

```
export OPENAI_API_KEY=<insert your OpenAI API key>
export OPENAI_API_BASE_URL=<insert your OpenAI API BASE URL>  # Optional: for proxy services

```

**For Windows Command Prompt:**

```
set OPENAI_API_KEY=<insert your OpenAI API key>
set OPENAI_API_BASE_URL=<insert your OpenAI API BASE URL>  # Optional: for proxy services

```

**For Windows PowerShell:**

```
$env:OPENAI_API_KEY="<insert your OpenAI API key>"
$env:OPENAI_API_BASE_URL="<insert your OpenAI API BASE URL>"  # Optional: for proxy services

```

Prepare the user profiles

If you install with `pip`, download [this file](https://github.com/camel-ai/oasis/blob/main/data/reddit/user%5Fdata%5F36.json) to your own `./data/reddit/user_data_36.json` directory.

Run a Reddit simulation

Execute the Reddit simulation script:

```
import asyncio
import os

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

import oasis
from oasis import (ActionType, LLMAction, ManualAction,
                  generate_reddit_agent_graph)

async def main():
    # Define the model for the agents
    openai_model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
    )

    # Define the available actions for the agents
    available_actions = [
        ActionType.LIKE_POST,
        ActionType.DISLIKE_POST,
        ActionType.CREATE_POST,
        ActionType.CREATE_COMMENT,
        ActionType.LIKE_COMMENT,
        ActionType.DISLIKE_COMMENT,
        ActionType.SEARCH_POSTS,
        ActionType.SEARCH_USER,
        ActionType.TREND,
        ActionType.REFRESH,
        ActionType.DO_NOTHING,
        ActionType.FOLLOW,
        ActionType.MUTE,
    ]

    agent_graph = await generate_reddit_agent_graph(
        profile_path="./data/reddit/user_data_36.json",
        model=openai_model,
        available_actions=available_actions,
    )

    # Define the path to the database
    db_path = "./data/reddit_simulation.db"

    # Delete the old database
    if os.path.exists(db_path):
        os.remove(db_path)

    # Make the environment
    env = oasis.make(
        agent_graph=agent_graph,
        platform=oasis.DefaultPlatformType.REDDIT,
        database_path=db_path,
    )

    # Run the environment
    await env.reset()

    actions_1 = {}
    actions_1[env.agent_graph.get_agent(0)] = [
        ManualAction(action_type=ActionType.CREATE_POST,
                    action_args={"content": "Hello, world!"}),
        ManualAction(action_type=ActionType.CREATE_COMMENT,
                    action_args={
                        "post_id": "1",
                        "content": "Welcome to the OASIS World!"
                    })
    ]
    actions_1[env.agent_graph.get_agent(1)] = ManualAction(
        action_type=ActionType.CREATE_COMMENT,
        action_args={
            "post_id": "1",
            "content": "I like the OASIS world."
        })
    await env.step(actions_1)

    actions_2 = {
        agent: LLMAction()
        for _, agent in env.agent_graph.get_agents()
    }

    # Perform the actions
    await env.step(actions_2)

    # Close the environment
    await env.close()

if __name__ == "__main__":
    asyncio.run(main())

```

This will start a simulation of user interactions in a Reddit-like environment.

Using local open-source models with VLLM

Set up VLLM

1. Install VLLM by following the instructions in the [VLLM repository](https://github.com/vllm-project/vllm)
2. Download a model (e.g., Qwen 2.5) to your local machine:

```
pip install huggingface_hub

huggingface-cli download --resume-download "Qwen/Qwen2.5-7B-Instruct" \
  --local-dir "YOUR_LOCAL_MODEL_DIRECTORY" \
  --local-dir-use-symlinks False \
  --resume-download \
  --token "YOUR_HUGGING_FACE_TOKEN"

```

1. Deploy the VLLM API server:

```
vllm serve /path/to/Qwen2.5-7B-Instruct --host 0.0.0.0 --port 8000 \
  --served-model-name 'qwen-2' \
  --enable-auto-tool-choice \
  --tool-call-parser hermes

```

1. Test if VLLM is correctly deployed:

```
curl http://$ip:$port/v1/models

```

Run a Twitter simulation with local models

1. Edit or write the `scripts/environment/twitter_simulation.py` file to use your VLLM deployment:

```
vllm_model_1 = ModelFactory.create(
    model_platform=ModelPlatformType.VLLM,
    model_type="qwen-2",
    url="http://$ip:$port",
)
vllm_model_2 = ModelFactory.create(
    model_platform=ModelPlatformType.VLLM,
    model_type="qwen-2",
    url="http://$ip:$port",
)
models = [vllm_model_1, vllm_model_2]

```

1. Prepare the user profiles: If you install with `pip`, download [this file](https://github.com/camel-ai/oasis/blob/refactor/data/twitter%5Fdataset/anonymous%5Ftopic%5F200%5F1h/False%5FBusiness%5F0.csv) to your own `data/twitter_dataset/anonymous_topic_200_1h/False_Business_0.csv` directory.
2. Run the Twitter simulation:

```
import asyncio
import os

from camel.models import ModelFactory
from camel.types import ModelPlatformType

import oasis
from oasis import (ActionType, LLMAction, ManualAction,
                  generate_twitter_agent_graph)

async def main():
    # Define the models for agents. Agents will select models based on
    # pre-defined scheduling strategies
    vllm_model_1 = ModelFactory.create(
        model_platform=ModelPlatformType.VLLM,
        model_type="qwen-2",
        url="http://$ip:$port",
    )
    vllm_model_2 = ModelFactory.create(
        model_platform=ModelPlatformType.VLLM,
        model_type="qwen-2",
        url="http://$ip:$port",
    )
    models = [vllm_model_1, vllm_model_2]

    # Define the available actions for the agents
    available_actions = [
        ActionType.CREATE_POST,
        ActionType.LIKE_POST,
        ActionType.REPOST,
        ActionType.FOLLOW,
        ActionType.DO_NOTHING,
        ActionType.QUOTE_POST,
    ]

    agent_graph = await generate_twitter_agent_graph(
        profile_path="./data/reddit/user_data_36.json",
        model=models,
        available_actions=available_actions,
    )

    # Define the path to the database
    db_path = "./data/twitter_simulation.db"

    # Delete the old database
    if os.path.exists(db_path):
        os.remove(db_path)

    # Make the environment
    env = oasis.make(
        agent_graph=agent_graph,
        platform=oasis.DefaultPlatformType.TWITTER,
        database_path=db_path,
    )

    # Run the environment
    await env.reset()

    actions_1 = {}

    actions_1[env.agent_graph.get_agent(0)] = ManualAction(
        action_type=ActionType.CREATE_POST,
        action_args={"content": "Earth is flat."})
    await env.step(actions_1)

    actions_2 = {
        agent: LLMAction()
        # Activate 5 agents with id 1, 3, 5, 7, 9
        for _, agent in env.agent_graph.get_agents([1, 3, 5, 7, 9])
    }

    await env.step(actions_2)

    actions_3 = {}

    actions_3[env.agent_graph.get_agent(1)] = ManualAction(
        action_type=ActionType.CREATE_POST,
        action_args={"content": "Earth is not flat."})
    await env.step(actions_3)

    actions_4 = {
        agent: LLMAction()
        # get all agents
        for _, agent in env.agent_graph.get_agents()
    }
    await env.step(actions_4)

    # Close the environment
    await env.close()

if __name__ == "__main__":
    asyncio.run(main())

```

[Introduction](https://docs.oasis.camel-ai.org/quickstart/introduction)[Overview](https://docs.oasis.camel-ai.org/quickstart/overview)
