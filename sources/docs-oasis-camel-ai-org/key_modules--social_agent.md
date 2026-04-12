---
title: "Social Agent"
source: "https://docs.oasis.camel-ai.org/key_modules/social_agent"
author: "CAMEL-AI OASIS Docs"
published: "2026-02-19"
---

# Social Agent

The Social Agent is the main class for creating social agents in the simulation. In this section, we will introduce how to create a `SocialAgent`.

`SocialAgent` class

A Social Agent in OASIS is an LLM-based social media user, inherited from CAMEL’s `ChatAgent`. It can perform actions on social media (e.g., posting), use external tools (such as Google Search), and has features like user information and a memory module. When initializing a `SocialAgent`, you can configure the following core parameters: 

| Parameter            | Type                                                                                                                                                                     | Required | Default | Description                                                                                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| agent\_id            | int                                                                                                                                                                      | ✔        | \-      | The unique ID of the agent, used as the primary key to distinguish different agents. Each SocialAgent must have a unique agent\_id.                                                                                                  |
| user\_info           | UserInfo                                                                                                                                                                 | ✔        | \-      | A dataclass containing the agent’s user registration info. For more details, see [UserInfo](#UserInfo).                                                                                                                              |
| user\_info\_template | [TextPrompt ](https://docs.camel-ai.org/key%5Fmodules/prompts)                                                                                                           | ✗        | None    | A text template that describes the agent when deciding what action to take. If None, a [default prompt template](#default-user-info-template) will be selected based on recsys\_type in UserInfo.                                    |
| agent\_graph         | [AgentGraph ](https://docs.oasis.camel-ai.org//key%5Fmodules/agent%5Fgraph)                                                                                              | ✔        | \-      | The AgentGraph instance that the SocialAgent belongs to.                                                                                                                                                                             |
| model                | [BaseModelBackend](https://docs.camel-ai.org/key%5Fmodules/models) or List\[BaseModelBackend\] or [ModelManager](https://docs.camel-ai.org/key%5Fmodules/models) or None | ✗        | None    | The llm model(s) to be used for the agent’s actions. If None, the gpt-4o-mini model will be used.                                                                                                                                    |
| available\_actions   | [list\[ActionType\]](https://docs.oasis.camel-ai.org/key%5Fmodules/actions) or None                                                                                      | ✗        | None    | List of allowed actions in the social platform. For more details, see [Actions Module](https://docs.oasis.camel-ai.org/key%5Fmodules/actions). If None, all actions are enabled by default.                                          |
| tools                | List\[Union\[FunctionTool, Callable\]\] or None                                                                                                                          | ✗        | None    | External tools the agent can use, such as a get\_weather function, a Toolkit, or an MCPToolkit from \[CAMEL\](<https://docs.camel-ai.org/key%5Fmodules/tools>. If set to None, the agent will not be able to use any external tools. |
| single\_iteration    | bool                                                                                                                                                                     | ✗        | True    | Whether the agent performs only a single round of reasoning when taking an LLM action. If False, the agent may continue acting based on the outcome of previous actions or tool calls.                                               |
| interview\_record    | bool                                                                                                                                                                     | ✗        | False   | Whether to record the interview prompt and result in the agent’s memory.                                                                                                                                                             |

For more details on the `model` and the `tools` parameter, see [Models Module](https://docs.oasis.camel-ai.org/key%5Fmodules/models) and [Toolkits Module](https://docs.oasis.camel-ai.org/key%5Fmodules/toolkits). 

`UserInfo` class

A dataclass containing the agent’s user registration info. Fields like `user_name`, `name`, and `description` must not be empty. The `profile` field is a dictionary whose keys must match those specified in `user_info_template`. 

```
@dataclass
class UserInfo:
   user_name: str
   name: str
   description: str
   profile: dict[str, Any]  # If user_info_template is provided, the keys must match those in the template.
   recsys_type: RecsysType # Ignored if user_info_template is provided.

```

* Example of a `user_info_template` and corresponding `UserInfo.profile` class:

```
from camel.prompts import TextPrompt

seller_template = TextPrompt('Your aim is: {aim} Your task is: {task}')

profile = {
    "aim": "Persuade people to buy `GlowPod` lamp.",
    "task": "Using roleplay to tell some story about the product.",
}

```

Default User Info Template

Twitter Style Template

```
def to_twitter_system_message(self) -> str:
    name_string = ""
    description_string = ""
    if self.name is not None:
        name_string = f"Your name is {self.name}."
    if self.profile is None:
        description = name_string
    elif "other_info" not in self.profile:
        description = name_string
    elif "user_profile" in self.profile["other_info"]:
        if self.profile["other_info"]["user_profile"] is not None:
            user_profile = self.profile["other_info"]["user_profile"]
            description_string = f"Your have profile: {user_profile}."
            description = f"{name_string}\n{description_string}"

    system_content = f"""
# OBJECTIVE
You're a Twitter user, and I'll present you with some tweets. After you see the tweets, choose some actions from the following functions.

# SELF-DESCRIPTION
Your actions should be consistent with your self-description and personality.
{description}

# RESPONSE METHOD
Please perform actions by tool calling.
"""
    return system_content

```

Reddit Style Template

```
def to_reddit_system_message(self) -> str:
    name_string = ""
    description_string = ""
    if self.name is not None:
        name_string = f"Your name is {self.name}."
    if self.profile is None:
        description = name_string
    elif "other_info" not in self.profile:
        description = name_string
    elif "user_profile" in self.profile["other_info"]:
        if self.profile["other_info"]["user_profile"] is not None:
            user_profile = self.profile["other_info"]["user_profile"]
            description_string = f"Your have profile: {user_profile}."
            description = f"{name_string}\n{description_string}"
            print(self.profile['other_info'])
            description += (
                f"You are a {self.profile['other_info']['gender']}, "
                f"{self.profile['other_info']['age']} years old, with an MBTI "
                f"personality type of {self.profile['other_info']['mbti']} from "
                f"{self.profile['other_info']['country']}.")

    system_content = f"""
# OBJECTIVE
You're a Reddit user, and I'll present you with some posts. After you see the posts, choose some actions from the following functions.

# SELF-DESCRIPTION
Your actions should be consistent with your self-description and personality.
{description}

# RESPONSE METHOD
Please perform actions by tool calling.
"""
    return system_content

```

[Agent Profile](https://docs.oasis.camel-ai.org/key_modules/social_agent/user%5Fgeneration/generation)[Models](https://docs.oasis.camel-ai.org/key_modules/social_agent/key%5Fmodules/models)
