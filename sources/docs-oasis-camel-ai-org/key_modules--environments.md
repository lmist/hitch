---
title: "Environment"
source: "https://docs.oasis.camel-ai.org/key_modules/environments"
author: "CAMEL-AI OASIS Docs"
published: "2025-11-13"
---

# Environment

Configure the fundamental settings for your OASIS simulation environment

Basic Environment Settings

OASIS provides a powerful simulation environment for social media platforms. This guide covers the basic configuration options for setting up your simulation environment. 

Environment Initialization

To create a simulation environment, use the `make` function from OASIS: 

```
import oasis
from oasis import DefaultPlatformType

# Make the environment
env = oasis.make(
    agent_graph=agent_graph,
    platform=oasis.DefaultPlatformType.REDDIT,
    database_path="simulation.db",
)

```

Core Environment Parameters

When initializing the OASIS environment, you can configure the following core parameters: 

| Parameter      | Type                            | Description                                                                                                                                                                  |
| -------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| agent\_graph   | AgentGraph                      | An AgentGraph instance that stores all the social agents in the simulation. For more details, see [Agent Graph](https://docs.oasis.camel-ai.org/key%5Fmodules/agent%5Fgraph) |
| platform       | DefaultPlatformType or Platform | The platform type to use (TWITTER or REDDIT) or a custom Platform instance                                                                                                   |
| database\_path | str                             | Path to create a SQLite database (must end with .db)                                                                                                                         |
| semaphore      | int                             | Limit on concurrent LLM requests (default: 128)                                                                                                                              |

For more details, see the [Platform](https://docs.oasis.camel-ai.org/key%5Fmodules/platform), [Agent Profile](https://docs.oasis.camel-ai.org/user%5Fgeneration/user%5Fgeneration), [Model](https://docs.oasis.camel-ai.org/key%5Fmodules/models) and [Actions](https://docs.oasis.camel-ai.org/key%5Fmodules/agent%5Fgraph) Module. 

Environment Lifecycle

The OASIS environment has a simple lifecycle you can manage with these methods: 

```
# Initialize the environment
await env.reset()

# Run simulation steps
for _ in range(n):
    await env.step(actions)

# Close the environment when done
await env.close()

```

For more action details, see [Actions Module](https://docs.oasis.camel-ai.org/key%5Fmodules/actions)

[Overview](https://docs.oasis.camel-ai.org/key_modules/environments/overview)[Agent Graph](https://docs.oasis.camel-ai.org/key_modules/environments/key%5Fmodules/agent%5Fgraph)
