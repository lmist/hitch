# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/)

## Writing code is cheap now

The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that _writing code is cheap now_.

Code has always been expensive. Producing a few hundred lines of clean, tested code takes most software developers a full day or more. Many of our engineering habits, at both the macro and micro level, are built around this core constraint.

At the macro level we spend a great deal of time designing, estimating and planning out projects, to ensure that our expensive coding time is spent as efficiently as possible. Product feature ideas are evaluated in terms of how much value they can provide _in exchange for that time_ \- a feature needs to earn its development costs many times over to be worthwhile!

At the micro level we make hundreds of decisions a day predicated on available time and anticipated tradeoffs. Should I refactor that function to be slightly more elegant if it adds an extra hour of coding time? How about writing documentation? Is it worth adding a test for this edge case? Can I justify building a debug interface for this?

Coding agents dramatically drop the cost of typing code into the computer, which disrupts _so many_ of our existing personal and organizational intuitions about which trade-offs make sense.

The ability to run parallel agents makes this even harder to evaluate, since one human engineer can now be implementing, refactoring, testing and documenting code in multiple places at the same time.

## Good code still has a cost [#](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/code-is-cheap/#good-code)

Delivering new code has dropped in price to almost free... but delivering _good_ code remains significantly more expensive than that.

Here's what I mean by "good code":

* The code works. It does what it's meant to do, without bugs.
* We _know the code works_. We've taken steps to confirm to ourselves and to others that the code is fit for purpose.
* It solves the right problem.
* It handles error cases gracefully and predictably: it doesn't just consider the happy path. Errors should provide enough information to help future maintainers understand what went wrong.
* It’s simple and minimal - it does only what’s needed, in a way that both humans and machines can understand now and maintain in the future.
* It's protected by tests. The tests show that it works now and act as a regression suite to avoid it quietly breaking in the future.
* It's documented at an appropriate level, and that documentation reflects the current state of the system - if the code changes an existing behavior the existing documentation needs to be updated to match.
* The design affords future changes. It's important to maintain [YAGNI](https://en.wikipedia.org/wiki/You%5Faren%27t%5Fgonna%5Fneed%5Fit) \- code with added complexity to anticipate future changes that may never come is often bad code - but it's also important not to write code that makes future changes much harder than they should be.
* All of the other relevant "ilities" - accessibility, testability, reliability, security, maintainability, observability, scalability, usability - the non-functional quality measures that are appropriate for the particular class of software being developed.

Coding agent tools can help with most of this, but there is still a substantial burden on the developer driving those tools to ensure that the produced code is good code for the subset of good that's needed for the current project.

## We need to build new habits [#](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/code-is-cheap/#we-need-to-build-new-habits)

The challenge is to develop new personal and organizational habits that respond to the affordances and opportunities of agentic engineering. 

These best practices are still being figured out across our industry. I'm still figuring them out myself.

For now I think the best we can do is to second guess ourselves: any time our instinct says "don't build that, it's not worth the time" fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens.

 ← [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/what-is-agentic-engineering/) 

[Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. **Writing code is cheap now**  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/prompts/)

[ coding-agents189 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/coding-agents/) [ ai-assisted-programming370 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/ai-assisted-programming/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/generative-ai/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/llms/) [ agentic-engineering38 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/agentic-engineering/) [ yagni7 ](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/tags/yagni/) 

 Created: 23rd February 2026  
 Last modified: 24th February 2026  
[7 changes](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/code-is-cheap/changes/) 

**Previous:** [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/what-is-agentic-engineering/)

**Next:** [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/2026/)