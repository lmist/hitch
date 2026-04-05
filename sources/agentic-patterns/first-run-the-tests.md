# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/)

## First run the tests

Automated tests are no longer optional when working with coding agents.

The old excuses for not writing them - that they're time consuming and expensive to constantly rewrite while a codebase is rapidly evolving - no longer hold when an agent can knock them into shape in just a few minutes.

They're also _vital_ for ensuring AI-generated code does what it claims to do. If the code has never been executed it's pure luck if it actually works when deployed to production.

Tests are also a great tool to help get an agent up to speed with an existing codebase. Watch what happens when you ask Claude Code or similar about an existing feature - the chances are high that they'll find and read the relevant tests.

Agents are already biased towards testing, but the presence of an existing test suite will almost certainly push the agent into testing new changes that it makes.

Any time I start a new session with an agent against an existing project I'll start by prompting a variant of the following:

First run the tests

For my Python projects I have [pyproject.toml set up](https://til.simonwillison.net/uv/dependency-groups) such that I can prompt this instead:

Run "uv run pytest"

These four word prompts serve several purposes: 
1. It tells the agent that there is a test suite and forces it to figure out how to run the tests. This makes it almost certain that the agent will run the tests in the future to ensure it didn't break anything.
2. Most test harnesses will give the agent a rough indication of how many tests they are. This can act as a proxy for how large and complex the project is, and also hints that the agent should search the tests themselves if they want to learn more.
3. It puts the agent in a testing mindset. Having run the tests it's natural for it to then expand them with its own tests later on.

Similar to ["Use red/green TDD"](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), "First run the tests" provides a four word prompt that encompasses a substantial amount of software engineering discipline that's already baked into the models.

 ← [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/red-green-tdd/) 

[Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/agentic-manual-testing/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. **First run the tests**  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/prompts/)

[ testing93 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/testing/) [ tdd5 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/tdd/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/llms/) [ coding-agents190 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/coding-agents/) [ ai-assisted-programming371 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/ai-assisted-programming/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/generative-ai/) [ agentic-engineering39 ](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/tags/agentic-engineering/) 

 Created: 24th February 2026  
 Last modified: 28th February 2026  
[4 changes](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/first-run-the-tests/changes/) 

**Previous:** [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/red-green-tdd/)

**Next:** [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/guides/agentic-engineering-patterns/agentic-manual-testing/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/2026/)