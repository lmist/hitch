# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/)

## Anti-patterns: things to avoid

There are some behaviors that are anti-patterns in our weird new world of agentic engineering.

## Inflicting unreviewed code on collaborators [#](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/anti-patterns/#inflicting-unreviewed-code-on-collaborators)

This anti-pattern is common and deeply frustrating.

**Don't file pull requests with code you haven't reviewed yourself**.

If you open a PR with hundreds (or thousands) of lines of code that an agent produced for you, and you haven't done the work to ensure that code is functional yourself, you are delegating the actual work to other people.

They could have prompted an agent themselves. What value are you even providing?

If you put code up for review you need to be confident that it's ready for other people to spend their time on it. The initial review pass is your responsibility, not something you should farm out to others.

A good agentic engineering pull request has the following characteristics:

* The code works, and you are confident that it works. [Your job is to deliver code that works](https://simonwillison.net/2025/Dec/18/code-proven-to-work/).
* The change is small enough to be reviewed efficiently without inflicting too much additional cognitive load on the reviewer. Several small PRs beats one big one, and splitting code into separate commits is easy with a coding agent to do the Git finagling for you.
* The PR includes additional context to help explain the change. What's the higher level goal that the change serves? Linking to relevant issues or specifications is useful here.
* Agents write convincing looking pull request descriptions. You need to review these too! It's rude to expect someone else to read text that you haven't read and validated yourself.

Given how easy it is to dump unreviewed code on other people, I recommend including some form of evidence that you've put that extra work in yourself. Notes on how you manually tested it, comments on specific implementation choices or even screenshots and video of the feature working go a _long_ way to demonstrating that a reviewer's time will not be wasted digging into the details.

 ← [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/better-code/) 

[How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/how-coding-agents-work/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/better-code/)  
   5. **Anti-patterns: things to avoid**
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/prompts/)

[ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/llms/) [ ai-ethics286 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/ai-ethics/) [ coding-agents190 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/coding-agents/) [ ai-assisted-programming371 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/ai-assisted-programming/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/generative-ai/) [ agentic-engineering39 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/agentic-engineering/) [ code-review14 ](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/tags/code-review/) 

 Created: 4th March 2026  
 Last modified: 4th March 2026  
[2 changes](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/anti-patterns/changes/) 

**Previous:** [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/better-code/)

**Next:** [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/guides/agentic-engineering-patterns/how-coding-agents-work/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/2026/)