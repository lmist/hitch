# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/)

## How coding agents work

As with any tool, understanding how [coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/) work under the hood can help you make better decisions about how to apply them.

A coding agent is a piece of software that acts as a **harness** for an LLM, extending that LLM with additional capabilities that are powered by invisible prompts and implemented as callable tools.

## Large Language Models [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#large-language-models)

At the heart of any coding agent is a Large Language Model, or LLM. These have names like GPT-5.4 or Claude Opus 4.6 or Gemini 3.1 Pro or Qwen3.5-35B-A3B.

An LLM is a machine learning model that can complete a sentence of text. Give the model the phrase "the cat sat on the " and it will (almost certainly) suggest "mat" as the next word in the sentence.

As these models get larger and train on increasing amounts of data, they can complete more complex sentences - like "a python function to download a file from a URL is def download\_file(url): ".

LLMs don't actually work directly with words - they work with tokens. A sequence of text is converted into a sequence of integer tokens, so "the cat sat on the " becomes `[3086, 9059, 10139, 402, 290, 220]`. This is worth understanding because LLM providers charge based on the number of tokens processed, and are limited in how many tokens they can consider at a time.

You can experiment with the OpenAI tokenizer to see how this works at [platform.openai.com/tokenizer](https://platform.openai.com/tokenizer).

The input to an LLM is called the **prompt**. The text returned by an LLM is called the **completion**, or sometimes the **response**.

Many models today are **multimodal**, which means they can accept more than just text as input. **Vision LLMs** (vLLMs) can accept images as part of the input, which means you can feed them sketches or photos or screenshots. A common misconception is that these are run through a separate process for OCR or image analysis, but these inputs are actually turned into yet more token integers which are processed in the same way as text.

## Chat templated prompts [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#chat-templated-prompts)

The first LLMs worked as completion engines - users were expected to provide a prompt which could then be completed by the model, such as the two examples shown above.

This wasn't particularly user-friendly so models mostly switched to using **chat templated prompts** instead, which represent communication with the model as a simulated conversation.

This is actually just a form of completion prompt with a special format that looks something like this.

`user: write a python function to download a file from a URL
assistant:
`

The natural completion for this prompt is for the assistant (represented by the LLM) to answer the user's question with some Python code.

LLMs are stateless: every time they execute a prompt they start from the same blank slate. 

To maintain the simulation of a conversation, the software that talks to the model needs to maintain its own state and replay the entire existing conversation every time the user enters a new chat prompt:

`user: write a python function to download a file from a URL
assistant: def download_url(url):
    return urllib.request.urlopen(url).read()
user: use the requests library instead
assistant:
`

Since providers charge for both input and output tokens, this means that as a conversation gets longer, each prompt becomes more expensive since the number of input tokens grows every time.

## Token caching [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#token-caching)

Most model providers offset this somewhat through a cheaper rate for **cached input tokens** \- common token prefixes that have been processed within a short time period can be charged at a lower rate as the underlying infrastructure can cache and then reuse many of the expensive calculations used to process that input.

Coding agents are designed with this optimization in mind - they avoid modifying earlier conversation content to ensure the cache is used as efficiently as possible.

## Calling tools [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#calling-tools)

The defining feature of an LLM **agent** is that agents can call **tools**. But what is a tool?

A tool is a function that the agent harness makes available to the LLM.

At the level of the prompt itself, that looks something like this:

`system: If you need to access the weather, end your turn with <tool>get_weather(city_name)</tool>
user: what's the weather in San Francisco?
assistant:
`

Here the assistant might respond with the following text:

`<tool>get_weather("San Francisco")</tool>
`

The model harness software then extracts that function call request from the response - probably with a regular expression - and executes the tool.

It then returns the result to the model, with a constructed prompt that looks something like this:

`system: If you need to access the weather, end your turn with <tool>get_weather(city_name)</tool>
user: what's the weather in San Francisco?
assistant: <tool>get_weather("San Francisco")</tool>
user: <tool-result>61°, Partly cloudy</tool-result>
assistant:
`

The LLM can now use that tool result to help generate an answer to the user's question.

Most coding agents define a dozen or more tools for the agent to call. The most powerful of these allow for code execution - a `Bash()` tool for executing terminal commands, or a `Python()` tool for running Python code, for example.

## The system prompt [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#the-system-prompt)

In the previous example I included an initial message marked "system" which informed the LLM about the available tool and how to call it.

Coding agents usually start every conversation with a system prompt like this, which is not shown to the user but provides instructions telling the model how it should behave.

These system prompts can be hundreds of lines long. Here's [the system prompt for OpenAI Codex](https://github.com/openai/codex/blob/rust-v0.114.0/codex-rs/core/templates/model%5Finstructions/gpt-5.2-codex%5Finstructions%5Ftemplate.md) as-of March 2026, which is a useful clear example of the kind of instructions that make these coding agents work.

## Reasoning [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#reasoning)

One of the big new advances in 2025 was the introduction of **reasoning** to the frontier model families.

Reasoning, sometimes presented as **thinking** in the UI, is when a model spends additional time generating text that talks through the problem and its potential solutions before presenting a reply to the user.

This can look similar to a person thinking out loud, and has a similar effect. Crucially it allows models to spend more time (and more tokens) working on a problem in order to hopefully get a better result.

Reasoning is particularly useful for debugging issues in code as it gives the model an opportunity to navigate more complex code paths, mixing in tool calls and using the reasoning phase to follow function calls back to the potential source of an issue.

Many coding agents include options for dialing up or down the reasoning effort level, encouraging models to spend more time chewing on harder problems.

## LLM + system prompt + tools in a loop [#](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/#llm-system-prompt-tools-in-a-loop)

Believe it or not, that's most of what it takes to build a coding agent!

If you want to develop a deeper understanding of how these things work, a useful exercise is to try building your own agent from scratch. A simple tool loop can be achieved with a few dozen lines of code on top of an existing LLM API.

A _good_ tool loop is a great deal more work than that, but the fundamental mechanics are surprisingly straightforward.

 ← [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/anti-patterns/) 

[Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/using-git-with-coding-agents/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. **How coding agents work**  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/prompts/)

[ coding-agents189 ](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/tags/coding-agents/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/tags/generative-ai/) [ agentic-engineering38 ](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/tags/agentic-engineering/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/tags/ai/) [ llms1694 ](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/tags/llms/) 

 Created: 16th March 2026  
 Last modified: 16th March 2026  
[7 changes](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/how-coding-agents-work/changes/) 

**Previous:** [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/anti-patterns/)

**Next:** [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/guides/agentic-engineering-patterns/using-git-with-coding-agents/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/2026/)