# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

22nd October 2025 - Link Blog

**[SLOCCount in WebAssembly](https://tools.simonwillison.net/sloccount)**. This project/side-quest got a little bit out of hand.

![Screenshot of SLOCCount web application showing code analysis interface. The page header reads "SLOCCount - Count Lines of Code" with subtitle "Analyze source code to count physical Source Lines of Code (SLOC) using Perl and C programs running via WebAssembly" and "Based on SLOCCount by David A. Wheeler". Three tabs are shown: "Paste Code", "GitHub Repository" (selected), and "Upload ZIP". Below is a text input field labeled "GitHub Repository URL:" containing "simonw/llm" and a blue "Analyze Repository" button. The Analysis Results section displays five statistics: Total Lines: 13,490, Languages: 2, Files: 40, Est. Cost (USD)*: $415,101, and Est. Person-Years*: 3.07.](https://static.simonwillison.net/static/2025/sloccount.jpg)

I remembered an old tool called SLOCCount which could count lines of code and produce an estimate for how much they would cost to develop. I thought it would be fun to play around with it again, especially given how cheap it is to generate code using LLMs these days.

Here's [the homepage for SLOCCount](https://dwheeler.com/sloccount/) by David A. Wheeler. It dates back to 2001!

I figured it might be fun to try and get it running on the web. Surely someone had compiled Perl to WebAssembly...?

[WebPerl](https://webperl.zero-g.net) by Hauke Dämpfling is exactly that, even adding a neat `<script type="text/perl">` tag.

I told Claude Code for web on my iPhone to figure it out and build something, giving it some hints from my initial research:

> Build sloccount.html - a mobile friendly UI for running the Perl sloccount tool against pasted code or against a GitHub repository that is provided in a form field
> 
> It works using the webperl webassembly build of Perl, plus it loads Perl code from this exact commit of this GitHub repository https://github.com/licquia/sloccount/tree/7220ff627334a8f646617fe0fa542d401fb5287e - I guess via the GitHub API, maybe using the https://github.com/licquia/sloccount/archive/7220ff627334a8f646617fe0fa542d401fb5287e.zip URL if that works via CORS
> 
> Test it with playwright Python - don’t edit any file other than sloccount.html and a tests/test\_sloccount.py file

Since I was working on my phone I didn't review the results at all. It seemed to work so I deployed it to static hosting... and then when I went to look at it properly later on found that Claude had given up, cheated and reimplemented it in JavaScript instead!

So I switched to Claude Code on my laptop where I have more control and coached Claude through implementing the project for real. This took _way longer_ than the project deserved - probably a solid hour of my active time, spread out across the morning.

I've shared some of the transcripts - [one](https://gistpreview.github.io/?0fc406a18e14a1f7d28bfff02a18eaaf#simonw/0fc406a18e14a1f7d28bfff02a18eaaf), [two](https://gistpreview.github.io/?56ecae45cf2e1baca798a83deea50939), and [three](https://gistpreview.github.io/?79ca231e801fe1188268a54d30aa67ed) \- as terminal sessions rendered to HTML using my [rtf-to-html](https://tools.simonwillison.net/rtf-to-html) tool.

At one point I realized that the original SLOCCount project wasn't even entirely Perl as I had assumed, it included several C utilities! So I had Claude Code figure out how to compile those to WebAssembly (it used Emscripten) and incorporate those into the project (with [notes on what it did](https://github.com/simonw/tools/blob/473e89edfebc27781b434430f2e8a76adfbe3b16/lib/README.md#webassembly-compilation-of-c-programs).)

The end result ([source code here](https://github.com/simonw/tools/blob/main/sloccount.html)) is actually pretty cool. It's a web UI with three tabs - one for pasting in code, a second for loading code from a GitHub repository and a third that lets you open a Zip file full of code that you want to analyze. Here's an animated demo:

![I enter simonw/llm in the GitHub repository field. It loads 41 files from GitHub and displays a report showing the number of lines and estimated cost.](https://static.simonwillison.net/static/2025/sloccount-optimized.gif)

The cost estimates it produces are of very little value. By default it uses the original method from 2001\. You can also twiddle the factors - bumping up the expected US software engineer's annual salary from its 2000 estimate of $56,286 is a good start! 

I had ChatGPT [take a guess](https://chatgpt.com/share/68f7e0ac-00c4-8006-979e-64d1f0162283) at what those figures should be for today and included those in the tool, with a **very** prominent warning not to trust them in the slightest.

Posted [22nd October 2025](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2025/Oct/22/) at 6:12 am

## Recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is a **link post** by Simon Willison, posted on [22nd October 2025](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2025/Oct/22/).

[ javascript750 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/javascript/) [ perl29 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/perl/) [ projects523 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/projects/) [ tools53 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/tools/) [ ai1947 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/ai/) [ webassembly90 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/webassembly/) [ generative-ai1728 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/generative-ai/) [ llms1695 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/llms/) [ ai-assisted-programming371 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/ai-assisted-programming/) [ vibe-coding80 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/vibe-coding/) [ claude-code103 ](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/tags/claude-code/) 

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/about/#disclosures)
* [Colophon](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/about/#about-site)
* ©
* [2002](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2002/)
* [2003](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2003/)
* [2004](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2004/)
* [2005](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2005/)
* [2006](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2006/)
* [2007](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2007/)
* [2008](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2008/)
* [2009](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2009/)
* [2010](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2010/)
* [2011](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2011/)
* [2012](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2012/)
* [2013](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2013/)
* [2014](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2014/)
* [2015](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2015/)
* [2016](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2016/)
* [2017](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2017/)
* [2018](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2018/)
* [2019](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2019/)
* [2020](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2020/)
* [2021](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2021/)
* [2022](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2022/)
* [2023](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2023/)
* [2024](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2024/)
* [2025](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2025/)
* [2026](https://simonwillison.net/2025/Oct/22/sloccount-in-webassembly/2026/)