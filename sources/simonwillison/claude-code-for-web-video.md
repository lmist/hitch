# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Video: Building a tool to copy-paste share terminal sessions using Claude Code for web

23rd October 2025

This afternoon I was manually converting a terminal session into a shared HTML file for the umpteenth time when I decided to reduce the friction by building a custom tool for it—and on the spur of the moment I fired up [Descript](https://www.descript.com/) to record the process. The result is this new [11 minute YouTube video](https://www.youtube.com/watch?v=GQvMLLrFPVI) showing my workflow for vibe-coding simple tools from start to finish.

#### The initial problem [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#the-initial-problem)

The problem I wanted to solve involves sharing my Claude Code CLI sessions—and the more general problem of sharing interesting things that happen in my terminal.

A while back I discovered (using my vibe-coded [clipboard inspector](https://tools.simonwillison.net/clipboard-viewer)) that copying and pasting from the macOS terminal populates a rich text clipboard format which preserves the colors and general formatting of the terminal output.

The problem is that format looks like this:

```
{\rtf1\ansi\ansicpg1252\cocoartf2859
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Monaco;}
{\colortbl;\red255\green255\blue255;\red242\green242\blue242;\red0\green0\blue0;\red204\green98\blue70;
\red0\green0\blue0;\red97\green97\blue97;\red102\green102\blue102;\red255\

```

This struck me as the kind of thing an LLM might be able to write code to parse, so I had [ChatGPT take a crack at it](https://chatgpt.com/share/680801ad-0804-8006-83fc-c2b209841a9c) and then later [rewrote it from scratch with Claude Sonnet 4.5](https://claude.ai/share/5c12dd0e-713d-4f32-a6c1-d05dee353e4d). The result was [this rtf-to-html tool](https://tools.simonwillison.net/rtf-to-html) which lets you paste in rich formatted text and gives you reasonably solid HTML that you can share elsewhere.

To share that HTML I’ve started habitually pasting it into a [GitHub Gist](https://gist.github.com/) and then taking advantage of `gitpreview.github.io`, a neat little unofficial tool that accepts `?GIST_ID` and displays the gist content as a standalone HTML page... which means you can link to rendered HTML that’s stored in a gist.

So my process was:

1. Copy terminal output
2. Paste into [rtf-to-html](https://tools.simonwillison.net/rtf-to-html)
3. Copy resulting HTML
4. Paste that int a new GitHub Gist
5. Grab that Gist’s ID
6. Share the link to `gitpreview.github.io?GIST_ID`

Not too much hassle, but frustratingly manual if you’re doing it several times a day.

#### The desired solution [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#the-desired-solution)

Ideally I want a tool where I can do this:

1. Copy terminal output
2. Paste into a new tool
3. Click a button and get a `gistpreview` link to share

I decided to get Claude Code for web to build the entire thing.

#### The prompt [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#the-prompt)

Here’s the full prompt I used on [claude.ai/code](https://claude.ai/code), pointed at my `simonw/tools` repo, to build the tool:

> `Build a new tool called terminal-to-html which lets the user copy RTF directly from their terminal and paste it into a paste area, it then produces the HTML version of that in a textarea with a copy button, below is a button that says "Save this to a Gist", and below that is a full preview. It will be very similar to the existing rtf-to-html.html tool but it doesn't show the raw RTF and it has that Save this to a Gist button`
> 
> `That button should do the same trick that openai-audio-output.html does, with the same use of localStorage and the same flow to get users signed in with a token if they are not already`
> 
> `So click the button, it asks the user to sign in if necessary, then it saves that HTML to a Gist in a file called index.html, gets back the Gist ID and shows the user the URL https://gistpreview.github.io/?6d778a8f9c4c2c005a189ff308c3bc47 - but with their gist ID in it`
> 
> `They can see the URL, they can click it (do not use target="_blank") and there is also a "Copy URL" button to copy it to their clipboard`
> 
> `Make the UI mobile friendly but also have it be courier green-text-on-black themed to reflect what it does`
> 
> `If the user pastes and the pasted data is available as HTML but not as RTF skip the RTF step and process the HTML directly`
> 
> `If the user pastes and it's only available as plain text then generate HTML that is just an open <pre> tag and their text and a closing </pre> tag`

It’s quite a long prompt—it took me several minutes to type! But it covered the functionality I wanted in enough detail that I was pretty confident Claude would be able to build it.

#### Combining previous tools [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#combining)

I’m using one key technique in this prompt: I’m referencing existing tools in the same repo and telling Claude to imitate their functionality.

I first wrote about this trick last March in [Running OCR against PDFs and images directly in your browser](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/), where I described how a snippet of code that used PDF.js and another snippet that used Tesseract.js was enough for Claude 3 Opus to build me this [working PDF OCR tool](https://tools.simonwillison.net/ocr). That was actually the tool that kicked off my [tools.simonwillison.net](https://tools.simonwillison.net/) collection in the first place, which has since grown to 139 and counting.

Here I’m telling Claude that I want the RTF to HTML functionality of [rtf-to-html.html](https://github.com/simonw/tools/blob/main/rtf-to-html.html) combined with the Gist saving functionality of [openai-audio-output.html](https://github.com/simonw/tools/blob/main/openai-audio-output.html).

That one has quite a bit going on. It uses the OpenAI audio API to generate audio output from a text prompt, which is returned by that API as base64-encoded data in JSON.

Then it offers the user a button to save that JSON to a Gist, which gives the snippet a URL.

Another tool I wrote, [gpt-4o-audio-player.html](https://github.com/simonw/tools/blob/main/gpt-4o-audio-player.html), can then accept that Gist ID in the URL and will fetch the JSON data and make the audio playable in the browser. [Here’s an example](https://tools.simonwillison.net/gpt-4o-audio-player?gist=4a982d3fe7ba8cb4c01e89c69a4a5335).

The trickiest part of this is API tokens. I’ve built tools in the past that require users to paste in a GitHub Personal Access Token (PAT) (which I then store in `localStorage` in their browser—I don’t want other people’s authentication credentials anywhere near my own servers). But that’s a bit fiddly.

Instead, I [figured out](https://gist.github.com/simonw/975b8934066417fe771561a1b672ad4f) the minimal Cloudflare worker necessary to implement the server-side portion of GitHub’s authentication flow. That code [lives here](https://github.com/simonw/tools/blob/main/cloudflare-workers/github-auth.js) and means that any of the HTML+JavaScript tools in my collection can implement a GitHub authentication flow if they need to save Gists.

But I don’t have to tell the model any of that! I can just say “do the same trick that openai-audio-output.html does” and Claude Code will work the rest out for itself.

#### The result [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#the-result)

Here’s what [the resulting app](https://tools.simonwillison.net/terminal-to-html) looks like after I’ve pasted in some terminal output from Claude Code CLI:

![Terminal to HTML app. Green glowing text on black. Instructions: Paste terminal output below. Supports RTF, HTML or plain text. There's an HTML Code area with a Copy HTML button, Save this to a Gist and a bunch of HTML. Below is the result of save to a gist showing a URL and a Copy URL button. Below that a preview with the Claude Code heading in ASCII art.](https://static.simonwillison.net/static/2025/terminal-to-html.jpg)

It’s exactly what I asked for, and the green-on-black terminal aesthetic is spot on too.

#### Other notes from the video [#](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/claude-code-for-web-video/#other-notes-from-the-video)

There are a bunch of other things that I touch on in the video. Here’s a quick summary:

* [tools.simonwillison.net/colophon](https://tools.simonwillison.net/colophon) is the list of all of my tools, with accompanying AI-generated descriptions. Here’s [more about how I built that with Claude Code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/#a-detailed-example) and notes on [how I added the AI-generated descriptions](https://simonwillison.net/2025/Mar/13/tools-colophon/).
* [gistpreview.github.io](https://gistpreview.github.io) is really neat.
* I used [Descript](https://www.descript.com/) to record and edit the video. I’m still getting the hang of it—hence the slightly clumsy pan-and-zoom—but it’s pretty great for this kind of screen recording.
* The site’s automated deploys are managed [by this GitHub Actions workflow](https://github.com/simonw/tools/blob/main/.github/workflows/pages.yml). I also have it configured to work with [Cloudflare Pages](https://pages.cloudflare.com/) for those preview deployments from PRs (here’s [an example](https://github.com/simonw/tools/pull/84#issuecomment-3434969331)).
* The automated documentation is created using my [llm](https://llm.datasette.io/) tool and [llm-anthropic](https://github.com/simonw/llm-anthropic) plugin. Here’s [the script that does that](https://github.com/simonw/tools/blob/main/write%5Fdocs.py), recently [upgraded](https://github.com/simonw/tools/commit/99f5f2713f8001b72f4b1cafee5a15c0c26efb0d) to use Claude Haiku 4.5.

Posted [23rd October 2025](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/) at 4:14 am · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Video: Building a tool to copy-paste share terminal sessions using Claude Code for web** by Simon Willison, posted on [23rd October 2025](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/23/).

Part of series **[How I use LLMs and ChatGPT](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/series/using-llms/)**

1. [Vibe engineering](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/7/vibe-engineering/) \- Oct. 7, 2025, 2:32 p.m.
2. [Claude can write complete Datasette plugins now](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/8/claude-datasette-plugins/) \- Oct. 8, 2025, 11:43 p.m.
3. [Getting DeepSeek-OCR working on an NVIDIA Spark via brute force using Claude Code](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/20/deepseek-ocr-claude-code/) \- Oct. 20, 2025, 5:21 p.m.
4. **Video: Building a tool to copy-paste share terminal sessions using Claude Code for web** \- Oct. 23, 2025, 4:14 a.m.
5. [Video + notes on upgrading a Datasette plugin for the latest 1.0 alpha, with help from uv and OpenAI Codex CLI](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Nov/6/upgrading-datasette-plugins/) \- Nov. 6, 2025, 6:26 p.m.
6. [Useful patterns for building HTML tools](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Dec/10/html-tools/) \- Dec. 10, 2025, 9 p.m.
7. [I ported JustHTML from Python to JavaScript with Codex CLI and GPT-5.2 in 4.5 hours](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Dec/15/porting-justhtml/) \- Dec. 15, 2025, 11:58 p.m.
8. [… more](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/series/using-llms/)

[ github183 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/github/) [ tools53 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/tools/) [ youtube57 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/youtube/) [ ai1947 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/ai/) [ cloudflare30 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/cloudflare/) [ generative-ai1728 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/generative-ai/) [ llms1695 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/llms/) [ ai-assisted-programming371 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/ai-assisted-programming/) [ anthropic266 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/anthropic/) [ claude264 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/claude/) [ vibe-coding80 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/vibe-coding/) [ coding-agents190 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/coding-agents/) [ claude-code103 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/claude-code/) [ async-coding-agents17 ](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/tags/async-coding-agents/) 

**Next:** [Hacking the WiFi-enabled color screen GitHub Universe conference badge](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/28/github-universe-badge/)

**Previous:** [Dane Stuckey (OpenAI CISO) on prompt injection risks for ChatGPT Atlas](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/Oct/22/openai-ciso-on-atlas/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/about/#disclosures)
* [Colophon](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/about/#about-site)
* ©
* [2002](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2002/)
* [2003](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2003/)
* [2004](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2004/)
* [2005](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2005/)
* [2006](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2006/)
* [2007](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2007/)
* [2008](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2008/)
* [2009](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2009/)
* [2010](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2010/)
* [2011](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2011/)
* [2012](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2012/)
* [2013](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2013/)
* [2014](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2014/)
* [2015](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2015/)
* [2016](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2016/)
* [2017](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2017/)
* [2018](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2018/)
* [2019](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2019/)
* [2020](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2020/)
* [2021](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2021/)
* [2022](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2022/)
* [2023](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2023/)
* [2024](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2024/)
* [2025](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2025/)
* [2026](https://simonwillison.net/2025/Oct/23/claude-code-for-web-video/2026/)