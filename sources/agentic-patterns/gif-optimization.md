# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

[Guides](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/) \> [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/)

## GIF optimization tool using WebAssembly and Gifsicle

I like to include animated GIF demos in my online writing, often recorded using [LICEcap](https://www.cockos.com/licecap/). There's an example in the [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/) chapter.

These GIFs can be pretty big. I've tried a few tools for optimizing GIF file size and my favorite is [Gifsicle](https://github.com/kohler/gifsicle) by Eddie Kohler. It compresses GIFs by identifying regions of frames that have not changed and storing only the differences, and can optionally reduce the GIF color palette or apply visible lossy compression for greater size reductions.

Gifsicle is written in C and the default interface is a command line tool. I wanted a web interface so I could access it in my browser and visually preview and compare the different settings.

I prompted Claude Code for web (from my iPhone using the Claude iPhone app) against my [simonw/tools](https://github.com/simonw/tools) repo with the following:

gif-optimizer.html Compile gifsicle to WASM, then build a web page that lets you open or drag-drop an animated GIF onto it and it then shows you that GIF compressed using gifsicle with a number of different settings, each preview with the size and a download button Also include controls for the gifsicle options for manual use - each preview has a “tweak these settings” link which sets those manual settings to the ones used for that preview so the user can customize them further Run “uvx rodney –help” and use that tool to tray your work - use this GIF for testing https://static.simonwillison.net/static/2026/animated-word-cloud-demo.gif

Here's [what it built](https://tools.simonwillison.net/gif-optimizer), plus an animated GIF demo that I optimized using the tool:

![Animation. I drop on a GIF and the tool updates the page with a series of optimized versions under different settings. I eventually select Tweak settings on one of them, scroll to the bottom, adjust some sliders and download the result.](https://static.simonwillison.net/static/2026/demo2-32-colors-lossy.gif)

Let's address that prompt piece by piece.

> `gif-optimizer.html`

The first line simply tells it the name of the file I want to create. Just a filename is enough here - I know that when Claude runs "ls" on the repo it will understand that every file is a different tool.

My [simonw/tools](https://github.com/simonw/tools) repo currently lacks a `CLAUDE.md` or `AGENTS.md` file. I've found that agents pick up enough of the gist of the repo just from scanning the existing file tree and looking at relevant code in existing files.

> `Compile gifsicle to WASM, then build a web page that lets you open or drag-drop an animated GIF onto it and it then shows you that GIF compressed using gifsicle with a number of different settings, each preview with the size and a download button`

I'm making a bunch of assumptions here about Claude's existing knowledge, all of which paid off.

Gifsicle is nearly 30 years old now and is a widely used piece of software - I was confident that referring to it by name would be enough for Claude to find the code.

"`Compile gifsicle to WASM`" is doing a _lot_ of work here.

WASM is short for [WebAssembly](https://webassembly.org/), the technology that lets browsers run compiled code safely in a sandbox.

Compiling a project like Gifsicle to WASM is not a trivial operation, involving a complex toolchain usually involving the [Emscripten](https://emscripten.org/) project. It often requires a lot of trial and error to get everything working.

Coding agents are fantastic at trial and error! They can often brute force their way to a solution where I would have given up after the fifth inscrutable compiler error.

I've seen Claude Code figure out WASM builds many times before, so I was quite confident this would work.

"`then build a web page that lets you open or drag-drop an animated GIF onto it`" describes a pattern I've used in a lot of my other tools.

HTML file uploads work fine for selecting files, but a nicer UI, especially on desktop, is to allow users to drag and drop files into a prominent drop zone on a page.

Setting this up involves a bit of JavaScript to process the events and some CSS for the drop zone. It's not complicated but it's enough extra work that I might not normally add it myself. With a prompt it's almost free.

Here's the resulting UI - which was influenced by Claude taking a peek at my existing [image-resize-quality](https://tools.simonwillison.net/image-resize-quality) tool:

![Screenshot of a web application titled "GIF Optimizer" with subtitle "Powered by gifsicle compiled to WebAssembly — all processing happens in your browser". A large dashed-border drop zone reads "Drop an animated GIF here or click to select". Below is a text input with placeholder "Or paste a GIF URL..." and a blue "Load URL" button. Footer text reads "Built with gifsicle by Eddie Kohler, compiled to WebAssembly. gifsicle is released under the GNU General Public License, version 2."](https://static.simonwillison.net/static/2026/gif-optimizer.jpg)

I didn't ask for the GIF URL input and I'm not keen on it, because it only works against URLs to GIFs that are served with open CORS headers. I'll probably remove that in a future update.

"`then shows you that GIF compressed using gifsicle with a number of different settings, each preview with the size and a download button`" describes the key feature of the application.

I didn't bother defining the collection of settings I wanted - in my experience Claude has good enough taste at picking those for me, and we can always change them if its first guesses don't work.

Showing the size is important since this is all about optimizing for size.

I know from past experience that asking for a "download button" gets a button with the right HTML and JavaScript mechanisms set up such that clicking it provides a file save dialog, which is a nice convenience over needing to right-click-save-as.

> `Also include controls for the gifsicle options for manual use - each preview has a “tweak these settings” link which sets those manual settings to the ones used for that preview so the user can customize them further`

This is a pretty clumsy prompt - I was typing it in my phone after all - but it expressed my intention well enough for Claude to build what I wanted. 

Here's what that looks like in the resulting tool, this screenshot showing the mobile version. Each image has a "Tweak these settings" button which, when clicked, updates this set of manual settings and sliders:

![Screenshot of a GIF Optimizer results and settings panel. At top, results show "110.4 KB (original: 274.0 KB) — 59.7% smaller" in green, with a blue "Download" button and a "Tweak these settings" button. Below is a "Manual Settings" card containing: "Optimization level" dropdown set to "-O3 (aggressive)", "Lossy (0 = off, higher = more loss)" slider set to 0, "Colors (0 = unchanged)" slider set to 0, "Color reduction method" dropdown set to "Default", "Scale (%)" slider set to 100%, "Dither" dropdown set to "Default", and a blue "Optimize with these settings" button.](https://static.simonwillison.net/static/2026/gif-optimizer-tweak.jpg)

> `Run “uvx rodney --help” and use that tool to tray your work - use this GIF for testing https://static.simonwillison.net/static/2026/animated-word-cloud-demo.gif`

Coding agents work _so much better_ if you make sure they have the ability to test their code while they are working.

There are many different ways to test a web interface - [Playwright](https://playwright.dev/) and [Selenium](https://www.selenium.dev/) and [agent-browser](https://agent-browser.dev/) are three solid options.

[Rodney](https://github.com/simonw/rodney) is a browser automation tool I built myself, which is quick to install and has `--help` output that's designed to teach an agent everything it needs to know to use the tool.

This worked great - in [the session transcript](https://claude.ai/code/session%5F01C8JpE3yQpwHfBCFni4ZUc4) you can see Claude using Rodney and fixing some minor bugs that it spotted, for example:

> The CSS `display: none` is winning over the inline style reset. I need to set `display: 'block'` explicitly.

## The follow-up prompts [#](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/gif-optimization/#the-follow-up-prompts)

When I'm working with Claude Code I usually keep an eye on what it's doing so I can redirect it while it's still in flight. I also often come up with new ideas while it's working which I then inject into the queue.

> `Include the build script and diff against original gifsicle code in the commit in an appropriate subdirectory`
> 
> `The build script should clone the gifsicle repo to /tmp and switch to a known commit before applying the diff - so no copy of gifsicle in the commit but all the scripts needed to build the wqsm`

I added this when I noticed it was putting a _lot_ of effort into figuring out how to get Gifsicle working with WebAssembly, including patching the original source code. Here's [the patch](https://github.com/simonw/tools/blob/main/lib/gifsicle/gifsicle-wasm.patch) and [the build script](https://github.com/simonw/tools/blob/main/lib/gifsicle/build.sh) it added to the repo.

I knew there was a pattern in that repo already for where supporting files lived but I couldn't remember what that pattern was. Saying "in an appropriate subdirectory" was enough for Claude to figure out where to put it - it found and used the existing [lib/ directory](https://github.com/simonw/tools/tree/main/lib).

> `You should include the wasm bundle`

This probably wasn't necessary, but I wanted to make absolutely sure that the compiled WASM file (which turned out [to be 233KB](https://github.com/simonw/tools/blob/main/lib/gifsicle/gifsicle.wasm)) was committed to the repo. I serve `simonw/tools` via GitHub Pages at [tools.simonwillison.net](https://tools.simonwillison.net/) and I wanted it to work without needing to be built locally.

> `Make sure the HTML page credits gifsicle and links to the repo`

This is just polite! I often build WebAssembly wrappers around other people's open source projects and I like to make sure they get credit in the resulting page.

Claude added this to the footer of the tool:

> Built with [gifsicle](https://github.com/kohler/gifsicle) by Eddie Kohler, compiled to WebAssembly. gifsicle is released under the GNU General Public License, version 2.

 ← [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/interactive-explanations/) 

[Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/prompts/) →

This is a chapter from the guide **[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/)**.

**Chapters in this guide**

1. **Principles**  
   1. [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
   2. [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/code-is-cheap/)  
   3. [Hoard things you know how to do](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)  
   4. [AI should help us produce better code](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/better-code/)  
   5. [Anti-patterns: things to avoid](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/anti-patterns/)
2. **Working with coding agents**  
   1. [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/how-coding-agents-work/)  
   2. [Using Git with coding agents](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/using-git-with-coding-agents/)  
   3. [Subagents](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/subagents/)
3. **Testing and QA**  
   1. [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/red-green-tdd/)  
   2. [First run the tests](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/first-run-the-tests/)  
   3. [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/agentic-manual-testing/)
4. **Understanding code**  
   1. [Linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/linear-walkthroughs/)  
   2. [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/interactive-explanations/)
5. **Annotated prompts**  
   1. **GIF optimization tool using WebAssembly and Gifsicle**
6. **Appendix**  
   1. [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/prompts/)

[ claude264 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/claude/) [ ai1947 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/ai/) [ claude-code103 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/claude-code/) [ llms1695 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/llms/) [ prompt-engineering182 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/prompt-engineering/) [ webassembly90 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/webassembly/) [ coding-agents190 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/coding-agents/) [ tools53 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/tools/) [ generative-ai1728 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/generative-ai/) [ gif5 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/gif/) [ agentic-engineering39 ](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/tags/agentic-engineering/) 

 Created: 2nd March 2026  
 Last modified: 2nd March 2026  
[3 changes](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/gif-optimization/changes/) 

**Previous:** [Interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/interactive-explanations/)

**Next:** [Prompts I use](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/guides/agentic-engineering-patterns/prompts/)

* [Disclosures](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/about/#disclosures)
* [Colophon](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/about/#about-site)
* ©
* [2002](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2002/)
* [2003](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2003/)
* [2004](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2004/)
* [2005](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2005/)
* [2006](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2006/)
* [2007](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2007/)
* [2008](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2008/)
* [2009](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2009/)
* [2010](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2010/)
* [2011](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2011/)
* [2012](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2012/)
* [2013](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2013/)
* [2014](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2014/)
* [2015](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2015/)
* [2016](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2016/)
* [2017](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2017/)
* [2018](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2018/)
* [2019](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2019/)
* [2020](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2020/)
* [2021](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2021/)
* [2022](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2022/)
* [2023](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2023/)
* [2024](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2024/)
* [2025](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2025/)
* [2026](https://simonwillison.net/guides/agentic-engineering-patterns/gif-optimization/2026/)