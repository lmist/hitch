---
title: "Platform"
source: "https://docs.oasis.camel-ai.org/key_modules/platform"
author: "CAMEL-AI OASIS Docs"
published: "2025-11-13"
---

# Platform

This section introduces how to configure the social platform in OASIS.

The Social Platform module is a core component of Oasis that simulates a social media environment for agent interactions. It provides a complete infrastructure for social network activities, including user management, content creation, engagement metrics, recommendation systems, and user interactions. We support passing in two types of platforms. One is the `DefaultPlatformType`, which includes Twitter and Reddit. Otherwise, you can customize the `Platform` settings and pass them in. 

Default Platform Type (Recommend)

OASIS supports two built-in platform types, which can be specified during environment creation: 

Twitter-like Platform

```
env = oasis.make(
    platform=DefaultPlatformType.TWITTER,
    database_path="./data/twitter_simulation.db",
    agent_profile_path="./data/profiles/twitter_users.csv",
    agent_models=models,
    available_actions=available_actions,
)

```

The Twitter-like platform simulates a microblogging service with features like posts, likes, retweets, and following. 

Reddit-like Platform

```
env = oasis.make(
    platform=DefaultPlatformType.REDDIT,
    database_path="./data/reddit_simulation.db",
    agent_profile_path="./data/profiles/reddit_users.json",
    agent_models=models,
    available_actions=available_actions,
)

```

Customized Platform

The platform uses an asynchronous architecture to handle agent actions and maintain a consistent timeline within the simulation. 

Key Features

Time Management

* Configurable time acceleration using `sandbox_clock`
* Support for simulated timeline progression

Database Integration

* SQLite-based storage for all social activities and relationships
* Comprehensive logging of user actions and system events

Recommendation Systems

Several recommendation system types are supported: 
* **Random**: Simple randomized content recommendation
* **Reddit**: Reddit-style recommendation based on engagement metrics
* **Twitter**: Personalized recommendations based on user history
* **TWHin**: Advanced recommendation using graph embedding (optional OpenAI embedding integration)

Social Actions

The platform supports a wide range of social media actions. 

Initialization

```
from oasis.social_platform.platform import Platform
from oasis.clock.clock import Clock

# Initialize with custom configuration
platform = Platform(
    db_path="social_platform.db",
    sandbox_clock=Clock(k=60),
    show_score=True,
    allow_self_rating=False,
    recsys_type="twitter",
    refresh_rec_post_count=5,
    max_rec_post_len=10,
    following_post_count=3,
    use_openai_embedding=False
)

```

Configuration Options

| Parameter                 | Type           | Default        | Description                                                                                                        |
| ------------------------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------ |
| db\_path                  | str            | Required       | Path to SQLite database                                                                                            |
| channel                   | Any            | Channel()      | Communication channel for agent interactions                                                                       |
| sandbox\_clock            | Clock          | Clock(60)      | Time management for the simulation(for reddit recommendation system)                                               |
| start\_time               | datetime       | datetime.now() | Initial time for the simulation(for reddit recommendation system)                                                  |
| show\_score               | bool           | False          | Show combined score (Reddit style) instead of separate likes/dislikes                                              |
| allow\_self\_rating       | bool           | True           | Allow users to like/dislike their own content                                                                      |
| recsys\_type              | str/RecsysType | ”reddit”       | Recommendation system type (“random”, “reddit”, “twitter”, “twhin”)                                                |
| refresh\_rec\_post\_count | int            | 1              | Number of posts returned per refresh                                                                               |
| max\_rec\_post\_len       | int            | 2              | Maximum posts per user in recommendation buffer                                                                    |
| following\_post\_count    | int            | 3              | Number of posts from followed users                                                                                |
| use\_openai\_embedding    | bool           | False          | Use OpenAI embeddings for TWHin recommendation system. If false, use the local TWHIN-BERT model to get embeddings. |

Recommendation System

Different recommendation algorithms can be configured through the `recsys_type` parameter: The available recommendation system types are: 

| RecsysType       | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| TWITTER          | Standard Twitter-like recommendation system                      |
| TWHIN(Recommend) | TWHINBert-based recommendation system for Twitter-like platforms |
| REDDIT           | Reddit-style recommendation system                               |
| RANDOM           | Random content recommendation (for baseline testing)             |

[Toolkits](https://docs.oasis.camel-ai.org/key_modules/platform/key%5Fmodules/toolkits)[Actions](https://docs.oasis.camel-ai.org/key_modules/platform/key%5Fmodules/actions)
