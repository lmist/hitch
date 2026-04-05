# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/)

## Red/green TDD

"**Use red/green TDD**" is a pleasingly succinct way to get better results out of a coding agent.

TDD stands for Test Driven Development. It's a programming style where you ensure every piece of code you write is accompanied by automated tests that demonstrate the code works.

The most disciplined form of TDD is test-first development. You write the automated tests first, confirm that they fail, then iterate on the implementation until the tests pass.

This turns out to be a _fantastic_ fit for coding agents. A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both.

Test-first development helps protect against both of these common mistakes, and also ensures a robust automated test suite that protects against future regressions. As projects grow the chance that a new change might break an existing feature grows with them. A comprehensive test suite is by far the most effective way to keep those features working.

It's important to confirm that the tests fail before implementing the code to make them pass. If you skip that step you risk building a test that passes already, hence failing to exercise and confirm your new implementation.

That's what "red/green" means: the red phase watches the tests fail, then the green phase confirms that they now pass.

Every good model understands "red/green TDD" as a shorthand for the much longer "use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass".

Example prompt:

Build a Python function to extract headers from a markdown string. Use red/green TDD.

 ← [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/subagents/) 

[First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/first-run-the-tests/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. **Red/green TDD**  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/prompts/)

[ testing93 ](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/tags/testing/) [ tdd5 ](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/tags/tdd/) [ coding-agents189 ](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/tags/coding-agents/) [ ai-assisted-programming370 ](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/tags/ai-assisted-programming/) [ agentic-engineering38 ](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/tags/agentic-engineering/) 

 Created: 23rd February 2026  
 Last modified: 28th February 2026  
[6 changes](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/red-green-tdd/changes/) 

**Previous:** [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/subagents/)

**Next:** [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/guides/agentic-engineering-patterns/first-run-the-tests/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/2026/)