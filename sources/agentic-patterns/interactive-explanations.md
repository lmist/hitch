# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/)

## Interactive explanations

When we lose track of how code written by our agents works we take on **cognitive debt**.

For a lot of things this doesn't matter: if the code fetches some data from a database and outputs it as JSON the implementation details are likely simple enough that we don't need to care. We can try out the new feature and make a very solid guess at how it works, then glance over the code to be sure.

Often though the details really do matter. If the core of our application becomes a black box that we don't fully understand we can no longer confidently reason about it, which makes planning new features harder and eventually slows our progress in the same way that accumulated technical debt does.

How do we pay down cognitive debt? By improving our understanding of how the code works.

One of my favorite ways to do that is by building **interactive explanations**.

## Understanding word clouds [#](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/interactive-explanations/#understanding-word-clouds)

In [An AI agent coding skeptic tries AI agent coding, in excessive detail](https://minimaxir.com/2026/02/ai-agent-coding/) Max Woolf mentioned testing LLMs' Rust abilities with the prompt `Create a Rust app that can create "word cloud" data visualizations given a long input text`.

This captured my imagination: I've always wanted to know how word clouds work, so I fired off an [asynchronous research project](https://simonwillison.net/2025/Nov/6/async-code-research/) \- [initial prompt here](https://github.com/simonw/research/pull/91#issue-4002426963), [code and report here](https://github.com/simonw/research/tree/main/rust-wordcloud) \- to explore the idea.

This worked really well: Claude Code for web built me a Rust CLI tool that could produce images like this one:

![A word cloud, many words, different colors and sizes, larger words in the middle.](https://raw.githubusercontent.com/simonw/research/refs/heads/main/rust-wordcloud/wordcloud.png)

But how does it actually work?

Claude's report said it uses "**Archimedean spiral placement** with per-word random angular offset for natural-looking layouts". This did not help me much!

I requested a [linear walkthrough](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/) of the codebase which helped me understand the Rust code in more detail - here's [that walkthrough](https://github.com/simonw/research/blob/main/rust-wordcloud/walkthrough.md) (and [the prompt](https://github.com/simonw/research/commit/2cb8c62477173ef6a4c2e274be9f712734df6126)). This helped me understand the structure of the Rust code but I still didn't have an intuitive understanding of how that "Archimedean spiral placement" part actually worked.

So I asked for an **animated explanation**. I did this by pasting a link to that existing `walkthrough.md` document into a Claude Code session along with the following:

Fetch https://raw.githubusercontent.com/simonw/research/refs/heads/main/rust-wordcloud/walkthrough.md to /tmp using curl so you can read the whole thing Inspired by that, build animated-word-cloud.html - a page that accepts pasted text (which it persists in the \`#fragment\` of the URL such that a page loaded with that \`#\` populated will use that text as input and auto-submit it) such that when you submit the text it builds a word cloud using the algorithm described in that document but does it animated, to make the algorithm as clear to understand. Include a slider for the animation which can be paused and the speed adjusted or even stepped through frame by frame while paused. At any stage the visible in-progress word cloud can be downloaded as a PNG.

You can [play with the result here](https://tools.simonwillison.net/animated-word-cloud). Here's an animated GIF demo: 

![Words appear on the word cloud one at a time, with little boxes showing where the algorithm is attempting to place them - if those boxes overlap an existing word it tries again.](https://static.simonwillison.net/static/2026/animated-word-cloud-demo.gif)

This was using Claude Opus 4.6, which turns out to have quite good taste when it comes to building explanatory animations.

If you watch the animation closely you can see that for each word it attempts to place it somewhere on the page by showing a box, run checks if that box intersects an existing word. If so it continues to try to find a good spot, moving outward in a spiral from the center.

I found that this animation really helped make the way the algorithm worked click for me.

I have long been a fan of animations and interactive interfaces to help explain different concepts. A good coding agent can produce these on demand to help explain code - its own code or code written by others.

 ← [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/linear-walkthroughs/) 

[GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/gif-optimization/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. **Interactive explanations**
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/prompts/)

[ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/ai/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/llms/) [ coding-agents189 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/coding-agents/) [ ai-assisted-programming370 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/ai-assisted-programming/) [ cognitive-debt10 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/cognitive-debt/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/generative-ai/) [ explorables30 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/explorables/) [ agentic-engineering38 ](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/tags/agentic-engineering/) 

 Created: 28th February 2026  
 Last modified: 28th February 2026  
[6 changes](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/interactive-explanations/changes/) 

**Previous:** [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/linear-walkthroughs/)

**Next:** [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/guides/agentic-engineering-patterns/gif-optimization/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/2026/)