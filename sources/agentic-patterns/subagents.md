# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/)

## Subagents

LLMs are restricted by their **context limit** \- how many tokens they can fit in their working memory at any given time. These values have not increased much over the past two years even as the LLMs themselves have seen dramatic improvements in their abilities - they generally top out at around 1,000,000, and benchmarks frequently report better quality results below 200,000.

Carefully managing the context such that it fits within those limits is critical to getting great results out of a model.

**Subagents** provide a simple but effective way to handle larger tasks without burning through too much of the coding agent’s valuable top-level context.

When a coding agent uses a subagent it effectively dispatches a fresh copy of itself to achieve a specified goal, with a new context window that starts with a fresh prompt.

## Claude Code’s Explore subagent [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#claude-codes-explore-subagent)

Claude Code uses subagents extensively as part of its standard way of working. Let's use that as an illustrative example.

Any time you start a new task against an existing repo Claude Code first needs to explore that repo to figure out its general shape and find relevant information needed to achieve that task.

It does this by constructing a prompt and dispatching a subagent to perform that exploration and return a description of what it finds.

I kicked off a Claude Code session with a screenshot of [a page from my guide](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/changes/) and this prompt:

> Make the chapter diffs also show which characters have changed in this diff view with a darker color of red or green for the individually changed segments of text within the line

Here's [the transcript](https://gisthost.github.io/?effbdc564939b88fe5c6299387e217da/index.html) of that session.

Claude Code started by running an “Explore” subagent with the following starter prompt:

> Find the code that implements the diff view for "chapters" in this Django blog. I need to find:
> 
> 1. Templates that render diffs (look for diff-related HTML/CSS with red/green backgrounds)
> 2. Python code that generates diffs (look for difflib usage or similar)
> 3. Any JavaScript related to diff rendering
> 4. CSS styles for the diff view (red/green line backgrounds)
> 
> Search thoroughly - check templates/, static/, blog/ directories. Look for keywords like "diff", "chapter", "revision", "history", "compare".

Subagents work similar to any other tool call: the parent agent dispatches them just as they would any other tool and waits for the response. It's interesting to see models prompt themselves in this way - they generally have good taste in prompting strategies.

The Explore subagent churned away for a few seconds and returned a response that started like this:

> Perfect! Now let me create a comprehensive summary with all the findings:
> 
> ### Summary: Chapter Diff View Implementation [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#summary-chapter-diff-view-implementation)
> 
> I found the complete implementation of the diff view for chapters in this Django blog. Here are the key components:
> 
> #### 1\. **Python Code - Diff Generation** (`/home/user/simonwillisonblog/guides/views.py`, lines 139-202) [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#1-python-code-diff-generation-homeusersimonwillisonblogguidesviewspy-lines-139-202)
> 
> The `chapter_changes()` view function uses Python's built-in `difflib.unified_diff()` to generate diffs: \[…\]

The full subagent response included all of the details the parent agent needed in order to start editing the code to address my original request.

## Parallel subagents [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#parallel-subagents)

This Explore subagent is the simplest example of how subagents can work, with the parent agent pausing while the subagent runs. The principle advantage of this kind of subagent is that it can work with a fresh context in a way that avoids spending tokens from the parent’s available limit.

Subagents can also provide a significant performance boost by having the parent agent run multiple subagents at the same time, potentially also using faster and cheaper models such as Claude Haiku to accelerate those tasks.

Coding agents that support subagents can use them based on your instructions. Try prompts like this:

`Use subagents to find and update all of the templates that are affected by this change.
`

For tasks that involve editing several files - and where those files are not dependent on each other - this can offer a significant speed boost. 

## Specialist subagents [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#specialist-subagents)

Some coding agents allow subagents to run with further customizations, often in the form of a custom system prompt or custom tools or both, which allow those subagents to take on a different role.

These roles can cover a variety of useful specialties:

* A **code reviewer** agent can review code and identify bugs, feature gaps or weaknesses in the design.
* A **test runner** agent can run the test. This is particularly worthwhile if your test suite is large and verbose, as the subagent can hide the full test output from the main coding agent and report back with just details of any failures.
* A **debugger** agent can specialize in debugging problems, spending its token allowance reasoning though the codebase and running snippets of code to help isolate steps to reproduce and determine the root cause of a bug.

While it can be tempting to go overboard breaking up tasks across dozens of different specialist subagents, it's important to remember that the main value of subagents is in preserving that valuable root context and managing token-heavy operations. Your root coding agent is perfectly capable of debugging or reviewing its own output provided it has the tokens to spare.

## Official documentation [#](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/#official-documentation)

Several popular coding agents support subagents, each with their own documentation on how to use them:

* [OpenAI Codex subagents](https://developers.openai.com/codex/subagents/)
* [Claude subagents](https://code.claude.com/docs/en/sub-agents)
* [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/)
* [Mistral Vibe subagents](https://docs.mistral.ai/mistral-vibe/agents-skills#agent-selection)
* [OpenCode agents](https://opencode.ai/docs/agents/)
* [Subagents in Visual Studio Code](https://code.visualstudio.com/docs/copilot/agents/subagents)
* [Cursor Subagents](https://cursor.com/docs/subagents)

 ← [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/using-git-with-coding-agents/) 

[Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/red-green-tdd/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. **Subagents**
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/prompts/)

[ parallel-agents16 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/parallel-agents/) [ coding-agents190 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/coding-agents/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/generative-ai/) [ agentic-engineering39 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/agentic-engineering/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/tags/llms/) 

 Created: 17th March 2026  
 Last modified: 17th March 2026  
[4 changes](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/subagents/changes/) 

**Previous:** [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/using-git-with-coding-agents/)

**Next:** [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/guides/agentic-engineering-patterns/red-green-tdd/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/2026/)