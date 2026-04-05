# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/)

## Prompts I use

This section of the guide will be continually updated with prompts that I use myself, linked to from other chapters where appropriate.

## Artifacts [#](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/prompts/#artifacts)

I frequently use Claude's Artifacts feature for prototyping and to build small HTML tools. Artifacts are when regular Claude chat builds an application in HTML and JavaScript and displays it directly within the Claude chat interface. OpenAI and Gemini offer a finial feature which they both call Canvas.

Models love using React for these. I don't like how React requires an additional build step which prevents me from copying and pasting code out of an artifact and into static hosting elsewhere, so I create my artifacts in Claude using a project with the following custom instructions:

Never use React in artifacts - always plain HTML and vanilla JavaScript and CSS with minimal dependencies. CSS should be indented with two spaces and should start like this: \`\`\` <style> \* { box-sizing: border-box; } \`\`\` Inputs and textareas should be font size 16px. Font should always prefer Helvetica. JavaScript should be two space indents and start like this: \`\`\` <script type="module"> // code in here should not be indented at the first level \`\`\` Prefer Sentence case for headings.

## Proofreader [#](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/prompts/#proofreader)

I don't let LLMs write text for my blog. My hard line is that anything that expresses opinions or uses "I" pronouns needs to have been written by me. I'll allow an LLM to update code documentation but if something has my name and personality attached to it then I write it myself.

I do use LLMs to proofread text that I publish. Here's my current proofreading prompt, which I use as custom instructions in a Claude project:

You are a proofreader for posts about to be published. 1\. Identify spelling mistakes and typos 2\. Identify grammar mistakes 3\. Watch out for repeated terms like "It was interesting that X, and it was interesting that Y" 4\. Spot any logical errors or factual mistakes 5\. Highlight weak arguments that could be strengthened 6\. Make sure there are no empty or placeholder links

## Alt text [#](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/prompts/#alt-text)

I use this prompt with images to help write the first draft of the alt text for accessibility.

You write alt text for any image pasted in by the user. Alt text is always presented in a fenced code block to make it easy to copy and paste out. It is always presented on a single line so it can be used easily in Markdown images. All text on the image (for screenshots etc) must be exactly included. A short note describing the nature of the image itself should go first.

I usually use this with Claude Opus, which I find has extremely good taste in alt text. It will often make editorial decisions of its own to do things like highlight just the most interesting numbers from a chart.

These decisions may not always be the right ones. Alt text should express the key meaning that is being conferred by the image. I often edit the text produced by this prompt myself, or provide further prompts telling it to expand certain descriptions or drop extraneous information.

Sometimes I pass multiple images to the same conversation driven by this prompt, since that way the model can describe a subsequent image by making reference to the information communicated by the first.

## Podcast highlights [#](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/prompts/#podcast-highlights)

After I'm a [guest on a podcast](https://simonwillison.net/tags/podcast-appearances/) I like to publish a blog post with some quoted highlights from the conversation. I start by pasting a transcript of the podcast into a Claude Project with the following custom instructions:

You will be given a transcript of a podcast episode. Find the most interesting quotes in that transcript - quotes that best illustrate the overall themes, and quotes that introduce surprising ideas or express things in a particularly clear or engaging or spicy way. Answer just with those quotes - long quotes are fine.

Here's [example output](https://claude.ai/share/713e7c9a-66cb-4c24-a9e2-028ad96ec23b) after pasting in the transcript from [An AI state of the union: We've passed the inflection point, dark factories are coming, and automation timelines](https://www.lennysnewsletter.com/p/an-ai-state-of-the-union) with Lenny Rachitsky.

 ← [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/gif-optimization/) 

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/gif-optimization/)
6. **Appendix**  
   1. **Prompts I use**

[ prompt-engineering182 ](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/tags/prompt-engineering/) 

 Created: 28th February 2026  
 Last modified: 2nd April 2026  
[13 changes](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/prompts/changes/) 

**Previous:** [GIF optimization tool using WebAssembly and Gifsicle](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/guides/agentic-engineering-patterns/gif-optimization/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/2026/)