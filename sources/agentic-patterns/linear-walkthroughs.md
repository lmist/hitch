# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/)

## Linear walkthroughs

Sometimes it's useful to have a coding agent give you a structured walkthrough of a codebase. 

Maybe it's existing code you need to get up to speed on, maybe it's your own code that you've forgotten the details of, or maybe you vibe coded the whole thing and need to understand how it actually works.

Frontier models with the right agent harness can construct a detailed walkthrough to help you understand how code works.

## An example using Showboat and Present [#](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/linear-walkthroughs/#an-example-using-showboat-and-present)

I recently [vibe coded a SwiftUI slide presentation app](https://simonwillison.net/2026/Feb/25/present/) on my Mac using Claude Code and Opus 4.6.

I was speaking about the advances in frontier models between November 2025 and February 2026, and I like to include at least one gimmick in my talks (a [STAR moment](https://simonwillison.net/2019/Dec/10/better-presentations/) \- Something They'll Always Remember). In this case I decided the gimmick would be revealing at the end of the presentation that the slide mechanism itself was an example of what vibe coding could do.

I released the code [to GitHub](https://github.com/simonw/present) and then realized I didn't know anything about how it actually worked - I had prompted the whole thing into existence ([partial transcript here](https://gisthost.github.io/?bfbc338977ceb71e298e4d4d5ac7d63c)) without paying any attention to the code it was writing.

So I fired up a new instance of Claude Code for web, pointed it at my repo and prompted:

Read the source and then plan a linear walkthrough of the code that explains how it all works in detail Then run “uvx showboat –help” to learn showboat - use showboat to create a walkthrough.md file in the repo and build the walkthrough in there, using showboat note for commentary and showboat exec plus sed or grep or cat or whatever you need to include snippets of code you are talking about

[Showboat](https://github.com/simonw/showboat) is a tool I built to help coding agents write documents that demonstrate their work. You can see the [showboat --help output here](https://github.com/simonw/showboat/blob/main/help.txt), which is designed to give the model everything it needs to know in order to use the tool. 

The `showboat note` command adds Markdown to the document. The `showboat exec` command accepts a shell command, executes it and then adds both the command and its output to the document.

By telling it to use "sed or grep or cat or whatever you need to include snippets of code you are talking about" I ensured that Claude Code would not manually copy snippets of code into the document, since that could introduce a risk of hallucinations or mistakes.

This worked extremely well. Here's the [document Claude Code created with Showboat](https://github.com/simonw/present/blob/main/walkthrough.md), which talks through all six `.swift` files in detail and provides a clear and actionable explanation about how the code works.

I learned a great deal about how SwiftUI apps are structured and absorbed some solid details about the Swift language itself just from reading this document.

If you are concerned that LLMs might reduce the speed at which you learn new skills I strongly recommend adopting patterns like this one. Even a \~40 minute vibe coded toy project can become an opportunity to explore new ecosystems and pick up some interesting new tricks.

 ← [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/agentic-manual-testing/) 

[Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/interactive-explanations/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. **Linear walkthroughs**  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/prompts/)

[ agentic-engineering39 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/agentic-engineering/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/llms/) [ vibe-coding80 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/vibe-coding/) [ coding-agents190 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/coding-agents/) [ ai-assisted-programming371 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/ai-assisted-programming/) [ swift11 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/swift/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/generative-ai/) [ showboat14 ](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/tags/showboat/) 

 Created: 25th February 2026  
 Last modified: 4th March 2026  
[7 changes](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/linear-walkthroughs/changes/) 

**Previous:** [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/agentic-manual-testing/)

**Next:** [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/guides/agentic-engineering-patterns/interactive-explanations/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/2026/)